# TEKNIK TALIMATNAME (Meta-Analysis Workspace)

> Bu doküman, aşağıdaki 4 dokümanın **tam kapsam ile** tek bir teknik talimatname altında birleştirilmiş hâlidir ve bu repodaki “meta-analiz” iş akışında **yeniden üretilebilirlik (PRISMA-S)**, **denetlenebilirlik (audit trail)**, **idempotent çıktı üretimi**, **MCP tabanlı agent kullanım pratikleri** ve **çoklu veri kaynağına programatik erişim** için operasyonel referans sağlar.
>
> Birleştirilen kaynak dokümanlar:
> 1) `AI-AGENT-VERI-CEKME-KILAVUZU.md`
> 2) `ARAMA-VERI-KAYNAKLARI-VE-API-ERISIMI.md`
> 3) `MCP-KULLANIM-DOKUMANTASYONU.md`
> 4) `RUNBOOK-MCP-STRATEJI-1.md`

---

## 0) Amaç, kapsam ve repo standardı

### 0.1 Amaç
Bu talimatnamenin amacı; bu repo içinde bir AI agent’ın (Cline/VS Code/MCP dahil) aşağıdaki işleri **standart**, **tutarlı** ve **kanıtlanabilir** şekilde yapmasını sağlamaktır:

- Sistematik literatür taraması (çoklu veri kaynağı)
- PRISMA-S uyumlu arama loglama
- Dedup / screening / audit log üretimi
- Full-text bulma/indirme ve DOI/PMID zenginleştirme
- MCP server’ları (Knowledgebase, Skill-to-MCP, Paper-Search) ile çalışma

### 0.2 Repo CLI standardı

Bu repo’da yerel (repo-local) CLI kalıbı:

```bash
python -m tools.<modül> <subcommand> [args]
```

Beklenen davranış:

- Çıktılar `data/raw/...` veya ilgili hedef dizinlere yazılır.
- Her “arama/çekim” çalıştırması `logs/search_log.csv` içine PRISMA-S uyumlu bir satır ekler.
- Aynı komut aynı parametrelerle tekrar çalıştırıldığında **idempotent** olacak şekilde aynı `--out` hedefine yazabilir.

---

## 1) Temel prensipler (reprodüksiyon, idempotency, güvenlik)

### 1.1 Yeniden üretilebilirlik (PRISMA-S)

- Her arama çalıştırması:
  - ham query string,
  - tarih/zaman (UTC),
  - filtre/sort,
  - toplam sonuç sayısı (mümkünse)
  ile loglanmalıdır.
- Bu repo’da amaç, aramanın “kanıtını” `logs/search_log.csv` ve ilgili çıktı dosyaları ile sağlayabilmektir.

### 1.2 İdempotent çıktı (Idempotent)

- Aynı sorgu, aynı parametrelerle tekrar koşulduğunda çıktılar **aynı path**’e yazılabilir.
- Versiyonlama gerekiyorsa şu yaklaşımlar tercih edilir:
  - `data/raw/<source>/runs/<YYYY-MM-DD>/...`
  - veya dosya adında tarih/saat

### 1.3 Güvenlik / etik / ToS

- API key/token’lar **hard-code edilmez**.
- Tercih sırası:
  1) `.env` (lokal geliştirme)
  2) CI/runner secrets (GitHub Actions vb.)
- ToS/etik/hukuki riskli scraping yaklaşımları önerilmez.

### 1.4 Nazik kullanım (rate limit)

- 429 durumunda retry/backoff uygulanmalı.
- “Polite pool” için email öneren servislerde email sağlanmalı (Unpaywall’da zorunlu).

---

## 2) Minimum konfigürasyon (.env)

Bu repo çoğu CLI’da `.env` dosyasını otomatik yükler.

Önerilen minimum değişkenler:

