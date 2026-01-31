from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from ._io import write_json
from .search_log import append_search_log_row
from .wiley_tdm import load_dotenv_if_present

# EMA Public Data Endpoints
EMA_BASE_URL = "https://www.ema.europa.eu"
EMA_MEDICINES_EXCEL_URL = f"{EMA_BASE_URL}/en/documents/report/medicines-output-medicines-report_en.xlsx"
EMA_MEDICINES_JSON_URL = f"{EMA_BASE_URL}/en/documents/report/medicines-output-medicines_json-report_en.json"
EMA_POST_AUTH_JSON_URL = f"{EMA_BASE_URL}/en/documents/report/medicines-output-post_authorisation_json-report_en.json"
EMA_EPAR_DOCS_JSON_URL = f"{EMA_BASE_URL}/en/documents/report/documents-output-epar_documents_json-report_en.json"
EMA_EPAR_BASE_URL = f"{EMA_BASE_URL}/en/medicines/human/EPAR"


def sanitize_filename(s: str) -> str:
    """String'i güvenli dosya adına çevir."""
    s = s.strip()
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    return s[:200]  # Max uzunluk sınırı


@dataclass
class EMAmedicine:
    """Tek bir EMA onaylı ilaç kaydı."""

    name: str
    active_substance: str
    inn: str  # International Non-proprietary Name
    therapeutic_area: str
    authorisation_status: str
    atc_code: str
    marketing_authorisation_holder: str
    marketing_authorisation_date: Optional[str]
    product_number: str
    ema_product_url: str
    epar_url: str
    decision_date: Optional[str]
    revision_number: Optional[str]
    condition: str
    additional_info: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "active_substance": self.active_substance,
            "inn": self.inn,
            "therapeutic_area": self.therapeutic_area,
            "authorisation_status": self.authorisation_status,
            "atc_code": self.atc_code,
            "marketing_authorisation_holder": self.marketing_authorisation_holder,
            "marketing_authorisation_date": self.marketing_authorisation_date,
            "product_number": self.product_number,
            "ema_product_url": self.ema_product_url,
            "epar_url": self.epar_url,
            "decision_date": self.decision_date,
            "revision_number": self.revision_number,
            "condition": self.condition,
            **self.additional_info,
        }


