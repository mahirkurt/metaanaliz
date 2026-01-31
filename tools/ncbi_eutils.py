from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import requests

from ._io import write_json
from .search_log import append_search_log_row
from .wiley_tdm import load_dotenv_if_present


EUTILS_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


@dataclass
class NcbieutilsClient:
    api_key: Optional[str] = None
    email: Optional[str] = None
    tool: str = "meta-analysis-repo"
    base_url: str = EUTILS_BASE_URL
    timeout_s: int = 60
    user_agent: str = "meta-analysis-repo/1.0 (ncbi-eutils)"

    def _common_params(self) -> dict[str, str]:
        params: dict[str, str] = {"tool": self.tool}
        if self.email:
            params["email"] = self.email
        if self.api_key:
            params["api_key"] = self.api_key
        return params

    def esearch(
        self,
        *,
        db: str,
        term: str,
        retmax: int = 20,
        retstart: int = 0,
        usehistory: bool = False,
        sort: str = "",
        datetype: str = "",
        mindate: str = "",
        maxdate: str = "",
    ) -> dict[str, Any]:
        url = f"{self.base_url}/esearch.fcgi"
        params = {
            **self._common_params(),
            "db": db,
            "term": term,
            "retmax": str(retmax),
            "retstart": str(retstart),
            "retmode": "json",
        }
        if usehistory:
            params["usehistory"] = "y"
        if sort:
            params["sort"] = sort
        if datetype:
            params["datetype"] = datetype
        if mindate:
            params["mindate"] = mindate
        if maxdate:
            params["maxdate"] = maxdate

        headers = {"User-Agent": self.user_agent}
        r = requests.get(url, params=params, headers=headers, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def esummary(self, *, db: str, ids: str) -> dict[str, Any]:
        url = f"{self.base_url}/esummary.fcgi"
        params = {**self._common_params(), "db": db, "id": ids, "retmode": "json"}
        headers = {"User-Agent": self.user_agent}
        r = requests.get(url, params=params, headers=headers, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def efetch(
        self,
        *,
        db: str,
        ids: str,
        rettype: str = "",
        retmode: str = "xml",
    ) -> str:
        url = f"{self.base_url}/efetch.fcgi"
        params = {**self._common_params(), "db": db, "id": ids, "retmode": retmode}
        if rettype:
            params["rettype"] = rettype
        headers = {"User-Agent": self.user_agent}
        r = requests.get(url, params=params, headers=headers, timeout=self.timeout_s)
        r.raise_for_status()
        return r.text


def _load_ncbi_creds(args: argparse.Namespace) -> tuple[Optional[str], Optional[str]]:
    api_key = args.api_key or os.getenv("PUBMED_API_KEY") or os.getenv("NCBI_API_KEY")
    email = args.email or os.getenv("PUBMED_EMAIL") or os.getenv("NCBI_EMAIL")
    return api_key, email


def _safe_int(v: Any) -> Optional[int]:
    try:
        return int(v)
    except Exception:
        return None


def cmd_esearch(args: argparse.Namespace) -> None:
    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))
    api_key, email = _load_ncbi_creds(args)

    client = NcbieutilsClient(api_key=api_key, email=email, timeout_s=args.timeout)
    payload = client.esearch(
        db=args.db,
        term=args.term,
        retmax=args.retmax,
        retstart=args.retstart,
        usehistory=args.usehistory,
        sort=args.sort,
        datetype=args.datetype,
        mindate=args.mindate,
        maxdate=args.maxdate,
    )

    out_path = Path(args.out)
    write_json(out_path, payload)

    # NCBI JSON schema: esearchresult.count
    count = _safe_int(((payload.get("esearchresult") or {}).get("count")))

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source=f"NCBI E-utilities ({args.db})",
        interface="API",
        query=args.term,
        filters=args.filters or "",
        sort=args.sort or "",
        results_total=count,
        exported_format="json",
        export_scope=f"retstart={args.retstart};retmax={args.retmax}"
        + ("; usehistory=y" if args.usehistory else ""),
        endpoint=f"{client.base_url}/esearch.fcgi",
        notes=(
            f"saved={out_path.as_posix()}"
            + (f"; email={email}" if email else "")
            + ("; api_key=yes" if api_key else "; api_key=no")
        ),
    )

    print(out_path)


