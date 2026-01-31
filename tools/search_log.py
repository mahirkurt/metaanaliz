from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


SEARCH_LOG_HEADER = [
    "source",
    "interface",
    "datetime_utc",
    "query",
    "filters",
    "sort",
    "results_total",
    "exported_format",
    "export_scope",
    "endpoint",
    "notes",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_search_log_header(path: Path) -> None:
    """search_log.csv yoksa veya boşsa header yazar.

    Not: Repo'da mevcut logs/search_log.csv bir "şablon" gibi tutulabilir.
    Header yoksa ilk satırın header olmasını garanti eder.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        path.write_text(",".join(SEARCH_LOG_HEADER) + "\n", encoding="utf-8")
        return

    first_line = path.open("r", encoding="utf-8").readline().strip("\n")
    if first_line != ",".join(SEARCH_LOG_HEADER):
        # Var olan dosya şablon/başka format olabilir; header eklemek için üstüne yazmıyoruz.
        # Kullanıcı isterse ayrı bir dosya kullanabilir.
        return


def append_search_log_row(
    *,
    logs_dir: Path = Path("logs"),
    source: str,
    interface: str,
    query: str = "",
    filters: str = "",
    sort: str = "",
    results_total: Optional[int] = None,
    exported_format: str = "",
    export_scope: str = "",
    endpoint: str = "",
    notes: str = "",
    datetime_utc: Optional[str] = None,
) -> Path:
    """Repo standardı logs/search_log.csv'e bir satır ekler."""

    path = logs_dir / "search_log.csv"
    ensure_search_log_header(path)

    row = {
        "source": source,
        "interface": interface,
        "datetime_utc": datetime_utc or utc_now_iso(),
        "query": query,
        "filters": filters,
        "sort": sort,
        "results_total": "" if results_total is None else str(results_total),
        "exported_format": exported_format,
        "export_scope": export_scope,
        "endpoint": endpoint,
        "notes": notes,
    }

    # Header var mı kontrol et; yoksa DictWriter header yazmayı denemesin.
    first_line = path.open("r", encoding="utf-8").readline().strip("\n") if path.exists() else ""
    has_header = first_line == ",".join(SEARCH_LOG_HEADER)

    # Eğer dosya newline ile bitmiyorsa, yeni satır ekleyip sonra append et.
    if path.exists() and path.stat().st_size > 0:
        with path.open("rb") as bf:
            bf.seek(-1, 2)
            last_byte = bf.read(1)
        if last_byte not in (b"\n", b"\r"):
            with path.open("a", encoding="utf-8") as f:
                f.write("\n")

    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SEARCH_LOG_HEADER)
        if not has_header and path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)

    return path