@dataclass
class EMAEparClient:
    """EMA EPAR (European Public Assessment Reports) API istemcisi."""

    timeout_s: int = 120
    user_agent: str = "meta-analysis-repo/1.0 (ema-epar)"
    cache_dir: Path = field(default_factory=lambda: Path("data/cache/ema"))

    def _headers(self) -> Dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            "Accept": "application/json, */*",
            "Accept-Encoding": "gzip, deflate",  # Brotli desteği sorunlu olabilir
        }

    def download_medicines_json(self) -> List[Dict[str, Any]]:
        """EMA'dan tüm onaylı ilaç listesini JSON olarak indir."""

        headers = self._headers()
        headers["Accept"] = "application/json"

        r = requests.get(
            EMA_MEDICINES_JSON_URL,
            headers=headers,
            timeout=self.timeout_s,
        )
        r.raise_for_status()
        return r.json()

    def download_medicines_excel(self, out_path: Path) -> Path:
        """EMA'dan ilaç Excel dosyasını indir."""

        headers = self._headers()
        headers["Accept"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        r = requests.get(
            EMA_MEDICINES_EXCEL_URL,
            headers=headers,
            timeout=self.timeout_s,
            stream=True,
        )
        r.raise_for_status()

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        return out_path

    def download_epar_documents(
        self,
        product_name: str,
        doc_type: str = "all",
        out_dir: Optional[Path] = None,
    ) -> List[Path]:
        """Belirli bir ürünün EPAR dokümanlarını indir.

        doc_type: 'all', 'assessment-report', 'product-information', 'summary'
        """

        # EMA ürün sayfası pattern: /en/medicines/human/EPAR/{product-name}
        # Dokümanlar genelde JSON meta endpoint'inden alınır.

        if out_dir is None:
            out_dir = Path("data/raw/ema/epar") / sanitize_filename(product_name)
        out_dir.mkdir(parents=True, exist_ok=True)

        # İlk olarak ürün detay sayfasını JSON olarak çek
        product_slug = sanitize_filename(product_name.lower())
        product_json_url = f"https://www.ema.europa.eu/en/medicines/human/EPAR/{product_slug}?format=json"

        headers = self._headers()
        headers["Accept"] = "application/json"

        downloaded = []

        try:
            r = requests.get(product_json_url, headers=headers, timeout=self.timeout_s)
            if r.status_code == 200:
                product_data = r.json()
                meta_path = out_dir / f"{product_slug}_meta.json"
                write_json(meta_path, product_data)
                downloaded.append(meta_path)

                # Doküman linklerini çıkar
                docs = self._extract_document_links(product_data, doc_type)
                for doc_url, doc_name in docs:
                    doc_path = self._download_document(doc_url, out_dir, doc_name)
                    if doc_path:
                        downloaded.append(doc_path)
        except requests.RequestException:
            # JSON endpoint çalışmazsa alternatif yol dene
            pass

        return downloaded

    def _extract_document_links(
        self,
        product_data: Dict[str, Any],
        doc_type: str,
    ) -> List[tuple[str, str]]:
        """Ürün JSON'ından doküman linklerini çıkar."""

        docs = []

        # EMA JSON yapısı değişkenlik gösterebilir, yaygın pattern'leri dene
        if "field_ema_web_categories" in product_data:
            for cat in product_data.get("field_ema_web_categories", []):
                if isinstance(cat, dict) and "documents" in cat:
                    for doc in cat["documents"]:
                        url = doc.get("url", "")
                        name = doc.get("name", "") or doc.get("title", "")
                        if url and self._match_doc_type(name, url, doc_type):
                            docs.append((url, name))

        # Alternatif: doğrudan documents array
        for doc in product_data.get("documents", []):
            url = doc.get("url", "") or doc.get("uri", "")
            name = doc.get("name", "") or doc.get("title", "")
            if url and self._match_doc_type(name, url, doc_type):
                docs.append((url, name))

        return docs

    def _match_doc_type(self, name: str, url: str, doc_type: str) -> bool:
        """Doküman tipini filtrele."""
        if doc_type == "all":
            return True

        name_lower = (name or "").lower()
        url_lower = url.lower()

        if doc_type == "assessment-report":
            return any(x in name_lower or x in url_lower for x in ["assessment", "epar", "scientific"])
        elif doc_type == "product-information":
            return any(x in name_lower or x in url_lower for x in ["product-information", "spc", "smpc", "pil"])
        elif doc_type == "summary":
            return any(x in name_lower or x in url_lower for x in ["summary", "overview", "public"])

        return True

    def _download_document(self, url: str, out_dir: Path, doc_name: str) -> Optional[Path]:
        """Tek dokümanı indir."""

        if not url.startswith("http"):
            url = f"https://www.ema.europa.eu{url}"

        try:
            headers = self._headers()
            r = requests.get(url, headers=headers, timeout=self.timeout_s, stream=True)
            r.raise_for_status()

            # Dosya adını belirle
            content_disp = r.headers.get("Content-Disposition", "")
            if "filename=" in content_disp:
                filename = re.search(r'filename="?([^";\n]+)"?', content_disp)
                if filename:
                    doc_name = filename.group(1)

            if not doc_name:
                doc_name = url.split("/")[-1].split("?")[0]

            safe_name = sanitize_filename(doc_name)
            if not safe_name.endswith(".pdf"):
                safe_name += ".pdf"

            out_path = out_dir / safe_name
            with open(out_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            return out_path

        except requests.RequestException:
            return None

    def search_medicines(
        self,
        query: str,
        filters: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        """İlaç listesinde arama yap.

        query: Arama terimi (ürün adı, etken madde, ATC kodu, vb.)
        filters: Opsiyonel filtreler (status, therapeutic_area, etc.)
        """

        # Önce tüm listeyi çek
        all_medicines = self.download_medicines_json()

        query_lower = query.lower()
        results = []

        for med in all_medicines:
            # EMA JSON field adları
            name = str(med.get("medicineName", "") or med.get("name", "")).lower()
            active = str(med.get("activeSubstance", "") or med.get("inn", "")).lower()
            atc = str(med.get("atcCode", "")).lower()
            therapeutic = str(med.get("therapeuticArea", "")).lower()
            condition = str(med.get("condition", "")).lower()
            holder = str(med.get("marketingAuthorisationHolder", "")).lower()

            # Arama eşleşmesi
            if any(query_lower in field for field in [name, active, atc, therapeutic, condition, holder]):
                # Filtre uygula
                if filters:
                    match = True
                    for fkey, fval in filters.items():
                        med_val = str(med.get(fkey, "")).lower()
                        if fval.lower() not in med_val:
                            match = False
                            break
                    if not match:
                        continue

                results.append(med)

        return results


def cmd_list_medicines(args: argparse.Namespace) -> None:
    """Tüm EMA onaylı ilaçları listele (JSON)."""

    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))

    client = EMAEparClient(timeout_s=args.timeout)

    try:
        medicines = client.download_medicines_json()
    except requests.RequestException as e:
        append_search_log_row(
            logs_dir=Path(args.logs_dir),
            source="EMA EPAR",
            interface="API (JSON)",
            query="list-all",
            results_total=0,
            exported_format="json",
            endpoint=EMA_MEDICINES_JSON_URL,
            notes=f"error: {e}",
        )
        raise SystemExit(f"EMA JSON indirme başarısız: {e}")

    out_path = Path(args.out)
    write_json(out_path, medicines)

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source="EMA EPAR",
        interface="API (JSON)",
        query="list-all",
        results_total=len(medicines),
        exported_format="json",
        export_scope="full",
        endpoint=EMA_MEDICINES_JSON_URL,
        notes=f"saved={out_path.as_posix()}",
    )

    print(f"İndirilen ilaç sayısı: {len(medicines)}")
    print(out_path)


