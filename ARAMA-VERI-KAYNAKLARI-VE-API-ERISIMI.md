# Sistematik Literatür Taraması için Veri Kaynakları ve API/Programatik Erişim Rehberi

Bu doküman, `META-ANALIZ-KILAVUZU.md` içindeki **4. Sistematik literatür taraması** bölümünü uygulamaya dökmek için; PubMed/MEDLINE, Embase, Cochrane CENTRAL, Scopus, Web of Science, Semantic Scholar, Google Scholar ve ilgili “gri literatür + kayıt + regülatif” kaynaklarına **nasıl erişileceğini** (UI, export, API, kurumsal erişim) ve **nasıl yeniden üretilebilir şekilde kullanılacağını** derler.

> Odak: **yeniden üretilebilir arama** (PRISMA-S), **denetlenebilir loglama**, ve mümkün olan yerlerde **API ile otomasyon**.

---

## 1) Hızlı Özet Tablo

| Kaynak | Tür | Programatik erişim | Lisans/erişim notu | Resmî dokümantasyon |
|---|---|---|---|---|
| PubMed/MEDLINE (NLM/NCBI) | Bibliyografik | **Var:** NCBI E-utilities | Ücretsiz; hız limiti var | https://www.ncbi.nlm.nih.gov/books/NBK25497/  |
| PubMed Central (PMC) | Tam metin (OA ağırlıklı) | **Var:** E-utilities (pmc db), ayrıca Europe PMC | Ücretsiz; tam metin kapsamı sınırlı | https://www.ncbi.nlm.nih.gov/home/develop/api/ |
| Europe PMC | Bibliyografik + PMC benzeri tam metin | **Var:** REST API | Ücretsiz | https://europepmc.org/RestfulWebService |
| Embase | Bibliyografik (Emtree) | **Sınırlı/kurumsal:** Elsevier Embase API | Genellikle abonelik/kurumsal onay | https://dev.elsevier.com/embase_apis.html |
| Cochrane CENTRAL | Klinik çalışma kayıtları | UI + (kısıtlı) Cochrane API | Cochrane Library erişimi gerekebilir | https://test-api.cochrane.org/api-docs/index.html |
| Scopus | Bibliyografik + atıf | **Var:** Elsevier Scopus APIs | Abonelik + API key (çoğu kurumda InstToken) | https://dev.elsevier.com/ |
| Web of Science | Bibliyografik + atıf | **Var:** Clarivate WoS APIs | Abonelik + API erişim izni | https://developer.clarivate.com/apis/wos |
| Semantic Scholar | Açık akademik grafik | **Var:** Academic Graph API | Ücretsiz; rate limit var | https://api.semanticscholar.org/api-docs/ |
| Google Scholar | Arama motoru/indeks | **Resmî API yok** | Otomasyon ToS/robots riskli | (resmî API yok) |
| OpenAlex | Açık bibliyografik + atıf | **Var:** REST API | Ücretsiz; “polite pool” için email önerilir | https://docs.openalex.org/ |
| Crossref | DOI/metadata | **Var:** REST API | Ücretsiz; “mailto/User-Agent” önerilir | https://www.crossref.org/documentation/retrieve-metadata/rest-api/ |
| Unpaywall | OA full-text linkleri | **Var:** API | Ücretsiz; email param zorunlu | https://unpaywall.org/products/api |
| OpenCitations | Atıf grafiği | **Var:** REST API | Ücretsiz | https://api.opencitations.net/ |
| ClinicalTrials.gov | Kayıt sonuçları | **Var:** API v2 | Ücretsiz | https://clinicaltrials.gov/data-api/api |
| WHO ICTRP | Çoklu kayıt portalı | Resmî açık API tipik değil; indirme/portal | Erişim süreci değişken | https://www.who.int/tools/clinical-trials-registry-platform |
| FDA (openFDA) | Regülatif veri setleri | **Var:** openFDA API + veri indirme | Ücretsiz; rate limit var | https://open.fda.gov/apis/ |
| EMA EPAR / EU Open Data | Regülatif özet/rapor tabloları | Çoğu zaman veri seti (Excel/CKAN) | “Resmî tek REST API” her zaman yok | https://data.europa.eu/data/datasets/epar-human-medicines |
| Wiley Online Library (TDM) | Tam metin (abonelik kapsamına bağlı) | **Var:** Wiley TDM API | Token (Clickthrough Client Token) gerekir; kapsam/ToS önemli | https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining |

---

## 2) PubMed/MEDLINE (NCBI E-utilities) — En Önemli Otomasyon Bileşeni

### 2.1 Ne zaman kullanılır?
- Sistematik taramanın omurgası (MEDLINE indeksli literatür).
- PRISMA-S için arama sorgusunu “ham string” olarak kaydetmek kolay.
- PMID üzerinden standardize metadata çekimi (başlık, özet, MeSH, dergi, yıl, yazarlar).

### 2.2 Temel iş akışı
1) **ESearch** ile sorguyu çalıştır, PMID listesini al.
2) (İsteğe bağlı) **ESummary** ile hızlı özet/metadata al.
3) **EFetch** ile detaylı kayıt al (XML/medline/plaintext vb.).

### 2.3 Rate limit ve kimlik parametreleri
NCBI hız limitleri (genel):
- **API key yoksa:** saniyede ~3 istek.
- **API key ile:** saniyede ~10 istek.

Kaynak: NCBI E-utilities genel tanıtımı: https://www.ncbi.nlm.nih.gov/books/NBK25497/