```dotenv
# “Polite pool” ve zorunlu email parametreleri için
EUROPE_PMC_EMAIL=you@example.com
OPENALEX_EMAIL=you@example.com
CROSSREF_MAILTO=you@example.com
UNPAYWALL_EMAIL=you@example.com

# Opsiyonel API key’ler
SEMANTIC_SCHOLAR_API_KEY=
OPENFDA_API_KEY=
SERP_API_KEY=

# Kurumsal / abonelik tabanlı servisler (varsa)
ELSEVIER_API_KEY=
ELSEVIER_INSTTOKEN=
WILEY_TDM_CLIENT_TOKEN=

# Anna's Archive erişimi (kullanım politikalarını/ToS’u ayrıca doğrulayın)
ANNAS_SECRET_KEY=
```

Notlar:

- NCBI için repo bazı CLI’lar `PUBMED_API_KEY/NCBI_API_KEY` ve `PUBMED_EMAIL/NCBI_EMAIL` gibi adları da arayabilir.
- `CROSSREF_MAILTO` yoksa CLI bazı durumlarda sırayla `EUROPE_PMC_EMAIL` → `OPENALEX_EMAIL` → `PUBMED_EMAIL` gibi alanlardan email devralabilir.

---

## 3) Agent iş akışı (yüksek seviye uçtan uca)

### 3.1 PICO → Query üretimi

1) PICO (Population/Intervention/Comparator/Outcome) unsurlarını çıkar.
2) Her veri kaynağı için **kaynağa özgü query sentaksı** üret:
   - PubMed: `[tiab]`, MeSH
   - Scopus: `TITLE-ABS-KEY(...)`
   - Europe PMC: `TITLE:"..."` vb.
3) Query’leri (tercihen) dosyada sakla:
   - `screening/search_strategies/<source>_<topic>.txt`

### 3.2 Discovery araması (çoklu kaynak)

Minimum öneri:

- PubMed (NCBI)
- Europe PMC
- (varsa) Scopus/Embase/WoS
- OpenAlex
- Semantic Scholar (yardımcı)

### 3.3 Kayıt taraması (trial registries)

- ClinicalTrials.gov (API v2)
- (varsa) ICTRP / EU CTR / CTIS (çoğu zaman UI)

### 3.4 Regülatif tarama

- openFDA (drug label vb.)
- EMA EPAR dataset (medicines list + arama)

### 3.5 Zenginleştirme / full-text erişim

- Crossref (DOI doğrulama / metadata)
- Unpaywall (OA lokasyonları)
- OpenCitations (atıf verileri)
- (varsa) Wiley TDM (DOI bilerek tam metin)

### 3.6 Dedup + Screening + Audit

- Kayıt birleştirme/dedup (skill veya harici ref manager)
- Screening kararlarını standart formatta logla
- Audit log’a kanıt (evidence pointer) ekle

---

## 4) Repo CLI “altın komutlar” (kopyala-çalıştır)

> Not: Komutlar `logs/search_log.csv` satırı üretir. Çıktılar genelde `data/raw/...` altına yazılır.

### 4.1 PubMed (NCBI E-utilities)

```bash
python -m tools.ncbi_eutils esearch \
  --db pubmed \
  --term '(adapalene[tiab]) AND (benzoyl peroxide[tiab])' \
  --retmax 20 \
  --out data/raw/ncbi/pubmed_esearch.json
```

### 4.2 Europe PMC

```bash
python -m tools.europe_pmc search \
  --query 'TITLE:"adapalene" AND TITLE:"benzoyl peroxide"' \
  --page-size 25 \
  --page 1 \
  --result-type lite \
  --out data/raw/europe_pmc/adapalene_bpo_search.json
```

### 4.3 OpenAlex

```bash
python -m tools.openalex search \
  --search 'adapalene benzoyl peroxide' \
  --per-page 25 \
  --select 'id,doi,title,publication_year,authorships' \
  --out data/raw/openalex/works_search.json
```

### 4.4 Semantic Scholar

```bash
python -m tools.semantic_scholar search \
  --query 'adapalene benzoyl peroxide 5%' \
  --limit 5 \
  --out data/raw/semantic_scholar/search.json
```

### 4.5 Google Scholar (SerpAPI)