def cmd_esummary(args: argparse.Namespace) -> None:
    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))
    api_key, email = _load_ncbi_creds(args)

    client = NcbieutilsClient(api_key=api_key, email=email, timeout_s=args.timeout)
    payload = client.esummary(db=args.db, ids=args.ids)
    out_path = Path(args.out)
    write_json(out_path, payload)

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source=f"NCBI E-utilities ({args.db})",
        interface="API",
        query=f"ids:{args.ids}",
        results_total=None,
        exported_format="json",
        export_scope="ids",
        endpoint=f"{client.base_url}/esummary.fcgi",
        notes=f"saved={out_path.as_posix()}" + (f"; email={email}" if email else ""),
    )

    print(out_path)


def cmd_efetch(args: argparse.Namespace) -> None:
    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))
    api_key, email = _load_ncbi_creds(args)

    client = NcbieutilsClient(api_key=api_key, email=email, timeout_s=args.timeout)
    text = client.efetch(db=args.db, ids=args.ids, rettype=args.rettype, retmode=args.retmode)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source=f"NCBI E-utilities ({args.db})",
        interface="API",
        query=f"ids:{args.ids}",
        exported_format=args.retmode,
        export_scope="ids",
        endpoint=f"{client.base_url}/efetch.fcgi",
        notes=(
            f"saved={out_path.as_posix()}"
            + (f"; email={email}" if email else "")
            + (f"; rettype={args.rettype}" if args.rettype else "")
        ),
    )

    print(out_path)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.ncbi_eutils",
        description="NCBI E-utilities (PubMed/MEDLINE ve PMC) için repo-local CLI.",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    # Common args group builder
    def add_common(s: argparse.ArgumentParser) -> None:
        s.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")
        s.add_argument(
            "--dotenv",
            default=".env",
            help=".env dosya yolu (default: .env). Var ise otomatik okunur.",
        )
        s.add_argument("--timeout", type=int, default=60, help="HTTP timeout (s) (default: 60)")
        s.add_argument(
            "--api-key",
            default=None,
            help="NCBI API key (yoksa env: PUBMED_API_KEY veya NCBI_API_KEY)",
        )
        s.add_argument(
            "--email",
            default=None,
            help="NCBI email (yoksa env: PUBMED_EMAIL veya NCBI_EMAIL)",
        )

    # esearch
    s = sub.add_parser("esearch", help="ESearch (query -> id listesi + count)")
    s.add_argument("--db", choices=["pubmed", "pmc"], default="pubmed")
    s.add_argument("--term", required=True, help="NCBI term/query (örn: adapalene[tiab])")
    s.add_argument("--retmax", type=int, default=20)
    s.add_argument("--retstart", type=int, default=0)
    s.add_argument("--usehistory", action="store_true")
    s.add_argument("--sort", default="")
    s.add_argument("--datetype", default="")
    s.add_argument("--mindate", default="")
    s.add_argument("--maxdate", default="")
    s.add_argument(
        "--out",
        default="data/raw/ncbi/esearch.json",
        help="Çıktı JSON yolu (default: data/raw/ncbi/esearch.json)",
    )
    s.add_argument("--filters", default="", help="Log için filtre açıklaması")
    add_common(s)
    s.set_defaults(func=cmd_esearch)

    # esummary
    sm = sub.add_parser("esummary", help="ESummary (id listesi -> JSON summary)")
    sm.add_argument("--db", choices=["pubmed", "pmc"], default="pubmed")
    sm.add_argument("--ids", required=True, help="Comma-separated IDs")
    sm.add_argument(
        "--out",
        default="data/raw/ncbi/esummary.json",
        help="Çıktı JSON yolu (default: data/raw/ncbi/esummary.json)",
    )
    add_common(sm)
    sm.set_defaults(func=cmd_esummary)

    # efetch
    f = sub.add_parser("efetch", help="EFetch (id listesi -> XML/text)")
    f.add_argument("--db", choices=["pubmed", "pmc"], default="pubmed")
    f.add_argument("--ids", required=True, help="Comma-separated IDs")
    f.add_argument("--retmode", default="xml", help="xml|text|... (default: xml)")
    f.add_argument("--rettype", default="", help="Opsiyonel rettype")
    f.add_argument(
        "--out",
        default="data/raw/ncbi/efetch.xml",
        help="Çıktı dosya yolu (default: data/raw/ncbi/efetch.xml)",
    )
    add_common(f)
    f.set_defaults(func=cmd_efetch)

    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