Öneri:
- İsteklere `tool=` ve `email=` ekleyin (NCBI iyi vatandaşlık).
- Yüksek hacimde çekim için `usehistory=y` + WebEnv/query_key kullanın.

### 2.4 Örnekler (curl)

**A) ESearch (PMID listesi):**

```bash
TERM='(adapalene[Title/Abstract] OR adapalene[MeSH Terms]) AND (benzoyl peroxide[Title/Abstract] OR benzoyl peroxide[MeSH Terms])'
curl -sG 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi' \
  --data-urlencode db=pubmed \
  --data-urlencode term="$TERM" \
  --data-urlencode retmax=20 \
  --data-urlencode retmode=json \
  --data-urlencode tool='meta-analysis-repo' \
  --data-urlencode email='you@example.com'
```

### 2.4.1 Repo entegrasyonu (CLI) — PubMed + PMC

Bu repoda NCBI E-utilities için repo-local bir CLI vardır:

```bash
# PubMed ESearch (JSON)
python -m tools.ncbi_eutils esearch \
  --db pubmed \
  --term '(adapalene[tiab]) AND (benzoyl peroxide[tiab])' \
  --retmax 20 \
  --out data/raw/ncbi/pubmed_esearch.json

# PubMed EFetch (XML) - örnek olarak ilk 2 PMID
python -m tools.ncbi_eutils efetch \
  --db pubmed \
  --ids '12345678,23456789' \
  --retmode xml \
  --out data/raw/ncbi/pubmed_efetch.xml

# PMC ESearch (JSON)
python -m tools.ncbi_eutils esearch \
  --db pmc \
  --term '(adapalene[tiab]) AND (benzoyl peroxide[tiab])' \
  --retmax 20 \
  --out data/raw/ncbi/pmc_esearch.json
```

Notlar:
- `.env` içinden otomatik okunur: `PUBMED_API_KEY`, `PUBMED_EMAIL` (yoksa `NCBI_API_KEY`, `NCBI_EMAIL`).
- Her çalıştırma `logs/search_log.csv` içine PRISMA-S uyumlu log satırı ekler.

**B) EFetch (PMID → XML):**

```bash
curl -sG 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi' \
  --data-urlencode db=pubmed \
  --data-urlencode id='12345678,23456789' \
  --data-urlencode retmode=xml \
  --data-urlencode tool='meta-analysis-repo' \
  --data-urlencode email='you@example.com'
```

### 2.5 R ve Python ile erişim

**R (`rentrez`)**
- PubMed için pratik; loglama + pagination yönetimi kolay.

**Python (Biopython `Entrez`)**
- NCBI, `Entrez.email` girilmesini ister.

> Not: Kodla çekim yaptığınızda arama sorgusunu, çekim tarihini, kullanılan parametreleri ve sonuç sayılarını `logs/search_log.csv` içine yazın (şema için bkz. Bölüm 20).

---

## 3) Europe PMC (REST API)

### 3.1 Neden önemli?
- Europe PMC; PubMed benzeri arama + bazı tam metin/alıntı zenginleştirmeleri sunar.
- API’si açık ve arama dili güçlü.

Dokümantasyon: https://europepmc.org/RestfulWebService

### 3.0 Polite kullanım (email)
Europe PMC genel olarak açık bir REST API sunsa da, yeniden üretilebilirlik ve “iyi vatandaşlık” için
bu repoda aramaları loglarken bir email bilgisini not ediyoruz.

`.env` içine ekleyin:

```dotenv
EUROPE_PMC_EMAIL=drmahirkurt@gmail.com
```

### 3.2 Örnek

```bash
curl -sG 'https://www.ebi.ac.uk/europepmc/webservices/rest/search' \
  --data-urlencode query='(TITLE:"adapalene" AND TITLE:"benzoyl peroxide")' \
  --data-urlencode format=json \
  --data-urlencode pageSize=25
```

### 3.2.1 Repo entegrasyonu (CLI)

Bu repoda Europe PMC için repo-local bir CLI vardır:

```bash
# Örnek sorgu çalıştır ve JSON'u kaydet
python -m tools.europe_pmc search \
  --query 'TITLE:"adapalene" AND TITLE:"benzoyl peroxide"' \
  --page-size 25 \
  --page 1 \
  --result-type lite \
  --out data/raw/europe_pmc/adapalene_bpo_search.json
```

Çıktılar:
- JSON: `data/raw/europe_pmc/...`
- Log: `logs/search_log.csv` içine `source=Europe PMC, interface=API, query=...` satırı eklenir.

### 3.3 R paketi
- `europepmc` (rOpenSci): hem query hem sonuç parse.

---

## 4) Semantic Scholar (Academic Graph API)

Dokümantasyon: https://api.semanticscholar.org/api-docs/

### 4.1 Kullanım senaryoları
- PubMed/Scopus/WoS yanında “ikincil” yakalama ve özellikle **atıf taraması**.
- Paper/Author/Corpus ID üzerinden zengin metadata.

### 4.2 Rate limit / hata yönetimi
- 429 (Too Many Requests) durumunda backoff.
- Bazı kaynaklar “anahtar iste” ile daha yüksek limitten söz eder; her durumda nazik istek hızı önerilir.

### 4.3 Örnek (paper search)

```bash
curl -sG 'https://api.semanticscholar.org/graph/v1/paper/search' \
  --data-urlencode query='adapalene benzoyl peroxide 5%' \
  --data-urlencode limit=5 \
  --data-urlencode fields='title,year,authors,citationCount,externalIds,url'
```

---

