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


DEFAULT_BASE_URL = "https://api.openalex.org"


@dataclass
class OpenAlexClient:
    """OpenAlex REST API istemcisi.

    Docs: https://docs.openalex.org/

    Notlar:
    - OpenAlex API key opsiyoneldir. Varsa header ile gönderilir.
    - Polite pool için `mailto` parametresi önerilir.
    """

    base_url: str = DEFAULT_BASE_URL
    api_key: Optional[str] = None
    mailto: Optional[str] = None
    timeout_s: int = 60
    user_agent: str = "meta-analysis-repo/1.0 (openalex)"

    def _headers(self) -> dict[str, str]:
        headers = {"User-Agent": self.user_agent}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _with_polite_params(self, params: dict[str, Any]) -> dict[str, Any]:
        if self.mailto and "mailto" not in params:
            params["mailto"] = self.mailto
        # OpenAlex API key kullanımını hem header hem query param olarak destekleyelim
        # (dokümantasyon/dağıtım farklılıkları için daha toleranslı).
        if self.api_key and "api_key" not in params:
            params["api_key"] = self.api_key
        return params

    def works_search(
        self,
        *,
        search: str,
        per_page: int = 25,
        cursor: str = "*",
        sort: str = "",
        filter: str = "",
        select: str = "",
    ) -> dict[str, Any]:
        """/works endpoint'inde full-text search.

        Endpoint: GET /works?search=...&per-page=...&cursor=...
        Cursor paging: https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/paging
        """

        url = f"{self.base_url}/works"
        params: dict[str, Any] = {
            "search": search,
            "per-page": per_page,
            "cursor": cursor,
        }
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if select:
            params["select"] = select

        params = self._with_polite_params(params)
        r = requests.get(url, params=params, headers=self._headers(), timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def work_by_id(self, *, work_id: str) -> dict[str, Any]:
        """Work detaylarını getir.

        work_id örnekleri:
        - OpenAlex ID: W2741809807
        - Tam URL: https://openalex.org/W2741809807
        """

        wid = work_id.strip()

        # Kullanıcı bazen OpenAlex entity URL'si (https://openalex.org/W...) verir.
        # Bu URL çoğu durumda API JSON'u değil HTML döndürebilir.
        # Bu nedenle mümkünse ID'yi çekip API base_url üzerinden çağırıyoruz.
        if wid.startswith("http://") or wid.startswith("https://"):
            if "openalex.org" in wid and "/W" in wid:
                # örn: https://openalex.org/W2105610837
                wid = wid.rstrip("/").split("/")[-1]
            elif "api.openalex.org" in wid:
                url = wid
                params = self._with_polite_params({})
                r = requests.get(url, params=params, headers=self._headers(), timeout=self.timeout_s)
                r.raise_for_status()
                try:
                    return r.json()
                except Exception:
                    detail = (r.text or "")[:500]
                    raise SystemExit(
                        f"OpenAlex work response JSON değil. status={r.status_code}; content-type={r.headers.get('Content-Type','')}; body={detail}"
                    )

        url = f"{self.base_url}/works/{wid}"

        params = self._with_polite_params({})
        r = requests.get(url, params=params, headers=self._headers(), timeout=self.timeout_s)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            detail = (r.text or "")[:500]
            raise SystemExit(
                f"OpenAlex work response JSON değil. status={r.status_code}; content-type={r.headers.get('Content-Type','')}; body={detail}"
            )


def _safe_int(v: Any) -> Optional[int]:
    try:
        return int(v)
    except Exception:
        return None


def _load_openalex_creds(args: argparse.Namespace) -> tuple[Optional[str], Optional[str]]:
    api_key = args.api_key or os.getenv("OPENALEX_API_KEY")
    email = args.email or os.getenv("OPENALEX_EMAIL")
    return api_key, email


def cmd_search(args: argparse.Namespace) -> None:
    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))
    api_key, email = _load_openalex_creds(args)

    client = OpenAlexClient(
        base_url=args.base_url,
        api_key=api_key,
        mailto=email,
        timeout_s=args.timeout,
    )

    payload = client.works_search(
        search=args.search,
        per_page=args.per_page,
        cursor=args.cursor,
        sort=args.sort,
        filter=args.filter,
        select=args.select,
    )

    out_path = Path(args.out)
    write_json(out_path, payload)

    # OpenAlex count schema: meta.count
    count = _safe_int(((payload.get("meta") or {}).get("count")))

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source="OpenAlex",
        interface="API",
        query=args.search,
        filters=args.filter or args.filters or "",
        sort=args.sort or "",
        results_total=count,
        exported_format="json",
        export_scope=f"cursor={args.cursor};per-page={args.per_page}",
        endpoint=f"{client.base_url}/works",
        notes=(
            f"saved={out_path.as_posix()}"
            + (f"; mailto={email}" if email else "")
            + ("; api_key=yes" if api_key else "; api_key=no")
        ),
    )

    print(out_path)


