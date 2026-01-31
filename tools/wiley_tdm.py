from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests

from ._io import atomic_write_text
from .search_log import append_search_log_row


DEFAULT_BASE_URL = "https://api.wiley.com/onlinelibrary/tdm/v1"


def load_dotenv_if_present(dotenv_path: Path = Path(".env")) -> None:
    """En minimal .env loader.

    Bu repo'da CLI'lerin çoğu doğrudan shell env ile çalışır. Ancak kullanıcı deneyimini
    iyileştirmek için, eğer çalışma dizininde .env varsa `KEY=VALUE` satırlarını
    process env'e set eder (var olan env değerlerini override etmez).
    """

    if not dotenv_path.exists():
        return
    try:
        for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except Exception:
        # .env okunamadıysa sessiz geç.
        return


def sanitize_filename(s: str) -> str:
    # DOI gibi string'leri güvenli dosya adına çevir.
    s = s.strip()
    s = s.replace("/", "_")
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    return s


@dataclass
class WileyTdmClient:
    token: str
    base_url: str = DEFAULT_BASE_URL
    timeout_s: int = 60

    def _headers(self) -> dict:
        return {
            "Wiley-TDM-Client-Token": self.token,
            # Bazı edge-case'lerde UA faydalı olabilir.
            "User-Agent": "meta-analysis-repo/1.0 (wiley-tdm)",
        }

    def download_article(self, doi: str, accept: str) -> requests.Response:
        url = f"{self.base_url}/articles/{doi}"
        headers = self._headers()
        headers["Accept"] = accept
        return requests.get(url, headers=headers, timeout=self.timeout_s)


def cmd_download(args: argparse.Namespace) -> None:
    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))
    token = args.token or os.getenv("WILEY_TDM_CLIENT_TOKEN") or os.getenv("WILEY_TDM_TOKEN")
    if not token:
        raise SystemExit(
            "Wiley TDM token bulunamadı. --token verin veya .env/.shell içinde WILEY_TDM_CLIENT_TOKEN ayarlayın."
        )

    client = WileyTdmClient(token=token, base_url=args.base_url, timeout_s=args.timeout)
    doi = args.doi.strip()

    # Varsayılan çıktı dizini repo standardı
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # PDF öncelikli; istenirse HTML de alınabilir.
    accept = "application/pdf" if args.format == "pdf" else "text/html"
    resp = client.download_article(doi, accept=accept)

    if args.dry_run:
        print(f"GET {client.base_url}/articles/{doi} -> status={resp.status_code}")
        print(f"Content-Type: {resp.headers.get('Content-Type','')}")
        # Logla (dry-run bile olsa bir deneme kaydı)
        append_search_log_row(
            logs_dir=Path(args.logs_dir),
            source="Wiley TDM",
            interface="API",
            query=f"doi:{doi}",
            filters="",
            sort="",
            results_total=1 if resp.status_code == 200 else 0,
            exported_format=args.format,
            export_scope="single",
            endpoint=f"{client.base_url}/articles/{doi}",
            notes=f"dry_run=yes; status={resp.status_code}",
        )
        return

    if resp.status_code != 200:
        # Hata gövdesi çoğu zaman text
        detail = resp.text[:500] if resp.text else ""
        append_search_log_row(
            logs_dir=Path(args.logs_dir),
            source="Wiley TDM",
            interface="API",
            query=f"doi:{doi}",
            results_total=0,
            exported_format=args.format,
            export_scope="single",
            endpoint=f"{client.base_url}/articles/{doi}",
            notes=f"status={resp.status_code}; error={detail}",
        )
        raise SystemExit(f"Wiley TDM indirme başarısız: HTTP {resp.status_code}. {detail}")

    ext = "pdf" if args.format == "pdf" else "html"
    out_path = out_dir / f"{sanitize_filename(doi)}.{ext}"
    out_path.write_bytes(resp.content)

    # Basit bir metadata sidecar (headers)
    if args.write_meta:
        meta = {
            "doi": doi,
            "endpoint": f"{client.base_url}/articles/{doi}",
            "status": resp.status_code,
            "content_type": resp.headers.get("Content-Type", ""),
            "content_length": resp.headers.get("Content-Length", ""),
        }
        meta_path = out_dir / f"{sanitize_filename(doi)}.{ext}.meta.json"
        atomic_write_text(meta_path, __import__("json").dumps(meta, ensure_ascii=False, indent=2) + "\n")

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source="Wiley TDM",
        interface="API",
        query=f"doi:{doi}",
        results_total=1,
        exported_format=args.format,
        export_scope="single",
        endpoint=f"{client.base_url}/articles/{doi}",
        notes=f"saved={out_path.as_posix()}"
        + ("; meta_json=yes" if args.write_meta else ""),
    )

    print(out_path)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.wiley_tdm",
        description="Wiley Text and Data Mining (TDM) API ile DOI üzerinden tam metin indir.",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("download", help="DOI ile makale indir (PDF/HTML)")
    d.add_argument("--doi", required=True, help="Örn: 10.1002/net.22207")
    d.add_argument(
        "--format",
        choices=["pdf", "html"],
        default="pdf",
        help="Varsayılan: pdf",
    )
    d.add_argument(
        "--out-dir",
        default="data/raw/pdfs/paper_search",
        help="Çıktı dizini (default: data/raw/pdfs/paper_search)",
    )
    d.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")
    d.add_argument(
        "--dotenv",
        default=".env",
        help=".env dosya yolu (default: .env). Var ise otomatik okunur.",
    )
    d.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Wiley TDM base URL (default: {DEFAULT_BASE_URL})",
    )
    d.add_argument("--timeout", type=int, default=60, help="HTTP timeout (s) (default: 60)")
    d.add_argument("--token", default=None, help="Token (yoksa env: WILEY_TDM_CLIENT_TOKEN)")
    d.add_argument("--dry-run", action="store_true", help="Dosya yazmadan sadece istek sonucu yazdır")
    d.add_argument(
        "--write-meta",
        action="store_true",
        help="Yanına basit bir .meta.json yaz (headers/endpoint)",
    )
    d.set_defaults(func=cmd_download)

    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