## 5) Google Scholar — Resmî API yok (Önemli Uyarı)

### 5.1 Gerçekçi durum
- Google Scholar için **resmî/kararlı bir kamu API’si yoktur**.
- Otomatik scraping; ToS, robots, IP kısıtlama ve hukuki riskler doğurabilir.

### 5.2 Sistematik derleme için öneri
Google Scholar’ı “tek kaynak” yapmayın. Bunun yerine:
- PubMed/Embase/Scopus/WoS gibi indekslenmiş veri tabanlarıyla temel taramayı yapın.
- Google Scholar’ı:
  - **gri literatür sinyali**, 
  - “cited by” ipuçları,
  - kurum arşivi/tez/rapor yakalama
  için **manuel + loglanmış** yardımcı kaynak olarak kullanın.

### 5.3 Reprodüksiyon
- Arama string’i, tarih, ilk kaç sayfanın tarandığı, uygulanan sıralama/filtre ve ekleme kriteri mutlaka loglanmalı.
- Export: Scholar arayüzünden direkt RIS/CSV her zaman yok; üçüncü parti araçlar (örn. Publish or Perish) kullanılabilir fakat bu tür araçların da ToS/etik riskleri dikkate alınmalıdır.

---

## 6) Scopus (Elsevier APIs)

Portal: https://dev.elsevier.com/

### 6.0 Elsevier API aileleri (Search / Retrieval / Metadata) — bu projede nerede kullanılır?

Elsevier Developer Portal, pratikte 3 ana API ailesi sunar:

1) **Search APIs** (`/content/search/...`)
   - Amaç: sorgu çalıştırmak ve *kayıt listesini* almak (discovery)
   - Bu proje bağlamı: Sprint 1’de **Scopus araması** için kullanılır (PRISMA-S uyumlu loglama ile).

2) **Retrieval APIs** (`/content/abstract/...`, `/content/article/...`)
   - Amaç: bir kaydın *detaylı* metadata/abstract bilgilerini çekmek (enrichment)
   - Bu proje bağlamı: Dedup sonrası seçilen kayıtlar için DOI/PMID/EID üzerinden zenginleştirme; özellikle
     - abstrakt/anahtar kelime/kurum-yazar bilgisi,
     - (yetkiye bağlı) tam metin linkleri veya erişim uygunluğu (“entitlement”) kontrolü.

3) **Metadata APIs** (`/content/abstract/citation-count`, `/content/abstract/citations`, serial/non-serial title)
   - Amaç: atıf sayısı/atıf overview ve dergi/kitap metadata doğrulama (bibliyografik tamamlama)
   - Bu proje bağlamı:
     - atıf taraması (citation chasing) için Scopus dışındaki OpenCitations/Semantic Scholar ile **tamamlayıcı**,
     - dergi/ISSN doğrulama (opsiyonel) ve “source title” standardizasyonu.

> Not: Elsevier API’lerde “VIEW” parametresi ile dönen alan seti değişebilir ve bazı VIEW’ler abonelik/kurumsal yetkiye bağlıdır.

### 6.1 Erişim modeli
- Genellikle **API Key** gerekir.
- Kurum aboneliği ile **Institutional Token (InstToken)** gerekebilir.

### 6.2 Örnek (Scopus Search API)

```bash
curl -sG 'https://api.elsevier.com/content/search/scopus' \
  -H 'Accept: application/json' \
  -H 'X-ELS-APIKey: ${ELSEVIER_API_KEY}' \
  --data-urlencode query='TITLE-ABS-KEY(adapalene AND benzoyl AND peroxide)'
```

#### 6.2.1 Phrase (ifade) ve proximity (yakınlık) araması — Search Tips’e göre doğru sentaks

Kaynak (Scopus Search Tips): https://dev.elsevier.com/sc_search_tips.html

**A) Phrase araması (2 farklı davranış)**

1) **Exact phrase (tam ifade)**: süslü parantez kullanın.
   - Tanım: stop word’ler, boşluklar ve noktalama *dahil* birebir eşleşme.
   - Örnek: `{benzoyl peroxide}`

2) **Loose/approximate phrase (gevşek ifade)**: çift tırnak kullanın.
   - Tanım: terimler bitişik olmalı; noktalama çoğunlukla göz ardı edilir; çoğullar vb. genişleyebilir.
   - Örnek: `"benzoyl peroxide"`

> Önemli pratik not: Scopus Search API çağrılarında query parametresini mutlaka **URL-encoded** gönderin.
> Bu repo için en güvenlisi `curl --data-urlencode` kullanmaktır. (Aksi halde tırnak/özel karakterler “Bad Request” hatasına sebep olabilir.)

**Çalışan örnekler (200 OK ile doğrulandı):**

```bash
# Loose phrase (çift tırnak)
curl -sG 'https://api.elsevier.com/content/search/scopus' \
  -H 'Accept: application/json' \
  -H 'X-ELS-APIKey: ${ELSEVIER_API_KEY}' \
  --data-urlencode 'query=TITLE-ABS-KEY(adapalene AND "benzoyl peroxide")'

# Exact phrase (süslü parantez)
curl -sG 'https://api.elsevier.com/content/search/scopus' \
  -H 'Accept: application/json' \
  -H 'X-ELS-APIKey: ${ELSEVIER_API_KEY}' \
  --data-urlencode 'query=TITLE-ABS-KEY(adapalene AND {benzoyl peroxide})'
```

**B) Proximity araması (yakınlık operatörleri)**