def cmd_work(args: argparse.Namespace) -> None:
    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))
    api_key, email = _load_openalex_creds(args)

    client = OpenAlexClient(
        base_url=args.base_url,
        api_key=api_key,
        mailto=email,
        timeout_s=args.timeout,
    )

    payload = client.work_by_id(work_id=args.id)
    out_path = Path(args.out)
    write_json(out_path, payload)

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source="OpenAlex",
        interface="API",
        query=f"id:{args.id}",
        results_total=1,
        exported_format="json",
        export_scope="single",
        endpoint=(args.id if args.id.startswith("http") else f"{client.base_url}/works/{args.id}"),
        notes=f"saved={out_path.as_posix()}" + (f"; mailto={email}" if email else ""),
    )

    print(out_path)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.openalex",
        description="OpenAlex REST API ile bibliyografik arama yap ve JSON olarak kaydet.",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(s: argparse.ArgumentParser) -> None:
        s.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")
        s.add_argument(
            "--dotenv",
            default=".env",
            help=".env dosya yolu (default: .env). Var ise otomatik okunur.",
        )
        s.add_argument(
            "--base-url",
            default=DEFAULT_BASE_URL,
            help=f"OpenAlex base URL (default: {DEFAULT_BASE_URL})",
        )
        s.add_argument("--timeout", type=int, default=60, help="HTTP timeout (s) (default: 60)")
        s.add_argument(
            "--api-key",
            default=None,
            help="OpenAlex API key (yoksa env: OPENALEX_API_KEY). Opsiyonel.",
        )
        s.add_argument(
            "--email",
            default=None,
            help="Polite pool mailto (yoksa env: OPENALEX_EMAIL). Önerilir.",
        )

    # search
    s = sub.add_parser("search", help="/works search")
    s.add_argument(
        "--search",
        required=True,
        help='OpenAlex works search string. Örn: "adapalene benzoyl peroxide"',
    )
    s.add_argument("--per-page", type=int, default=25, help="Varsayılan: 25")
    s.add_argument(
        "--cursor",
        default="*",
        help="Cursor paging için cursor (default: *). Sonraki sayfayı meta.next_cursor verir.",
    )
    s.add_argument(
        "--filter",
        default="",
        help='OpenAlex filter param (örn: from_publication_date:2010-01-01,to_publication_date:2025-12-31)',
    )
    s.add_argument("--filters", default="", help="Sadece log için filtre açıklaması (opsiyonel)")
    s.add_argument("--sort", default="", help='OpenAlex sort param (örn: cited_by_count:desc)')
    s.add_argument(
        "--select",
        default="",
        help="Dönen alanları daraltmak için select (örn: id,doi,title,publication_year,authorships)",
    )
    s.add_argument(
        "--out",
        default="data/raw/openalex/works_search.json",
        help="Çıktı JSON yolu (default: data/raw/openalex/works_search.json)",
    )
    add_common(s)
    s.set_defaults(func=cmd_search)

    # work
    w = sub.add_parser("work", help="/works/{id} detay")
    w.add_argument(
        "--id",
        required=True,
        help="OpenAlex Work ID (W...) veya tam URL (https://openalex.org/W...) ",
    )
    w.add_argument(
        "--out",
        default="data/raw/openalex/work.json",
        help="Çıktı JSON yolu (default: data/raw/openalex/work.json)",
    )
    add_common(w)
    w.set_defaults(func=cmd_work)

    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