def cmd_search(args: argparse.Namespace) -> None:
    """EMA ilaç veritabanında arama yap."""

    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))

    client = EMAEparClient(timeout_s=args.timeout)

    # Filtreleri parse et
    filters = {}
    if args.status:
        filters["authorisationStatus"] = args.status
    if args.therapeutic_area:
        filters["therapeuticArea"] = args.therapeutic_area

    try:
        results = client.search_medicines(args.query, filters=filters or None)
    except requests.RequestException as e:
        append_search_log_row(
            logs_dir=Path(args.logs_dir),
            source="EMA EPAR",
            interface="API (JSON)",
            query=args.query,
            filters=str(filters) if filters else "",
            results_total=0,
            exported_format="json",
            endpoint=EMA_MEDICINES_JSON_URL,
            notes=f"error: {e}",
        )
        raise SystemExit(f"EMA arama başarısız: {e}")

    out_path = Path(args.out)
    write_json(out_path, results)

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source="EMA EPAR",
        interface="API (JSON)",
        query=args.query,
        filters=str(filters) if filters else "",
        results_total=len(results),
        exported_format="json",
        export_scope="search",
        endpoint=EMA_MEDICINES_JSON_URL,
        notes=f"saved={out_path.as_posix()}",
    )

    print(f"Bulunan sonuç sayısı: {len(results)}")
    if results and not args.quiet:
        print("\nİlk 5 sonuç:")
        for med in results[:5]:
            name = med.get("medicineName", med.get("name", "?"))
            active = med.get("activeSubstance", med.get("inn", "?"))
            status = med.get("authorisationStatus", "?")
            print(f"  - {name} ({active}) [{status}]")

    print(out_path)


def cmd_download_excel(args: argparse.Namespace) -> None:
    """EMA ilaç Excel dosyasını indir."""

    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))

    client = EMAEparClient(timeout_s=args.timeout)
    out_path = Path(args.out)

    try:
        saved = client.download_medicines_excel(out_path)
    except requests.RequestException as e:
        append_search_log_row(
            logs_dir=Path(args.logs_dir),
            source="EMA EPAR",
            interface="Web (Excel)",
            query="download-excel",
            results_total=0,
            exported_format="xlsx",
            endpoint=EMA_MEDICINES_EXCEL_URL,
            notes=f"error: {e}",
        )
        raise SystemExit(f"EMA Excel indirme başarısız: {e}")

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source="EMA EPAR",
        interface="Web (Excel)",
        query="download-excel",
        results_total=1,
        exported_format="xlsx",
        export_scope="full",
        endpoint=EMA_MEDICINES_EXCEL_URL,
        notes=f"saved={saved.as_posix()}",
    )

    print(saved)