- `W/n`: terimler birbirine **n kelime** mesafede (genelde sıra esnek).
- `PRE/n`: ilk terim, ikinci terimden **önce** gelmeli ve araları **n kelime** içinde olmalı.

Örnekler:

```bash
# benzoyl kelimesi peroxide kelimesine 1 kelime mesafede olsun
curl -sG 'https://api.elsevier.com/content/search/scopus' \
  -H 'Accept: application/json' \
  -H 'X-ELS-APIKey: ${ELSEVIER_API_KEY}' \
  --data-urlencode 'query=TITLE-ABS-KEY(adapalene AND benzoyl W/1 peroxide)'

# benzoyl, peroxide’den önce gelsin ve araları 1 kelimeyi geçmesin
curl -sG 'https://api.elsevier.com/content/search/scopus' \
  -H 'Accept: application/json' \
  -H 'X-ELS-APIKey: ${ELSEVIER_API_KEY}' \
  --data-urlencode 'query=TITLE-ABS-KEY(adapalene AND benzoyl PRE/1 peroxide)'
```

**C) Proximity içinde Boolean kısıtı (Search Tips notu)**

- Scopus, proximity ifadesinin argümanı olarak `AND` veya `AND NOT` kullanılmasını desteklemez.
  - Örn: `cat pre/10 (dog AND mouse)` **geçersiz**
- Ancak `OR` ile grup kullanılabilir.
  - Örn: `(water OR vinegar OR wine) w/5 (oil OR yogurt)`

> Not: Yetkiye bağlı olarak tam alan seti ve atıf metrikleri değişebilir.

### 6.3 R
- `rscopus` paketi API anahtarını yönetir.

### 6.4 Önerilen minimum `.env` alanları (Scopus/Elsevier)

```dotenv
ELSEVIER_API_KEY=
ELSEVIER_EMAIL=

# Kurumsal erişimde gerekebilir
ELSEVIER_INSTTOKEN=
```

### 6.5 Proje için pratik kullanım akışları (Sprint uyumlu)

**A) Sprint 1 — Arama (Scopus Search API)**
- Endpoint: `GET https://api.elsevier.com/content/search/scopus`
- Query dili: `TITLE-ABS-KEY(...)` (Scopus query syntax)
- Çıktı: ham JSON + RIS/CSV export’a dönüştürme
- Log: `logs/search_log.csv` (source=Scopus, interface=API, query=..., results_total=...)

**B) Sprint 2 — Zenginleştirme (Abstract Retrieval API)**
- Amaç: dedup sonrası kalan kayıtlar için DOI/PMID/EID üzerinden daha zengin alanları çekmek
- Endpoint örnekleri:
  - `GET /content/abstract/doi/{doi}`
  - `GET /content/abstract/pubmed_id/{pubmed_id}`
  - `GET /content/abstract/eid/{eid}`

**C) Sprint 1–2 — Atıf sinyali (Metadata: Citation Count / Citations Overview)**
- Endpoint:
  - `GET /content/abstract/citation-count` (atıf sayısı)
  - `GET /content/abstract/citations` (atıf overview)
- Not: Bu çıktılar, OpenCitations/Semantic Scholar ile çapraz doğrulama için yardımcıdır.

---

## 7) Embase (Elsevier Embase APIs)

Başlangıç noktası: https://dev.elsevier.com/embase_apis.html

### 7.1 Notlar
- Embase çok güçlü bir sistematik tarama kaynağıdır (özellikle ilaç/AE ve Emtree).
- API erişimi çoğu zaman **abonelik ve ayrıca onay** gerektirir.

### 7.2 Pratik yaklaşım
- Kurumunuzda Embase erişimi varsa:
  1) Önce UI üzerinden arama stratejisini netleştirin (Emtree + serbest metin).
  2) Sonra mümkünse API ile aynı stratejiyi çalıştırıp export’u otomatikleştirin.
  3) Değilse UI export (RIS/CSV) + log.

---

## 8) Web of Science (Clarivate)

Dokümantasyon girişleri:
- WoS API Expanded: https://developer.clarivate.com/apis/wos
- WoS Starter API: https://developer.clarivate.com/apis/wos-starter

### 8.1 Erişim modeli
- Abonelik + Clarivate geliştirici portalında yetkilendirme.

### 8.2 Kullanım senaryosu
- Scopus ile benzer biçimde atıf taraması, “related records”, times-cited vb.

### 8.3 Kurumsal erişim + kimlik doğrulama (Web of Science) — operasyonel kontrol listesi

> Web of Science API kullanımı genellikle **abonelik** ve Clarivate Developer Portal’da **yetkilendirme** gerektirir.

**A) Ön koşullar**
- Kurumunuzun WoS Core Collection aboneliği var mı?
- API erişimi için (Starter/Expanded) kurumunuz adına yetki tanımlı mı?

**B) Başvuru / portal adımları**
1. Clarivate Developer Portal’da hesap oluşturun:
   - https://developer.clarivate.com/apis/wos
2. Kullanmak istediğiniz API’yi seçin:
   - Expanded (daha zengin alanlar)
   - Starter (Lite’ın yerini alan)
3. Uygulama kaydı / API credential alma adımlarını tamamlayın.
4. Erişim türünü doğrulayın:
   - IP allow-list (kurumsal) gerekebilir
   - Token/Key temelli olabilir

**C) İsteklerde iyi pratikler**
- Rate limit dokümanını kontrol edin.
- Retry/backoff (429/5xx) uygulayın.
- Aynı sorgular için cache ve idempotent çıktı üretin.

