#!/usr/bin/env python3
"""
Anna's Archive API Access Tool
Meta-Analysis projesi için Anna's Archive erişim ve indirme mekanizması

Kullanım:
    python annas_archive_api.py search "meta analysis methods"
    python annas_archive_api.py download BOOK_ID_12345
    python annas_archive_api.py batch-search --terms meta_terms.txt --output results.json
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/annas_archive.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class AnnasArchiveAPI:
    """
    Anna's Archive API erişim sınıfı
    Resmi MCP server ve HTTP API desteği
    """

    def __init__(self, api_key: str = None, download_path: str = "./downloads"):
        """
        API'yi başlat

        Args:
            api_key: Anna's Archive hesap ID'si (varsayılan: 5CxX9WiJ4sjvuXLtRpREdXngDWyd4)
            download_path: İndirme klasörü yolu
        """
        self.api_key = api_key or os.getenv('ANNAS_SECRET_KEY', '5CxX9WiJ4sjvuXLtRpREdXngDWyd4')
        self.base_url = "https://annas-archive.li"
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)

        # Session konfigürasyonu
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'Meta-Analysis-Research/1.0 (https://github.com/mahirkurt/meta-analysis)',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

        # Retry stratejisi
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        logger.info(f"Anna's Archive API initialized with key: {self.api_key[:8]}...")

    def _make_request(self, endpoint: str, method: str = 'GET', params: Dict = None, data: Dict = None) -> Dict:
        """
        HTTP isteği yap ve rate limiting'i handle et
        """
        url = urljoin(self.base_url, endpoint.lstrip('/'))

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            # Rate limit kontrolü
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return self._make_request(endpoint, method, params, data)

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def search_books(self, query: str, lang: str = "en", limit: int = 50,
                    content_type: str = None, year_from: int = None, year_to: int = None) -> Dict:
        """
        Kitap ara - Web scraping kullanarak

        Args:
            query: Arama sorgusu
            lang: Dil (en, tr, de, etc.)
            limit: Maksimum sonuç sayısı
            content_type: İçerik tipi (book, paper, etc.)
            year_from: Başlangıç yılı
            year_to: Bitiş yılı
        """
        try:
            params = {
                'q': quote(query),
                'lang': lang,
                'limit': min(limit, 100),  # Max 100
            }

            if content_type:
                params['content'] = content_type
            if year_from:
                params['year_from'] = year_from
            if year_to:
                params['year_to'] = year_to

            url = urljoin(self.base_url, 'search')
            logger.info(f"Searching for: {query} (limit: {limit})")

            response = self.session.get(url, params=params)
            response.raise_for_status()

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all MD5 links (book identifiers)
            md5_links = soup.find_all('a', href=lambda x: x and '/md5/' in x)

            books = []
            for link in md5_links[:limit]:
                href = link.get('href')
                if href and '/md5/' in href:
                    md5 = href.split('/md5/')[-1].split('/')[0]
                    title = link.get_text(strip=True)

                    # Try to get additional info from parent elements
                    parent = link.parent
                    description = ""
                    author = ""
                    year = ""
                    size = ""

                    # Look for additional info in sibling elements
                    for sibling in parent.find_next_siblings():
                        sibling_text = sibling.get_text(strip=True)
                        if sibling_text and len(sibling_text) > 10:
                            if not description and 'description' not in sibling_text.lower():
                                description = sibling_text[:200]  # Limit description length
                            break

                    book_info = {
                        'id': md5,
                        'title': title or f"Book {md5[:8]}",
                        'md5': md5,
                        'description': description,
                        'author': author,
                        'year': year,
                        'size': size,
                        'url': urljoin(self.base_url, href)
                    }
                    books.append(book_info)

            result = {
                'query': query,
                'total': len(books),
                'books': books
            }

            logger.info(f"Found {len(books)} books")
            return result

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    def get_book_details(self, book_id: str) -> Dict:
        """
        Kitap detaylarını al - Web scraping kullanarak
        """
        logger.info(f"Getting details for book: {book_id}")

        try:
            url = f"{self.base_url}/md5/{book_id}"
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract book information
            title = ""
            author = ""
            description = ""
            year = ""
            size = ""
            language = ""
            extension = ""

            # Try to find title
            title_elem = soup.find('title')
            if title_elem:
                title = title_elem.get_text(strip=True).replace(" - Anna's Archive", "")

            # Look for metadata in the page
            metadata_divs = soup.find_all('div', class_=lambda x: x and ('metadata' in x or 'info' in x))
            for div in metadata_divs:
                text = div.get_text(strip=True)
                if 'Author' in text or 'author' in text:
                    author = text.split(':')[-1].strip() if ':' in text else text
                elif 'Year' in text or 'year' in text:
                    year = text.split(':')[-1].strip() if ':' in text else text
                elif 'Language' in text or 'language' in text:
                    language = text.split(':')[-1].strip() if ':' in text else text
                elif 'Size' in text or 'size' in text:
                    size = text.split(':')[-1].strip() if ':' in text else text
                elif 'Extension' in text or 'extension' in text:
                    extension = text.split(':')[-1].strip() if ':' in text else text

            # Look for description
            desc_elem = soup.find('meta', attrs={'name': 'description'})
            if desc_elem:
                description = desc_elem.get('content', '')

            return {
                'id': book_id,
                'title': title,
                'author': author,
                'description': description,
                'year': year,
                'language': language,
                'size': size,
                'extension': extension,
                'url': url
            }

        except Exception as e:
            logger.error(f"Failed to get book details: {e}")
            raise

    def get_download_info(self, book_id: str) -> Dict:
        """
        İndirme bilgilerini al - Yeni API kullanarak
        """
        logger.info(f"Getting download info for: {book_id}")

        # book_id should be MD5 hash
        params = {
            'md5': book_id,
            'key': self.api_key
        }

        try:
            response = self.session.get(f"{self.base_url}/dyn/api/fast_download.json", params=params)
            response.raise_for_status()

            result = response.json()
            if result.get('download_url'):
                return {
                    'download_url': result['download_url'],
                    'account_fast_download_info': result.get('account_fast_download_info', {})
                }
            else:
                error_msg = result.get('error', 'Unknown error')
                raise ValueError(f"Download info error: {error_msg}")

        except requests.exceptions.JSONDecodeError:
            logger.error(f"Invalid JSON response for book {book_id}")
            raise ValueError(f"API returned invalid JSON for book {book_id}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def download_book(self, book_id: str, filename: str = None) -> Path:
        """
        Kitabı indir

        Args:
            book_id: Kitap ID'si
            filename: Özel dosya adı (varsayılan: book_id.pdf)

        Returns:
            İndirilen dosya yolu
        """
        try:
            # İndirme bilgilerini al
            download_info = self.get_download_info(book_id)
            download_url = download_info.get('download_url')

            if not download_url:
                raise ValueError(f"No download URL found for book {book_id}")

            # Dosya adını belirle
            if not filename:
                filename = f"{book_id}.pdf"
            filepath = self.download_path / filename

            logger.info(f"Downloading {book_id} to {filepath}")

            # Dosyayı indir
            with self.session.get(download_url, stream=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))

                with open(filepath, 'wb') as f:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

                            # Progress göster (her 1MB'da bir)
                            if total_size > 0 and downloaded % (1024 * 1024) == 0:
                                progress = (downloaded / total_size) * 100
                                logger.info(".1f")

            logger.info(f"Download completed: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Download failed for {book_id}: {e}")
            raise

    def search_meta_analysis_resources(self, query_terms: List[str], limit_per_term: int = 25) -> List[Dict]:
        """
        Meta-analysis kaynaklarını ara

        Args:
            query_terms: Arama terimleri listesi
            limit_per_term: Her terim için maksimum sonuç

        Returns:
            Filtrelenmiş sonuçlar listesi
        """
        all_results = []
        meta_keywords = [
            'meta-analysis', 'meta analysis', 'systematic review',
            'cochrane', 'randomized controlled trial', 'clinical trial',
            'evidence synthesis', 'forest plot', 'heterogeneity',
            'publication bias', 'sensitivity analysis'
        ]

        for term in query_terms:
            logger.info(f"Searching meta-analysis resources for: {term}")
            results = self.search_books(term, limit=limit_per_term)

            for book in results.get('books', []):
                title = book.get('title', '').lower()
                description = book.get('description', '').lower()

                # Meta-analysis ile ilgili filtrele
                if any(keyword in title or keyword in description for keyword in meta_keywords):
                    if book not in all_results:  # Duplikat kontrolü
                        all_results.append(book)

        logger.info(f"Found {len(all_results)} meta-analysis resources")
        return all_results

    def batch_download(self, book_ids: List[str], delay: float = 1.0) -> List[Path]:
        """
        Birden fazla kitabı indir

        Args:
            book_ids: Kitap ID'leri listesi
            delay: İndirmeler arası bekleme süresi (saniye)

        Returns:
            İndirilen dosyaların yolları
        """
        downloaded_files = []

        for i, book_id in enumerate(book_ids, 1):
            logger.info(f"Downloading {i}/{len(book_ids)}: {book_id}")

            try:
                filepath = self.download_book(book_id)
                downloaded_files.append(filepath)
            except Exception as e:
                logger.error(f"Failed to download {book_id}: {e}")

            # Rate limiting için bekle
            if i < len(book_ids):
                time.sleep(delay)

        return downloaded_files


def main():
    """Komut satırı arayüzü"""
    parser = argparse.ArgumentParser(description="Anna's Archive API Tool")
    parser.add_argument('command', choices=['search', 'download', 'details', 'batch-search', 'batch-download'],
                       help='Komut')
    parser.add_argument('query', nargs='?', help='Arama sorgusu veya kitap ID\'si')
    parser.add_argument('--limit', type=int, default=50, help='Maksimum sonuç sayısı')
    parser.add_argument('--lang', default='en', help='Dil')
    parser.add_argument('--output', '-o', help='Çıktı dosyası')
    parser.add_argument('--download-path', default='./downloads', help='İndirme klasörü')
    parser.add_argument('--terms-file', help='Arama terimleri dosyası (batch-search için)')
    parser.add_argument('--ids-file', help='Kitap ID\'leri dosyası (batch-download için)')
    parser.add_argument('--delay', type=float, default=1.0, help='İndirmeler arası bekleme süresi')
    parser.add_argument('--api-key', help='API anahtarı (varsayılan: env ANNAS_SECRET_KEY)')

    args = parser.parse_args()

    # API'yi başlat
    api = AnnasArchiveAPI(api_key=args.api_key, download_path=args.download_path)

    try:
        if args.command == 'search':
            if not args.query:
                parser.error("Search komutu için sorgu gerekli")
            results = api.search_books(args.query, lang=args.lang, limit=args.limit)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"Sonuçlar kaydedildi: {args.output}")
            else:
                print(json.dumps(results, indent=2, ensure_ascii=False))

        elif args.command == 'details':
            if not args.query:
                parser.error("Details komutu için kitap ID gerekli")
            details = api.get_book_details(args.query)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(details, f, indent=2, ensure_ascii=False)
                print(f"Detaylar kaydedildi: {args.output}")
            else:
                print(json.dumps(details, indent=2, ensure_ascii=False))

        elif args.command == 'download':
            if not args.query:
                parser.error("Download komutu için kitap ID gerekli")
            filepath = api.download_book(args.query)
            print(f"İndirildi: {filepath}")

        elif args.command == 'batch-search':
            if args.terms_file:
                with open(args.terms_file, 'r', encoding='utf-8') as f:
                    terms = [line.strip() for line in f if line.strip()]
            elif args.query:
                terms = [args.query]
            else:
                parser.error("Batch-search için terms-file veya query gerekli")

            results = api.search_meta_analysis_resources(terms, limit_per_term=args.limit)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"Toplu arama sonuçları kaydedildi: {args.output}")
            else:
                print(json.dumps(results, indent=2, ensure_ascii=False))

        elif args.command == 'batch-download':
            if args.ids_file:
                with open(args.ids_file, 'r', encoding='utf-8') as f:
                    book_ids = [line.strip() for line in f if line.strip()]
            elif args.query:
                book_ids = [args.query]
            else:
                parser.error("Batch-download için ids-file veya query gerekli")

            downloaded = api.batch_download(book_ids, delay=args.delay)
            print(f"Toplam {len(downloaded)} dosya indirildi")

    except Exception as e:
        logger.error(f"Komut başarısız: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()