def cmd_download_epar(args: argparse.Namespace) -> None:
    """Belirli bir ürünün EPAR dokümanlarını indir."""

    load_dotenv_if_present(Path(args.dotenv) if getattr(args, "dotenv", None) else Path(".env"))

    client = EMAEparClient(timeout_s=args.timeout)

    out_dir = Path(args.out_dir) if args.out_dir else None

    try:
        downloaded = client.download_epar_documents(
            product_name=args.product,
            doc_type=args.doc_type,
            out_dir=out_dir,
        )
    except Exception as e:
        append_search_log_row(
            logs_dir=Path(args.logs_dir),
            source="EMA EPAR",
            interface="Web (EPAR)",
            query=f"product:{args.product}",
            filters=f"doc_type={args.doc_type}",
            results_total=0,
            exported_format="pdf",
            endpoint=f"{EMA_EPAR_BASE_URL}/{args.product}",
            notes=f"error: {e}",
        )
        raise SystemExit(f"EPAR doküman indirme başarısız: {e}")

    append_search_log_row(
        logs_dir=Path(args.logs_dir),
        source="EMA EPAR",
        interface="Web (EPAR)",
        query=f"product:{args.product}",
        filters=f"doc_type={args.doc_type}",
        results_total=len(downloaded),
        exported_format="pdf+json",
        export_scope="product",
        endpoint=f"{EMA_EPAR_BASE_URL}/{args.product}",
        notes=f"files={[p.name for p in downloaded]}",
    )

    print(f"İndirilen dosya sayısı: {len(downloaded)}")
    for p in downloaded:
        print(f"  {p}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m tools.ema_epar",
        description="EMA EPAR (European Public Assessment Reports) veritabanına erişim ve indirme aracı.",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    # list-medicines subcommand
    ls = sub.add_parser("list-medicines", help="Tüm EMA onaylı ilaçları listele (JSON)")
    ls.add_argument(
        "--out",
        default="data/raw/ema/medicines_all.json",
        help="Çıktı JSON yolu (default: data/raw/ema/medicines_all.json)",
    )
    ls.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")
    ls.add_argument("--dotenv", default=".env", help=".env dosya yolu")
    ls.add_argument("--timeout", type=int, default=120, help="HTTP timeout (s) (default: 120)")
    ls.set_defaults(func=cmd_list_medicines)

    # search subcommand
    s = sub.add_parser("search", help="EMA ilaç veritabanında arama yap")
    s.add_argument("--query", required=True, help="Arama terimi (ürün adı, etken madde, ATC kodu)")
    s.add_argument("--status", default=None, help="Yetkilendirme durumu filtresi (Authorised, Withdrawn, etc.)")
    s.add_argument("--therapeutic-area", default=None, help="Terapötik alan filtresi")
    s.add_argument(
        "--out",
        default="data/raw/ema/search_results.json",
        help="Çıktı JSON yolu (default: data/raw/ema/search_results.json)",
    )
    s.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")
    s.add_argument("--dotenv", default=".env", help=".env dosya yolu")
    s.add_argument("--timeout", type=int, default=120, help="HTTP timeout (s) (default: 120)")
    s.add_argument("--quiet", action="store_true", help="Sadece dosya yolunu yazdır")
    s.set_defaults(func=cmd_search)

    # download-excel subcommand
    dx = sub.add_parser("download-excel", help="EMA ilaç Excel dosyasını indir")
    dx.add_argument(
        "--out",
        default="data/raw/ema/medicines_report.xlsx",
        help="Çıktı Excel yolu (default: data/raw/ema/medicines_report.xlsx)",
    )
    dx.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")
    dx.add_argument("--dotenv", default=".env", help=".env dosya yolu")
    dx.add_argument("--timeout", type=int, default=120, help="HTTP timeout (s) (default: 120)")
    dx.set_defaults(func=cmd_download_excel)

    # download-epar subcommand
    de = sub.add_parser("download-epar", help="Belirli bir ürünün EPAR dokümanlarını indir")
    de.add_argument("--product", required=True, help="Ürün adı (örn: humira, avastin)")
    de.add_argument(
        "--doc-type",
        choices=["all", "assessment-report", "product-information", "summary"],
        default="all",
        help="İndirilecek doküman tipi (default: all)",
    )
    de.add_argument("--out-dir", default=None, help="Çıktı dizini (default: data/raw/ema/epar/{product})")
    de.add_argument("--logs-dir", default="logs", help="Log dizini (default: logs)")
    de.add_argument("--dotenv", default=".env", help=".env dosya yolu")
    de.add_argument("--timeout", type=int, default=120, help="HTTP timeout (s) (default: 120)")
    de.set_defaults(func=cmd_download_epar)

    return p


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