**D) Loglama (PRISMA-S)**
- API adı (Starter/Expanded), sürüm, endpoint, tarih, sorgu, filtre ve toplam sonuç sayısı.

---

## 9) Cochrane CENTRAL ve Cochrane Library

### 9.1 CENTRAL nedir?
- Kontrollü çalışmalar için kritik bir kaynak.

### 9.2 Erişim
- Çoğu kullanım UI/kurumsal erişim üzerinden.
- Cochrane API dokümanı (erişim kısıtlı olabilir): https://test-api.cochrane.org/api-docs/index.html

> Not (önemli): `https://test-api.cochrane.org/api-docs/swagger.json` dosyasına erişim **açık** olabilir (HTTP 200).
> Ancak gerçek veri endpoint'leri (örn. `/reviews`) pratikte **`Authorization: Bearer <access_token>`** ister.
> Bu Bearer token, **Wiley TDM token / Wiley hesabı** ile ilgili değildir.
> 
> Kısacası:
> - Cochrane test API: `Authorization: Bearer ...` (Cochrane API erişimi)
> - Wiley Online Library TDM API: `Wiley-TDM-Client-Token: ...` (Wiley tam metin indirme)

Pratik öneri:
- UI aramasını “tam string” olarak saklayın ve export edilebilen formatlarla (RIS/CSV) kayıtları yönetin.

---

### 9.3 Kurumsal erişim + kimlik doğrulama (Cochrane / CENTRAL) — operasyonel kontrol listesi

> Cochrane Library/CENTRAL erişimi çoğu kurumda **abonelik + IP tanıma** veya **kurumsal oturum** ile gelir. Cochrane API’leri ise ayrıca **geliştirici portalı** üzerinden yetki gerektirebilir.

**A) Kurum erişimini doğrula (UI):**
1. Kurum ağı/VPN üzerinden https://www.cochranelibrary.com/ açın.
2. CENTRAL’da örnek bir sorgu çalıştırın ve sonuç geldiğini doğrulayın.
3. Export seçeneklerini kontrol edin (RIS/EndNote, CSV vb. ne sağlanıyor?).

**B) API erişimi gerekiyorsa (Cochrane API):**
1. Kurumsal/kullanıcı hesabınızla Cochrane geliştirici ortamına erişim isteyin.
2. API dokümantasyonunu ve base URL’leri doğrulayın:
   - https://test-api.cochrane.org/api-docs/index.html
3. Kimlik doğrulama tipini belirleyin:
   - API Key mi?
   - OAuth2 / JWT mi?
   - Basic auth mı?
4. Uygulamada sır saklama:
   - **Anahtarları repo’ya yazmayın.**
   - Tercih: `.env` dosyası (gitignore) veya CI secret.

**C) Minimum log alanları (PRISMA-S):**
- “Cochrane CENTRAL (UI)” olarak source’u loglayın.
- “Cochrane API” kullanıldıysa interface=API ve kullanılan endpoint/parametreleri not edin.

---

## 10) OpenAlex (Açık bibliyografik indeks)

Dokümantasyon: https://docs.openalex.org/

### 10.1 Neden kullanılır?
- Açık/ücretsiz; geniş kapsama ve atıf bağlantıları.
- Google Scholar’a alternatif/yardımcı olarak otomasyona daha uygundur.

### 10.2 Rate limit
- Genel olarak saniyede ~10 istek üstü 429 üretebilir.
- “Polite pool” için isteklerde email paylaşımı önerilir.

### 10.3 Örnek

```bash
curl -sG 'https://api.openalex.org/works' \
  --data-urlencode search='adapalene benzoyl peroxide 5%' \
  --data-urlencode per-page=25 \
  --data-urlencode mailto='you@example.com'
```

### 10.4 Repo entegrasyonu (CLI)

Bu repoda OpenAlex için repo-local bir CLI vardır:

`.env` içine (opsiyonel ama önerilir):

```dotenv
OPENALEX_API_KEY=
OPENALEX_EMAIL=you@example.com
```

**A) Works search (JSON):**

```bash
python -m tools.openalex search \
  --search 'adapalene benzoyl peroxide' \
  --per-page 25 \
  --select 'id,doi,title,publication_year,authorships' \
  --out data/raw/openalex/works_search.json
```

Cursor paging:
- İlk çağrıda `--cursor '*'` kullanın.
- Bir sonraki sayfa için `meta.next_cursor` değerini alıp `--cursor '<next_cursor>'` ile tekrar çağırın.

**B) Tekil work detay (JSON):**

```bash
python -m tools.openalex work \
  --id 'https://openalex.org/W2105610837' \
  --out data/raw/openalex/work.json
```

Çıktılar:
- JSON: `data/raw/openalex/...`
- Log: `logs/search_log.csv` içine `source=OpenAlex, interface=API, query=...` satırı eklenir.

---

## 11) Crossref (DOI/metadata)

Dokümantasyon: https://www.crossref.org/documentation/retrieve-metadata/rest-api/

### 11.1 Neden kullanılır?
- DOI doğrulama, bibliyografik metadata tamamlama, dergi/ISSN/ yayın yılı eşleme.

### 11.2 “Polite pool”
- `mailto=` parametresi veya User-Agent ile iletişim bilgisi eklemek önerilir (rate limit/etiket).

Örnek:
```bash
curl -sG 'https://api.crossref.org/works' \
  --data-urlencode 'query.bibliographic=adapalene benzoyl peroxide' \
  --data-urlencode 'rows=5' \
  --data-urlencode 'mailto=you@example.com'
```