> Google Scholar için resmî API yoktur; otomasyon ToS/etik riskleri taşır. SerpAPI kullanıyorsanız key gereklidir.

```bash
python -m tools.serpapi_scholar search \
  --query 'adapalene benzoyl peroxide 5%' \
  --num 20 \
  --as-ylo 2018 \
  --out data/raw/serpapi/google_scholar_search.json
```

### 4.6 ClinicalTrials.gov (API v2)

```bash
python -m tools.clinicaltrials_gov search \
  --query-term 'acne adapalene benzoyl peroxide' \
  --page-size 10 \
  --out data/raw/clinicaltrials_gov/studies.json
```

Pagination:

```bash
# 1. çağrının çıktısındaki nextPageToken değerini kopyalayın
python -m tools.clinicaltrials_gov search \
  --query-term 'acne adapalene benzoyl peroxide' \
  --page-size 10 \
  --page-token '<nextPageToken>' \
  --out data/raw/clinicaltrials_gov/studies_page2.json
```

### 4.7 openFDA

```bash
python -m tools.openfda drug-label-search \
  --search 'adapalene' \
  --limit 5 \
  --out data/raw/openfda/drug_label.json
```

### 4.8 EMA EPAR dataset

```bash
python -m tools.ema_epar search \
  --query 'adapalene' \
  --out data/raw/ema/adapalene_search.json
```

### 4.9 Anna's Archive

```bash
# Kitap arama
python -m tools.annas_archive_api search "meta analysis methods" \
  --limit 25 \
  --lang en \
  --output data/raw/annas_archive/search_results.json

# Kitap detayları
python -m tools.annas_archive_api details BOOK_MD5_ID \
  --output data/raw/annas_archive/book_details.json

# Kitap indirme
python -m tools.annas_archive_api download BOOK_MD5_ID \
  --download-path downloads/
```

### 4.10 Crossref (DOI metadata)

```bash
python -m tools.crossref search \
  --query 'adapalene benzoyl peroxide' \
  --rows 25 \
  --out data/raw/crossref/search_results.json
```

### 4.11 Unpaywall (OA link)

```bash
python -m tools.unpaywall check \
  --doi '10.1016/j.jaad.2019.07.074' \
  --out data/raw/unpaywall/doi_check.json
```

### 4.12 OpenCitations

```bash
python -m tools.opencitations citations \
  --doi '10.1016/j.jaad.2019.07.074' \
  --out data/raw/opencitations/citations.json
```

### 4.13 Wiley TDM (tam metin)

```bash
python -m tools.wiley_tdm download \
  --doi '10.1111/jdv.12345' \
  --out downloads/wiley_paper.pdf
```

### 4.14 Elsevier/Scopus

```bash
python -m tools.elsevier scopus-search \
  --query 'TITLE-ABS-KEY(adapalene AND "benzoyl peroxide")' \
  --count 25 \
  --out data/raw/elsevier/scopus_search.json
```

### 4.15 DOI Enrichment

```bash
python -m tools.doi_enrichment enrich \
  --doi '10.1016/j.jaad.2019.07.074' \
  --out data/raw/doi_enrichment/enriched_metadata.json
```

---

## 5) Veri kaynakları ve programatik erişim rehberi (UI/API/abonelik)

Bu bölüm; hangi kaynaklara nasıl erişileceğini ve proje içinde nasıl “reprodüksiyon + loglama” ile kullanılacağını özetler.

### 5.1 Hızlı özet tablo

