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


DEFAULT_BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"


@dataclass
class EuropePmcClient:
    base_url: str = DEFAULT_BASE_URL
    timeout_s: int = 60
    user_agent: str = "meta-analysis-repo/1.0 (europepmc)"

    def search(
        self,
        *,
        query: str,
        format: str = "json",
        page_size: int = 25,
        page: int = 1,
        result_type: str = "lite",
    ) -> dict[str, Any]:
        """Europe PMC search endpoint.

        Docs: https://europepmc.org/RestfulWebService
        Endpoint: GET /search?query=...&format=json&pageSize=25&page=1&resultType=lite
        """

        url = f"{self.base_url}/search"
        params = {
            "query": query,
            "format": format,
            "pageSize": page_size,
            "page": page,
            "resultType": result_type,
        }
        headers = {"User-Agent": self.user_agent}
        r = requests.get(url, params=params, headers=headers, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json() if format == "json" else {"raw": r.text}


def _safe_int(v: Any) -> Optional[int]:
    try:
        return int(v)
    except Exception:
        return None


def cmd_search(args: argparse.Namespace) -> None:
    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))

    # Europe PMC API açık ama “polite” kullanım için mailto/email loglamak faydalı.
    email = args.email or os.getenv("EUROPE_PMC_EMAIL") or os.getenv("NCBI_EMAIL")

    client = EuropePmcClient(base_url=args.base_url, timeout_s=args.timeout)
    payload = client.search(
        query=args.query,
        format="json",
        page_size=args.page_size,
        page=args.page,
        result_type=args.result_type,
    )

    out_path = Path(args.out)
    write_json(out_path, payload)

    # Total hits Europe PMC response: hitCount
    hit_count = _safe_int(payload.get("hitCount"))

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source="Europe PMC",
        interface="API",
        query=args.query,
        filters=args.filters or "",
        sort=args.sort or "",
        results_total=hit_count,
        exported_format="json",
        export_scope=f"page={args.page};pageSize={args.page_size}",
        endpoint=f"{client.base_url}/search",
        notes=(
            f"saved={out_path.as_posix()}"
            + (f"; email={email}" if email else "")
            + f"; resultType={args.result_type}"
        ),
    )

    print(out_path)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.europe_pmc",
        description="Europe PMC REST API ile bibliyografik arama yap ve JSON olarak kaydet.",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Europe PMC search")
    s.add_argument(
        "--query",
        required=True,
        help='Europe PMC query. Örn: TITLE:"adapalene" AND TITLE:"benzoyl peroxide"',
    )
    s.add_argument("--page-size", type=int, default=25, help="Varsayılan: 25")
    s.add_argument("--page", type=int, default=1, help="Varsayılan: 1")
    s.add_argument(
        "--result-type",
        default="lite",
        choices=["lite", "core"],
        help="Varsayılan: lite (core daha zengin alan seti döndürür)",
    )
    s.add_argument(
        "--out",
        default="data/raw/europe_pmc/search.json",
        help="Çıktı JSON yolu (default: data/raw/europe_pmc/search.json)",
    )
    s.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")
    s.add_argument(
        "--dotenv",
        default=".env",
        help=".env dosya yolu (default: .env). Var ise otomatik okunur.",
    )
    s.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Europe PMC base URL (default: {DEFAULT_BASE_URL})",
    )
    s.add_argument("--timeout", type=int, default=60, help="HTTP timeout (s) (default: 60)")

    # Log için opsiyonel metadata
    s.add_argument(
        "--email",
        default=None,
        help="Polite kullanım için email (yoksa env: EUROPE_PMC_EMAIL veya NCBI_EMAIL).",
    )
    s.add_argument("--filters", default="", help="Log için filtre açıklaması (örn. year:2010-2025)")
    s.add_argument("--sort", default="", help="Log için sort açıklaması")

    s.set_defaults(func=cmd_search)
    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