---

## 12) Unpaywall (OA full text linkleri)

API: https://unpaywall.org/products/api

### 12.1 Amaç
- DOI → açık erişim PDF/landing linklerini bulmak (tam metin indirme için “en iyi” açık konum).

### 12.2 Örnek

```bash
DOI='10.1038/nature12373'
curl -s "https://api.unpaywall.org/v2/${DOI}?email=you@example.com" | jq .
```

---

## 13) OpenCitations (atıf grafiği)

API ana sayfa: https://api.opencitations.net/

### 13.1 Amaç
- DOI/PMID üzerinden “kim kimi cite etmiş” verisi ile ileri/geri atıf taraması.

---

## 14) ClinicalTrials.gov (API v2)

Dokümantasyon: https://clinicaltrials.gov/data-api/api

### 14.1 Kullanım
- Yayınlanmamış/sonuç raporu eksik çalışmaların saptanması.
- “missing results” sinyali ve RoB/GRADE tartışmaları.

### 14.2 Örnek

```bash
curl -sG 'https://clinicaltrials.gov/api/v2/studies' \
  --data-urlencode 'query.term=acne adapalene benzoyl peroxide' \
  --data-urlencode 'pageSize=10'
```

---

## 15) WHO ICTRP

Ana sayfa: https://www.who.int/tools/clinical-trials-registry-platform

Notlar:
- ICTRP; çoklu kayıtları tek arayüzde birleştirmeyi hedefler.
- Programatik erişim çoğu zaman “resmî açık API” şeklinde değil; dönemsel dump/indirme süreçleri olabilir.
- Bu nedenle, ICTRP taraması genelde UI üzerinden yapılıp, erişim tarihi ve sonuç sayısı loglanır.

---

## 16) EudraCT / EU Clinical Trials Register / CTIS

Arayüz:
- EU CTR: https://www.clinicaltrialsregister.eu/
- EudraCT: https://eudract.ema.europa.eu/

Notlar:
- Bu ekosistem 2025 sonrası CTIS’e evrilmiştir; eski EudraCT kayıtları EU CTR’de görüntülenir.
- Resmî ve stabil bir açık REST API her zaman bulunmayabilir; çoğu zaman UI export/indirme ile çalışılır.

---

## 17) FDA — openFDA ve veri indirmeleri

API giriş: https://open.fda.gov/apis/

### 17.1 Rate limit
- Standart limit (dokümantasyonda): API key olmadan IP başına ~240 istek/dk.

Kaynak: https://open.fda.gov/apis/authentication/

### 17.2 Örnek (drug label)
```bash
curl -sG 'https://api.fda.gov/drug/label.json' \
  --data-urlencode 'search=adapalene' \
  --data-urlencode 'limit=5'
```

---

## 18) EMA EPAR / EU Open Data

EPAR veri seti örneği: https://data.europa.eu/data/datasets/epar-human-medicines

Notlar:
- EPAR içerikleri çoğu zaman tablo/dataset olarak yayımlanır (Excel/CSV/CKAN indirme).
- “Her şeyi kapsayan tek resmî REST API” her zaman olmayabilir; en güvenilir yaklaşım: **dataset indir + versiyonla + erişim tarihini logla**.

---

## 19) Lens.org (Scholar API) — Opsiyonel (Token tabanlı)

Dokümantasyon: https://docs.api.lens.org/

Lens; hem patent hem akademik kayıtlar için arama sunar ve token ile çalışır. Sistematik taramalarda “alternatif indeks” olarak değerlendirilebilir.

---

## 19.1) Wiley Online Library — Text and Data Mining (TDM) API (Token tabanlı)

Kaynak: https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining

### 19.1.1 Neden / ne zaman kullanılır?
- Wiley Online Library üzerinde bulunan ve kurum aboneliğinizin/erişim hakkınızın kapsadığı içeriklerin **tam metnini (PDF/HTML)** programatik olarak indirmek için.
- Sistematik derlemede **full-text retrieval** aşamasında (özellikle yayıncı platformlarından tam metin indirme) yardımcı olur.

> Önemli not: Bu API bir “arama/discovery” API’si değildir; çoğunlukla **DOI bilerek** çalışılır.

### 19.1.2 Kimlik doğrulama
- Header: `Wiley-TDM-Client-Token: <token>`
- Bu repo standardı: `.env` içine

```dotenv
WILEY_TDM_CLIENT_TOKEN=
```

### 19.1.3 Endpoint
- Tekil DOI indirme:

```
GET https://api.wiley.com/onlinelibrary/tdm/v1/articles/{doi}
```

### 19.1.4 Örnek (curl)

```bash
DOI='10.1002/net.22207'
curl -L -s -o "${DOI//\//_}.pdf" \
  -H "Wiley-TDM-Client-Token: ${WILEY_TDM_CLIENT_TOKEN}" \
  -H 'Accept: application/pdf' \
  "https://api.wiley.com/onlinelibrary/tdm/v1/articles/${DOI}"
```

### 19.1.5 Repo entegrasyonu (CLI)

Bu repoda Wiley TDM için repo-local bir CLI eklenmiştir:

```bash
# dry-run: sadece status ve content-type gör
python -m tools.wiley_tdm download --doi 10.1002/net.22207 --dry-run

# PDF indir ve yanına basit meta json yaz
python -m tools.wiley_tdm download --doi 10.1002/net.22207 --format pdf --write-meta
```

> Pratik not: Eğer amacınız “Wiley account” ile programatik erişim ise,
> Cochrane test API değil, çoğunlukla **Wiley TDM API** (bu bölüm) kullanılmalıdır.