| Kaynak | Tür | Programatik erişim | Lisans/erişim notu | Resmî dokümantasyon |
|---|---|---|---|---|
| PubMed/MEDLINE (NLM/NCBI) | Bibliyografik | Var (E-utilities) | Ücretsiz; rate limit | https://www.ncbi.nlm.nih.gov/books/NBK25497/ |
| PubMed Central (PMC) | Tam metin (OA ağırlıklı) | Var (E-utilities, pmc db) | Ücretsiz; kapsam sınırlı | https://www.ncbi.nlm.nih.gov/home/develop/api/ |
| Europe PMC | Bibliyografik + tam metin zenginliği | Var (REST) | Ücretsiz | https://europepmc.org/RestfulWebService |
| Embase | Bibliyografik (Emtree) | Kurumsal (Elsevier) | Abonelik/izin | https://dev.elsevier.com/embase_apis.html |
| Cochrane CENTRAL | Klinik çalışma kayıtları | UI + (kısıtlı) API | Erişim/tokens | https://test-api.cochrane.org/api-docs/index.html |
| Scopus | Bibliyografik + atıf | Var (Elsevier) | Abonelik + APIKey (+InstToken) | https://dev.elsevier.com/ |
| Web of Science | Bibliyografik + atıf | Var (Clarivate) | Abonelik + izin | https://developer.clarivate.com/apis/wos |
| Semantic Scholar | Açık akademik grafik | Var | Ücretsiz; rate limit | https://api.semanticscholar.org/api-docs/ |
| Google Scholar | Arama motoru | Resmî API yok | ToS riskleri | (resmî API yok) |
| OpenAlex | Açık bibliyografik + atıf | Var | Ücretsiz; email önerilir | https://docs.openalex.org/ |
| Crossref | DOI/metadata | Var | Ücretsiz; mailto önerilir | https://www.crossref.org/documentation/retrieve-metadata/rest-api/ |
| Unpaywall | OA lokasyon | Var | Ücretsiz; email zorunlu | https://unpaywall.org/products/api |
| OpenCitations | Atıf grafiği | Var | Ücretsiz | https://api.opencitations.net/ |
| ClinicalTrials.gov | Kayıt | Var (API v2) | Ücretsiz | https://clinicaltrials.gov/data-api/api |
| FDA (openFDA) | Regülatif | Var | Ücretsiz; rate limit | https://open.fda.gov/apis/ |
| EMA EPAR / EU Open Data | Regülatif | Dataset/indirme | API her zaman yok | https://data.europa.eu/data/datasets/epar-human-medicines |
| Wiley TDM | Tam metin | Var (TDM) | Token + ToS | https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining |

### 5.2 Repo-local araçların durum matrisi (entegrasyon + smoke-test)

| Kaynak | Repo-local CLI | Smoke test (repo içinde) | Kanıt/Not |
|---|---:|---:|---|
| PubMed/PMC (NCBI) | ✅ `tools/ncbi_eutils.py` | ✅ | `data/raw/ncbi/*` ve log satırları |
| Europe PMC | ✅ `tools/europe_pmc.py` | ✅ | `data/raw/europe_pmc/*` |
| OpenAlex | ✅ `tools/openalex.py` | ✅ | `data/raw/openalex/*` |
| Wiley TDM | ✅ `tools/wiley_tdm.py` | ✅ (credential varsa) | `data/raw/pdfs/paper_search/*` |
| Crossref | ✅ `tools/crossref.py` | ✅ | `data/raw/crossref/*` |
| Unpaywall | ✅ `tools/unpaywall.py` | ✅ | `data/raw/unpaywall/*` |
| OpenCitations | ✅ `tools/opencitations.py` | ✅ | `data/raw/opencitations/*` |
| DOI enrichment | ✅ `tools/doi_enrichment.py` | ✅ | `data/raw/doi_enrichment/*` |
| Anna's Archive | ✅ `tools/annas_archive_api.py` | ✅ | `data/raw/annas_archive/*` |
| Elsevier (Scopus/Embase) | ✅ `tools/elsevier.py` | ⚠️ kurumsal erişime bağlı | Token yoksa graceful-degrade |
| Cochrane API | (swagger var) | ⚠️ token gerekli | Bearer token |
| Web of Science | (CLI yok) | ⚠️ abonelik/izin | Clarivate credentials |

### 5.3 PubMed/NCBI — operasyonel notlar

- API key yoksa ~3 req/s; key ile ~10 req/s.
- Yüksek hacimde: `usehistory=y` + WebEnv/query_key tercih edin.

### 5.4 Europe PMC — polite email

`.env`:

```dotenv
EUROPE_PMC_EMAIL=you@example.com
```

### 5.5 Google Scholar — uyarı

- Resmî API yok.
- Otomasyon ToS/robots/IP kısıtları ve hukuki risklere yol açabilir.
- Bu nedenle “temel kaynak” olarak değil, yardımcı/manuel + loglanmış kullanım önerilir.

### 5.6 Elsevier/Scopus — search tips (phrase/proximity)

Kaynak: https://dev.elsevier.com/sc_search_tips.html

- **Exact phrase**: `{benzoyl peroxide}`
- **Loose phrase**: `"benzoyl peroxide"`
- **Proximity**: `W/n`, `PRE/n`

Örnek:

```bash
curl -sG 'https://api.elsevier.com/content/search/scopus' \
  -H 'Accept: application/json' \
  -H 'X-ELS-APIKey: ${ELSEVIER_API_KEY}' \
  --data-urlencode 'query=TITLE-ABS-KEY(adapalene AND benzoyl W/1 peroxide)'
```

### 5.7 Cochrane API vs Wiley TDM ayrımı

- Cochrane test API endpoint’leri genellikle `Authorization: Bearer <access_token>` ister.
- Wiley TDM ise `Wiley-TDM-Client-Token: <token>` header’ı ile çalışır.

---

## 6) PRISMA-S loglama standardı (`logs/search_log.csv`)

Bu repo’daki CLI’lar, her çalıştırmada `logs/search_log.csv` içine aşağıdaki alanları (mümkün olduğu ölçüde) yazar:

- `source` (örn. PubMed, Europe PMC, OpenAlex, Semantic Scholar)
- `interface` (API/UI)
- `datetime_utc`
- `query` (ham string)
- `filters`, `sort`
- `results_total`
- `exported_format` (json/xml/pdf/...)
- `export_scope` (örn. `offset=0;limit=20`)
- `endpoint`
- `notes` (çıktı yolu, retry/backoff, credential durumu)

Agent kontrol listesi:

1) Çıktı dosyası oluştu mu?
2) Log satırı eklendi mi?
3) `query` ve `endpoint` beklenen mi?
4) Hata varsa `notes` içinde yeterli detay var mı?

---

## 7) MCP (Cline/VS Code) — Strateji-1 kurulum ve kullanım

Bu bölüm, `.vscode/mcp.json` ile tanımlı MCP server’larının kullanımını standartlaştırır.

### 7.1 Önerilen minimum kurulum

- **Knowledgebase MCP** (`biocontext_kb`): harici literatür/biomedikal kaynak sorguları
- **Skill-to-MCP** (`meta-analysis-skills`): `skills/` altındaki SOP/şablonları resource olarak sunar
- **Paper-Search MCP** (`paper-search`): çoklu kaynak arama + PDF indirme/okuma

### 7.2 Önkoşullar

- Python (tercihen 3.11+)
- `uv` / `uvx` (kullanım kolaylığı)

PATH ayarı:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 7.3 `uv/uvx` kurulumu (bir kere)

```bash
python -m pip install --user uv
```

Doğrulama:

```bash
~/.local/bin/uv --version
~/.local/bin/uvx --version
```

### 7.4 MCP konfigürasyonu

- Dosya: `.vscode/mcp.json`
- İçerik: 3 server tanımı (`biocontext_kb`, `meta-analysis-skills`, `paper-search`)

### 7.5 Skills klasörü (SOP ekleme)

Yeni skill eklemek için:

1) `skills/<skill-adi>/` klasörü aç
2) İçine `SKILL.md` koy
3) YAML frontmatter alanlarını doldur:

```md
---
name: my-skill
description: Ne işe yarar, ne zaman kullanılır?
---
```

### 7.6 Hızlı terminal doğrulaması

#### 7.6.1 Skill-to-MCP

```bash
export PATH="$HOME/.local/bin:$PATH"
uvx --python 3.12 skill_to_mcp --skills-dir "$(pwd)/skills"
```

#### 7.6.2 Knowledgebase MCP

```bash
export PATH="$HOME/.local/bin:$PATH"
uvx --python 3.12 biocontext_kb@latest
```