Çıktılar:
- PDF/HTML: `data/raw/pdfs/paper_search/`
- Log: `logs/search_log.csv` içine `source=Wiley TDM, interface=API, query=doi:..., endpoint=...` satırı eklenir.

### 19.1.6 Loglama (PRISMA-S)
- `logs/search_log.csv`:
  - `source`: `Wiley TDM`
  - `interface`: `API`
  - `query`: `doi:{doi}`
  - `exported_format`: `pdf` veya `html`
  - `export_scope`: `single`
  - `notes`: kaydedilen dosya yolu / dry-run / hata detayı


---

## 20) Yeniden Üretilebilir Arama Logu (PRISMA-S uyumlu şablon)

Her kaynak için aşağıdaki bilgileri **mutlaka** kaydedin:

> Repo standardı: sorgu string’leri `screening/search_strategies/*.txt`, export’lar `screening/exports/`, log `logs/search_log.csv` (bkz. `META-ANALIZ-ICRA-PLANI.md` Sprint 1).

### 20.1 Minimum alanlar (CSV/Markdown tablo)

| alan | örnek |
|---|---|
| source | PubMed |
| interface | API (E-utilities) / UI |
| datetime_utc | 2026-01-31T12:00:00Z |
| query | tam arama string’i |
| filters | dil/tarih/yayın tipi (yoksa “none”) |
| sort | best match / date / relevance |
| results_total | 123 |
| exported_format | RIS / CSV / XML / JSON |
| export_scope | all / first 200 / date range |
| notes | örn. “seed çalışma yakalandı/yakalanmadı” |

### 20.2 Örnek YAML (isteğe bağlı)

```yaml
search_run:
  source: pubmed
  interface: eutils
  datetime_utc: 2026-01-31T12:00:00Z
  query: >-
    (adapalene[tiab] OR adapalene[mesh]) AND (benzoyl peroxide[tiab] OR benzoyl peroxide[mesh])
  filters:
    language: none
    date: inception-to-present
  results_total: 123
  export:
    format: xml
    retmax: 10000
  reproducibility:
    tool: meta-analysis-repo
    email: you@example.com
```

---

## 21) Pratik öneriler (Meta-analiz iş akışına entegrasyon)

1) **Önce geniş, sonra daralt:** Başlangıç sorgusunu duyarlı kurun; screening aşamasında dahil/dışla.
2) **En az iki büyük indeks + bir açık indeks:** PubMed + (Embase veya Scopus veya WoS) + OpenAlex/Semantic Scholar gibi.
3) **Kayıt taraması zorunlu:** ClinicalTrials.gov + (varsa EU CTR/CTIS) + ICTRP.
4) **Export format standardı:** RIS/EndNote XML/CSV → tek bir referans yöneticide birleştirip deduplikasyon.
5) **API çekimi yapıyorsanız:** rate limit + retry/backoff + idempotent kayıt (aynı sorgu aynı sonuç setiyle sürümlensin).

---

## 23) Anna's Archive — Açık Bilim ve Kitap Arşivi

### 23.1 Genel Bilgi
Anna's Archive, kitaplar, akademik makaleler, tezler ve diğer bilimsel dokümanların büyük bir açık erişim arşivi. Sci-Hub benzeri bir platform olup, milyonlarca dokümana erişim sağlar. **Resmi API** ve **MCP server** desteği vardır.

### 23.2 Erişim Koşulları
- **Ücretsiz üyelik:** Temel arama ve sınırlı indirme
- **Premium üyelik:** Bağış ile API erişimi ve sınırsız indirme
- **API Key:** Hesap ayarlarından alınır (Account ID: `5CxX9WiJ4sjvuXLtRpREdXngDWyd4`)

### 23.3 API Erişimi ve Kurulum

#### MCP Server Kurulumu (Önerilen)
```bash
# GitHub'dan indirin
wget https://github.com/iosifache/annas-mcp/releases/download/v0.1.0/annas-mcp-linux-x64.tar.gz
tar -xzf annas-mcp-linux-x64.tar.gz
cd annas-mcp

# Çalıştırılabilir yapın
chmod +x annas-mcp

# Test edin
./annas-mcp --help
```

#### MCP Server Konfigürasyonu
```json
{
  "mcpServers": {
    "annas-archive": {
      "command": "/path/to/annas-mcp",
      "args": ["mcp"],
      "env": {
        "ANNAS_SECRET_KEY": "5CxX9WiJ4sjvuXLtRpREdXngDWyd4",
        "ANNAS_DOWNLOAD_PATH": "/home/mahirkurt/projects/Meta-Analysis/downloads"
      }
    }
  }
}
```

### 23.4 Python API Kullanımı

#### Temel Kurulum
```python
import requests
import json
from pathlib import Path

class AnnasArchiveAPI:
    def __init__(self, api_key="5CxX9WiJ4sjvuXLtRpREdXngDWyd4"):
        self.api_key = api_key
        self.base_url = "https://annas-archive.li"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'Meta-Analysis-Research/1.0'
        })
    
    def search_books(self, query, lang="en", limit=50):
        """Kitap ara"""
        params = {
            'q': query,
            'lang': lang,
            'limit': limit
        }
        response = self.session.get(f"{self.base_url}/search", params=params)
        return response.json()
    
    def get_book_details(self, book_id):
        """Kitap detaylarını al"""
        response = self.session.get(f"{self.base_url}/book/{book_id}")
        return response.json()
    
    def download_book(self, book_id, output_path="./downloads"):
        """Kitabı indir"""
        Path(output_path).mkdir(exist_ok=True)
        
        # İndirme linkini al
        response = self.session.get(f"{self.base_url}/download/{book_id}")
        download_url = response.json()['download_url']
        
        # Dosyayı indir
        filename = f"{book_id}.pdf"
        filepath = Path(output_path) / filename
        
        with self.session.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        
        return filepath
```

#### Kullanım Örneği
```python
# API'yi başlat
api = AnnasArchiveAPI()

# Meta-analysis ile ilgili kitapları ara
results = api.search_books("meta analysis methods", lang="en", limit=20)

for book in results['books']:
    print(f"Başlık: {book['title']}")
    print(f"Yazar: {book['author']}")
    print(f"Yıl: {book['year']}")
    print(f"ID: {book['id']}")
    
    # Detayları al
    details = api.get_book_details(book['id'])
    print(f"Açıklama: {details.get('description', 'N/A')}")
    
    # İndir (premium üyelik gerekli)
    try:
        filepath = api.download_book(book['id'])
        print(f"İndirildi: {filepath}")
    except Exception as e:
        print(f"İndirme hatası: {e}")
    
    print("-" * 50)
```

### 23.5 CLI Kullanımı

#### Temel Arama
```bash
# Arama yap
./annas-mcp search "meta analysis" --limit 10

# Sonuçları JSON olarak al
./annas-mcp search "systematic review methods" --format json > results.json
```

#### İndirme
```bash
# Kitap ID'si ile indir
./annas-mcp download BOOK_ID_12345

# Toplu indirme
cat book_ids.txt | xargs -I {} ./annas-mcp download {}
```

### 23.6 Rate Limits ve Best Practices

- **Ücretsiz üyelik:** Saat başına 10 arama, günlük 5 indirme
- **Premium üyelik:** Saat başına 100 arama, sınırsız indirme
- **Retry logic:** 429 (rate limit) hatasında 60 saniye bekle
- **User-Agent:** Her istekte tanımlı User-Agent kullanın

### 23.7 Meta-Analysis Bağlamında Kullanım

Anna's Archive, meta-analysis çalışmaları için değerli bir kaynaktır çünkü:
- Nadir kitaplar ve eski yayınlara erişim
- Akademik tezler ve raporlar
- Konferans bildirileri
- Teknik raporlar

#### Sistemik Tarama İçin Entegrasyon
```python
def search_meta_analysis_resources(query_terms, output_dir="./meta_resources"):
    """Meta-analysis kaynaklarını ara ve indir"""
    api = AnnasArchiveAPI()
    
    all_results = []
    
    for term in query_terms:
        print(f"Aranıyor: {term}")
        results = api.search_books(term, limit=25)
        
        for book in results.get('books', []):
            # Meta-analysis ile ilgili filtrele
            if any(keyword in book.get('title', '').lower() for keyword in 
                  ['meta-analysis', 'meta analysis', 'systematic review', 'cochrane']):
                
                all_results.append(book)
                
                # Otomatik indir (premium gerekli)
                try:
                    filepath = api.download_book(book['id'], output_dir)
                    print(f"✓ İndirildi: {book['title']}")
                except:
                    print(f"✗ İndirilemedi: {book['title']}")
    
    # Sonuçları kaydet
    with open(f"{output_dir}/search_results.json", 'w') as f:
        json.dump(all_results, f, indent=2)
    
    return all_results

# Kullanım
terms = [
    "meta analysis methods",
    "systematic reviews handbook", 
    "cochrane methodology",
    "statistical methods meta-analysis"
]

results = search_meta_analysis_resources(terms)
```

### 23.8 Güvenlik ve Etik Notlar

- **Lisans kontrolü:** İndirilen materyallerin telif haklarını kontrol edin
- **Akademik kullanım:** Sadece araştırma amaçlı kullanın
- **Rate limiting:** API limitlerini aşmayın
- **Veri gizliliği:** Hassas bilgileri loglamayın

### 23.9 Alternatif Erişim Yöntemleri

Eğer API erişimi kısıtlı olursa:
1. **Web arayüzü:** https://annas-archive.li
2. **IPFS erişimi:** Bazı dosyalar IPFS üzerinden erişilebilir
3. **Tor Browser:** Anonim erişim için
4. **Mirror siteleri:** Ana site erişilemezse alternatifler

---

## 24) Kaynak Bağlantıları (Güncellenmiş Liste)

- Anna's Archive Ana Sayfa: https://annas-archive.li
- Anna's Archive API Dokümantasyonu: https://annas-archive.li/faq#api
- MCP Server GitHub: https://github.com/iosifache/annas-mcp
- NCBI E-utilities (genel): https://www.ncbi.nlm.nih.gov/books/NBK25497/
- NCBI Develop / APIs: https://www.ncbi.nlm.nih.gov/home/develop/api/
- Europe PMC REST: https://europepmc.org/RestfulWebService
- Semantic Scholar API: https://api.semanticscholar.org/api-docs/
- Elsevier Developer Portal (Scopus/Embase): https://dev.elsevier.com/
- Clarivate WoS APIs: https://developer.clarivate.com/apis/wos
- OpenAlex docs: https://docs.openalex.org/
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Unpaywall API: https://unpaywall.org/products/api
- OpenCitations API: https://api.opencitations.net/
- ClinicalTrials.gov Data API: https://clinicaltrials.gov/data-api/api
- openFDA APIs: https://open.fda.gov/apis/