#### 7.6.3 Paper-Search MCP

```bash
export PATH="$HOME/.local/bin:$PATH"
uvx --python 3.12 --from paper-search-mcp python -m paper_search_mcp.server
```

> Not: İndirilen PDF’ler `.vscode/mcp.json` içindeki `PAPER_SEARCH_DOWNLOAD_DIR` dizinine iner.

### 7.7 Cline içinde “ne zaman hangi server?”

- Süreç/SOP/şablon ihtiyacı: `meta-analysis-skills`
- Harici kaynak taraması: `biocontext_kb`
- Multi-source arama + PDF indirme/okuma: `paper-search`

### 7.8 Örnek akış (Cline prompt iskeleti)

#### 7.8.1 PICO → sorgular → arama QA

1) Skill: `pico-to-search-query`
2) Query’leri çalıştır:
   - `biocontext_kb` (EuropePMC/preprint)
   - veya `paper-search` (multi-source)
3) QA:
   - Skill: `prisma-s-press-search-qa`

#### 7.8.2 Dedup + screening log + evidence pointer

1) Skill: `dedup-record-manager`
2) Skill: `screening-inclusion-exclusion`
3) Skill: `audit-log-evidence-pointer`

#### 7.8.3 Full-text fetch + veri çıkarımı + RoB

1) `paper-search.search` ile sonuçları bul
2) `paper-search.fetch` ile seçilen `id` için detay getir
3) Skill: `data-extraction-effect-size`
4) Skill: `missing-data-conversions`
5) RoB:
   - RCT → `risk-of-bias-rob2`
   - Non-RCT → `risk-of-bias-robins-i`

#### 7.8.4 Analiz sonrası GRADE + SoF

- Skill: `grade-sof`

---

## 8) Repo içi log dosyalarını CLI ile doldurma (`tools.prisma_log`)

```bash
python -m tools.prisma_log -h
```

### 8.1 PRISMA sayaçları

```bash
python -m tools.prisma_log prisma-set --field screening.records_screened --value 120
python -m tools.prisma_log prisma-set --field identification.records_removed_before_screening.duplicates --value 35
python -m tools.prisma_log prisma-add-excluded --reason "wrong population" --n 12
```

### 8.2 Screening kararları (JSONL append)

```bash
python -m tools.prisma_log screening-append \
  --record-id "doi:10.1000/xyz" \
  --source EuropePMC \
  --stage title_abstract \
  --decision exclude \
  --reasons "not comparative|wrong population"
```

### 8.3 Audit log (kanıt referanslı JSONL append)

```bash
python -m tools.prisma_log audit-append \
  --action screening_decision \
  --record-id "doi:10.1000/xyz" \
  --payload-json '{"decision":"exclude"}' \
  --evidence-json '{"source_type":"database_record","source_locator":{"url":"https://..."},"location":{}}'
```

### 8.4 Protokol değişikliği (CSV append)

```bash
python -m tools.prisma_log protocol-change-append \
  --section "Analysis.Model" \
  --old-value "DL" \
  --new-value "HKSJ" \
  --reason "Small k" \
  --impact-assessment "CI widen" \
  --approved-by "PI"
```

---

## 9) Kapsam çapraz kontrol matrisi (4 doküman → bu doküman)

Bu bölüm, “tam kapsam”ı pratik olarak doğrulamak için bir kontrol matrisi sunar.

### 9.1 `AI-AGENT-VERI-CEKME-KILAVUZU.md` kapsama kontrolü

- [x] Temel prensipler (reprodüksiyon, idempotency, güvenlik, rate limit) → Bölüm 1
- [x] `.env` minimum konfigürasyon → Bölüm 2
- [x] Agent iş akışı (PICO→query→discovery→registries→regülatif→enrichment) → Bölüm 3
- [x] “Altın komutlar” (PubMed, EuropePMC, OpenAlex, Semantic Scholar, SerpAPI, CT.gov, openFDA, EMA, Anna’s Archive, Crossref, Unpaywall, OpenCitations, Wiley, Elsevier, DOI enrichment) → Bölüm 4
- [x] PRISMA-S log alanları + agent checklist → Bölüm 6
- [x] Hata yönetimi / retry / deterministik çıktı yaklaşımı → Bölüm 1.2, 1.4 ve 6

### 9.2 `ARAMA-VERI-KAYNAKLARI-VE-API-ERISIMI.md` kapsama kontrolü

- [x] Hızlı özet tablo (kaynaklar + erişim modeli + dokümantasyon linkleri) → Bölüm 5.1
- [x] Repo-local araçların durum matrisi → Bölüm 5.2
- [x] PubMed/NCBI iş akışı + rate limit notları → Bölüm 4.1 ve 5.3
- [x] Europe PMC polite email + örnek → Bölüm 4.2 ve 5.4
- [x] Semantic Scholar + rate limit → Bölüm 4.4 ve 1.4
- [x] Google Scholar uyarısı → Bölüm 5.5 ve 4.5 notu
- [x] Elsevier Scopus/Embase erişim modeli + search tips/proximity → Bölüm 5.6 ve 4.14
- [x] Cochrane API vs Wiley TDM ayrımı → Bölüm 5.7
- [x] Unpaywall email zorunluluğu → Bölüm 2 ve 4.11/5.1
- [x] OpenCitations limit/token opsiyonu (genel referans) → Bölüm 5.2 ve 4.12
- [x] ClinicalTrials.gov pagination notu → Bölüm 4.6
- [x] EMA EPAR dataset indirme/arama → Bölüm 4.8 ve 5.1
- [x] PRISMA-S log şablonu → Bölüm 6

### 9.3 `MCP-KULLANIM-DOKUMANTASYONU.md` kapsama kontrolü

- [x] MCP sunucuları ve amaçları (biocontext_kb / meta-analysis-skills / paper-search) → Bölüm 7.1
- [x] Konfigürasyon notları (.vscode/mcp.json, env) → Bölüm 7.4 ve Bölüm 2
- [x] Cline içinde kullanım rehberi (PICO→search QA, dedup/screening/audit, full-text/data extraction/RoB, GRADE) → Bölüm 7.7–7.8
- [x] MCP araçlarını CLI ile test etme (`uvx ...`) → Bölüm 7.6
- [x] Loglama önerileri ve tools.prisma_log referansı → Bölüm 8

### 9.4 `RUNBOOK-MCP-STRATEJI-1.md` kapsama kontrolü

- [x] Strateji-1 kurulum (3 MCP server, .vscode/mcp.json) → Bölüm 7.1, 7.4
- [x] Önkoşullar + uv/uvx kurulumu + PATH → Bölüm 7.2–7.3
- [x] Skills klasörü ve skill ekleme standardı → Bölüm 7.5
- [x] Terminal doğrulama komutları (3 server) → Bölüm 7.6
- [x] “Ne zaman hangi server?” + en iyi pratik → Bölüm 7.7
- [x] Örnek akış (Cline prompt iskeleti) → Bölüm 7.8
- [x] tools.prisma_log ile PRISMA/screening/audit/protocol-change örnekleri → Bölüm 8

---

## 10) Tutarlılık ve bütüncüllük notları (birleştirme kararları)

Bu birleşik dokümanda aşağıdaki tutarlılık düzenlemeleri yapılmıştır:

1) **Tek “kaynaklar” tablosu**: Veri kaynakları ve erişim notları tek tabloda toplandı (Bölüm 5.1).
2) **Tek “altın komutlar” bölümü**: CLI örnekleri tekrar etmeyecek şekilde konsolide edildi (Bölüm 4).
3) **Google Scholar uyarıları**: ToS/etik uyarılar tek yerde standartlaştırıldı (Bölüm 5.5 + 4.5 notu).
4) **Cochrane vs Wiley ayrımı**: Token/header farkı net bir şekilde ayrıştırıldı (Bölüm 5.7).
5) **PRISMA-S log şeması**: Log alanları tek standarda bağlandı (Bölüm 6).
