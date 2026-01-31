# Meta-Analiz İcra Planı (Fazlar/Sprintler)
## A/BPO %5 (Adapalen %0,1 + Benzoil Peroksit %5) — Güvenlilik & Tolerabilite

**Kaynak kılavuz:** `META-ANALIZ-KILAVUZU.md` (v3)
**R uygulama referansları:** `reference/Doing Meta-Analysis with R.md`, `reference/Meta-Analysis with R.md`
**Metodoloji referansları:** `reference/Introduction to Meta-Analysis.md`, `reference/Systematic Reviews in Health Research - Meta-Analysis in Context.md`, `reference/Network Meta-Analysis for Decision Making.md`
**Arama + API uygulama rehberi:** `ARAMA-VERI-KAYNAKLARI-VE-API-ERISIMI.md`

Bu doküman, `META-ANALIZ-KILAVUZU.md` doğrultusunda meta-analizi **uçtan uca yürütmek** için hazırlanmış **icra planıdır**. Plan; fazlar/sprintler halinde, her sprint için:

- hedef ve kapsam,
- adımlar (iş listesi),
- teslimatlar (deliverables),
- başarı kriterleri (done),
- human-in-the-loop (HITL) onay kapıları,
- gerekli **API entegrasyonları**, **tech stack** ve **R araç zinciri**

net ve uygulanabilir biçimde tanımlar.

---

# 1) Hedef, kapsam ve yöntemsel “north star”

## 1.1 Goal (Amaç)
A/BPO %5 topikal kombinasyonunun **güvenlilik/tolerabilite** profilini;

1) mümkün olduğunda **karşılaştırmalı pairwise meta-analiz** ile,
2) kanıt sınırlı ise **tek kollu (single-arm) güvenlilik meta-analizi** ile,
3) gerekirse daha geniş topikal akne tedavi ağında **Network Meta-Analiz (NMA)** ile

sentezlemek ve **PRISMA 2020 + Cochrane Handbook** uyumlu raporlamak.

## 1.2 Çalışma tasarımı gerçekliği (evidence landscape)
Kılavuza göre A/BPO %5 için:

- doğrudan RCT kanıtı **sınırlı** olabilir,
- çalışmalar küçük örneklem/kısa takipli olabilir,
- split-face/bilateral tasarımlar sık olabilir.

Bu nedenle ana yaklaşım:

- **random-effects**,
- küçük k için **HKSJ (Hartung–Knapp)**,
- tasarıma göre **ayrı sentez** (RCT vs non-RCT vs tek kollu; klinik popülasyon vs sağlıklı gönüllü),
- split-face için **paired** hesaplar ve korelasyon senaryoları.

**Seed set örnekleri (scoping; Sprint 1 retrieval sanity check):**
- Zheng et al., 2018 — randomize split-face (paired), 28 gün; A/BPO %5 vs %2 supramoleküler salisilik asit
- Andres et al., 2008 — sağlıklı gönüllü split-face tolerabilite; BPO dozu (%2,5/%5/%10) irritasyon farkı (dolaylı kanıt)

## 1.3 Metodolojik standartlar (raporlama + arama)
- PRISMA 2020 raporlama kontrol listesi zorunlu.
- PRISMA-S arama stratejisi raporlanması ve PRESS kalite kontrolü uygulanır.
- Observational veri dahil olursa MOOSE ilkeleri ek raporlama çerçevesidir.

## 1.4 PICOS (kılavuzla hizalı)

| Bileşen | Tanım |
|---|---|
| P | Akne vulgaris hastaları (tüm yaş/cilt tipi) |
| I | Adapalen %0,1 + BPO %5 (FDC jel ve/veya protokolde tanımlı eşzamanlı kullanım) |
| C | Vehikül/plasebo, BPO %5, adapalen %0,1, A/BPO %2,5, diğer topikal tedaviler |
| O | Güvenlilik/tolerabilite çıktıları (SoF çekirdeği + ikinciller) |
| S | RCT öncelikli; ayrıca uygun non-RCT ve tek kollu seriler (n≥10) |

> Not: Sağlıklı gönüllü tolerabilite/dose-assessment çalışmaları (varsa) yalnızca **ayrı sentez/özel analiz** modüllerinde kullanılır; primary SoF’e girmez.

## 1.5 SoF çekirdeği (≤7 çıktı)
SoF tablosu için önerilen çekirdek (kılavuz):

1. **AE nedeniyle tedavi kesilmesi**
2. **Orta–şiddetli lokal irritasyon**
3. **Eritem**
4. **Kuruluk/deskuamasyon**
5. **Yanma/batma**
6. **Kontakt dermatit** (irritan/alergjik)
7. **SAE**

> PIH/pigmentasyon gibi çıktılar veri azsa SoF dışı ikincil/narratif raporlanır.

---

# 2) Teslimatlar (Deliverables) ve başarı kriterleri (Done)

## 2.1 Ana teslimatlar
1. **Tek kaynaklı protokol config**: `config/protocol.yml`
2. **Sapma yönetimi**: `logs/protocol_changes.csv`
3. **Arama stratejileri**: `screening/search_strategies/` (tüm DB sorguları)
4. **Arama günlükleri**: `logs/search_log.csv` (tarih/saat, sorgu, sonuç sayısı, export formatı)
5. **Kayıt havuzu + dedup raporu**: `screening/records_master.csv`, `screening/dedup_report.md`
6. **Screening kararları**: `screening/screening_decisions.csv` + gerekçeler + kappa
7. **Tam metin arşivi**: `data/raw/pdfs/` + dönüştürülmüş MD: `out/marker-md/`
8. **Extraction DB**: `extraction/extracted_data.csv` + veri sözlüğü
9. **Sentez hazırlığı (Cochrane çerçevesi)**: `report/characteristics_included_studies.md`, `analysis/synthesis_matrix.csv`, `analysis/input/*.csv`
10. **RoB**: `rob/rob2_results.csv` (result-level gerekçeli), `rob/robins_i.csv` (gerekiyorsa)
11. **Analiz çıktıları**: `analysis/results/`, `analysis/plots/` (forest/funnel/prediction interval)
12. **GRADE girdileri + SoF**: `grade/grade_inputs.csv`, `report/sof_table.*`
13. **PRISMA 2020 raporu**: `report/manuscript.qmd` + `report/supplements/`
14. **QA / reprodüksiyon paketi**: `renv.lock`, `logs/`, çıktı hash’leri

## 2.2 Done kriterleri
- Protokol kararları tek dosyada (`config/protocol.yml`) ve değişiklikler loglanmış.
- Screening + extraction + RoB, en az **iki bağımsız** değerlendirici ile yürütülmüş, uyuşmazlıklar kayıtlı.
- SoF çekirdeğindeki her çıktı için **outcome 5 bileşen tanımı** (domain/ölçüm/metrik/toplulaştırma/zaman) + zaman penceresi kuralı tanımlı ve extraction’da uygulanmış.
- Analiz pipeline tek komutla yeniden üretilebilir (`make all` veya `targets`).
- PRISMA 2020 checklist %100 tamam; ek materyaller eksiksiz.
- SoF çıktıları için RoB gerekçeleri ve GRADE kararları dokümante.
- PRISMA-S arama stratejisi raporu ve PRESS onayı dokümante.

---

# 3) Tech stack (önerilen mimari)

## 3.1 R ekosistemi (istatistik + reprodüksiyon)
**Zorunlu**

- R (>= 4.3 önerilir)
- `renv` (paket sürüm kilidi)

**Meta-analiz**

- `meta` (ana iş akışı: `metabin`, `metacont`, `metagen`, `metaprop`, `forest`, `funnel`, `update.meta`, `metareg`, `metabias`, `trimfill`)
- `metafor` (ileri yöntemler: `rma`, `gosh`, selection model `selmodel`, esnek dönüşüm/çok düzeyli modeller)
- `dmetar` (diagnostics: `find.outliers`, `InfluenceAnalysis`, yardımcı plot/araçlar)

**NMA (opsiyonel)**

- `netmeta` (frequentist NMA)

**Veri işleme**

- `tidyverse`, `readxl`, `janitor`
- (ops.) `arrow` (büyük veri/kolon bazlı format)

**Raporlama**

- Quarto (`quarto` CLI)
- `knitr`, `rmarkdown`
- `gt` / `gtsummary` (tablo üretimi)

**Kalite/tekrarlanabilirlik**

- `sessionInfo()` çıktısının rapora eklenmesi
- Sabit seed (rastgelelik içeren adımlarda)

## 3.2 PDF → metin çıkarımı
Repo standardı:

- Python venv: `.venv-marker/`
- marker-pdf kurulumu: (Sprint 0 ile) `scripts/marker_setup.sh` **veya** manuel kurulum
- batch dönüştürme: (Sprint 0 ile) `scripts/marker_batch.sh` (PDF klasörü → MD klasörü)

Alternatif/ek (opsiyonel):

- GROBID (bibliyografik metadata)
- Tabula/Camelot (tablo çıkarımı)

## 3.3 Proje orkestrasyonu
İki seçenek:

1) Basit: `Makefile` (öneri: başlangıç için)
2) Gelişmiş: R `targets` (pipeline bağımlılık yönetimi ve cache)

## 3.4 CI/QA (opsiyonel ama önerilir)
- GitHub Actions ile:
  - `renv::restore()`
  - analiz pipeline çalıştırma
  - çıktı artefact yayınlama (hash ile)

---

# 4) API entegrasyonları (ne zaman, neden, nasıl)

> Not: Bazı veri tabanları (Embase/WoS/Scopus/CENTRAL) genelde **kurumsal** erişim + export ile yürütülür. API yoksa “export + import standardı” yaklaşımı kullanılır.

## 4.1 Literatür tarama API’leri

### PubMed / NCBI E-utilities
**Amaç:** arama otomasyonu, PMID listesi, metadata çekimi.

- R: `rentrez`
- Çıktı:
  - `data/raw/search/pubmed_<date>.json`
  - `screening/exports/pubmed_<date>.ris`
- Log:
  - `logs/search_log.csv` (query + tarih + sonuç sayısı)

### Scopus / Elsevier (Search + Retrieval + Metadata)

**Amaç (Sprint 1–2 odaklı):**
- Sprint 1: Scopus’ta programatik arama ile kayıt listesi almak (PRISMA-S uyumlu log).
- Sprint 2: Dedup sonrası kalan kayıtlar için DOI/PMID/EID üzerinden metadata zenginleştirmek.
- (Opsiyonel) Atıf sinyali: citation count / citations overview.

**API aileleri ve önerilen endpoint’ler**
- **Search:** `GET https://api.elsevier.com/content/search/scopus`
- **Retrieval (abstract metadata):**
  - `GET https://api.elsevier.com/content/abstract/doi/{doi}`
  - `GET https://api.elsevier.com/content/abstract/pubmed_id/{pubmed_id}`
  - `GET https://api.elsevier.com/content/abstract/eid/{eid}`
- **Metadata (atıf/dergi doğrulama):**
  - `GET https://api.elsevier.com/content/abstract/citation-count`
  - `GET https://api.elsevier.com/content/abstract/citations`

**Kimlik doğrulama / sır yönetimi**
- Header: `X-ELS-APIKey: ${ELSEVIER_API_KEY}`
- Kurumsal aboneliğe bağlı olarak `InstToken` gerekebilir (gerekirse `.env`’de `ELSEVIER_INSTTOKEN`).

**Çıktı standardı**
- Ham API çıktısı: `data/raw/search/scopus_<date>.json`
- Normalize edilmiş tablo/RIS: `screening/exports/scopus_<date>.ris` (veya CSV)
- Log: `logs/search_log.csv` içine `source=Scopus`, `interface=API`, `query=...`, `results_total=...`.

**Not (VIEW):** Elsevier API’lerde `view` parametresi ile dönen alanlar değişebilir ve bazı view’ler abonelik kapsamına göre kısıtlıdır.

### Crossref
**Amaç:** DOI çözümleme, metadata zenginleştirme, dedup destek.

- R: `rcrossref`
- Çıktı: `data/raw/metadata/crossref_<date>.json`

### OpenAlex / Semantic Scholar
**Amaç:** citation chasing (ileri/geri atıf), ilgili çalışmalar.

- Çıktı: `data/raw/metadata/openalex_<date>.json` vb.
- Not: rate limit ve lisans koşulları; kullanım loglanır.

## 4.2 Arama kalite güvencesi
- PRESS kontrol checklist’i `screening/search_strategies/press_checklist.md` olarak saklanır.
- “Last search date / cut-off”: `logs/search_log.csv` içindeki en son `datetime_utc` kaydıdır (raporda ayrıca açık yazılır).

## 4.3 Klinik çalışma kayıtları

### ClinicalTrials.gov
**Amaç:** yayınlanmamış/verisi eksik çalışmaların tespiti.

- Çıktı: `data/raw/registries/ctgov_<date>.json`

### WHO ICTRP / EudraCT
**Amaç:** global kayıt taraması, unpublished evidence.

- Genelde portal tabanlı: manuel tarama + log.

## 4.4 Regülatif dokümanlar

### FDA Drugs@FDA / EMA EPAR
**Amaç:** güvenlilik sinyali, alt analiz, raporlama destek.

- Yaklaşım: doküman indirme → marker-pdf → extraction.

## 4.5 Referans yönetimi

### Zotero + Better BibTeX
**Amaç:** tek kaynak referans havuzu, otomatik BibTeX/RIS export.

- Çıktı:
  - `screening/library.bib`
  - `screening/library.ris`

---

# 5) Faz/Sprint planı (uygulama takvimi)

Önerilen sprint süresi: **1–2 hafta**. Toplam süre, veri hacmine göre değişir.

## Sprint 0 — Repo ve yürütme iskeleti (kılavuz Milestone 0)

### Hedef
Reprodüksiyon + denetlenebilirlik + “tek kaynaklı gerçek” altyapısını kur.

### Adımlar
1) `config/protocol.yml` oluştur (aşağıdaki başlıkları içerecek):
   - araştırma sorusu (0. bölüm)
   - PICOS
   - SoF çekirdeği
   - advers etkiler yaklaşımı: confirmatory / exploratory / hibrit + exploratory raporlama kuralı
   - outcome 5 bileşen standardı (domain/ölçüm/metrik/toplulaştırma/zaman) + zaman penceresi kuralı
   - dahil/dışla kriterleri
   - zaman noktası kuralı
   - pairwise vs single-arm karar kuralları
   - istatistik varsayılanları: RE+HKSJ, τ² (REML/PM), heterojenite raporu
   - split-face paired kuralları + r senaryoları
   - multi-arm ve cluster/crossover kuralları
   - NMA devreye alma koşulları
   - publication bias eşiği (k≥10)
2) Klasör standardı:
   - `data/raw`, `data/processed`, `screening/`, `extraction/`, `rob/`, `analysis/`, `report/`, `logs/`
3) `scripts/` iskeleti:
   - `scripts/doctor.sh` (opsiyonel: `scripts/marker_setup.sh`, `scripts/marker_batch.sh`)
4) `renv` başlat + kilitle.
   - `renv::init()` / `renv::snapshot()` standardı
   - Analiz script standardı: `analysis/scripts/00_prepare_inputs.R`, `analysis/scripts/10_pairwise_binary.R`, `analysis/scripts/20_pairwise_continuous.R`, `analysis/scripts/30_single_arm.R`
5) Audit log şemasını oluştur:
   - `{who, when, stage, evidence_pointer, decision, rationale}`
6) Pipeline komutlarını tanımla (Make/targets).

### Teslimatlar
- `config/protocol.yml`
- `renv.lock`
- klasörler
- `scripts/doctor.sh` (opsiyonel: `scripts/marker_setup.sh`, `scripts/marker_batch.sh`)
- `logs/audit_log.csv` (veya jsonl)

### Başarı kriterleri
- Dummy veri ile pipeline çalıştırılabilir.

### HITL kapısı
- **Protocol freeze**: bu sprint sonunda protokol config “dondurulur”.

---

## Sprint 1 — Arama stratejisi, kayıt ve PROSPERO (kılavuz Milestone 1)

### Hedef
Arama stratejilerini çoğaltılabilir şekilde üret, seed check yap, PROSPERO taslağını çıkar.

### Adımlar
1) Her DB için query üret ve kaydet:
   - PubMed/MEDLINE
   - Embase
   - CENTRAL
   - Web of Science
   - Scopus
   - Uygulama notları: `ARAMA-VERI-KAYNAKLARI-VE-API-ERISIMI.md`
2) Arama yönetimi:
   - sorgu metni, tarih/saat, sonuç sayısı, export formatı log.
3) Seed sanity check:
   - Seed set retrieval: Zheng 2018, Andres 2008 arama sonuçlarında yakalanıyor mu? (bkz. `META-ANALIZ-KILAVUZU.md` Bölüm 1.1)
4) Gri literatür kaynak listesi.
5) PROSPERO kayıt metni taslağı.
6) PRESS kalite kontrol ve PRISMA-S rapor taslağı.

### Teslimatlar
- `screening/search_strategies/*.txt`
- `logs/search_log.csv`
- `report/prospero_draft.md`
- `screening/search_strategies/press_checklist.md`
- `report/prisma_s_report.md`

### Başarı kriterleri
- Tüm DB’ler için arama tekrarlanabilir; seed çalışmaları yakalanıyor.
- PRESS checklist tamamlanmış ve arama stratejisi onaylanmış.

### HITL kapısı
- **Search strategy final** onayı (bilgi uzmanı/PI).

---

## Sprint 2 — Dedup + kayıt havuzu + PRISMA sayıları (kılavuz Milestone 2 / 1. parça)

### Hedef
Tekilleştirilmiş master kayıt havuzu ve otomatik PRISMA sayıları.

### Adımlar
1) Export import standardı (RIS/CSV alan haritalama).
2) Dedup:
   - DOI exact match
   - PMID exact match
   - Title fuzzy + yıl + yazar kontrolü
3) Kalıcı `record_id` üret.
4) PRISMA counts otomasyonu.

### Teslimatlar
- `screening/records_master.csv`
- `screening/dedup_report.md`
- `report/prisma_counts.json`

### Başarı kriterleri
- Aynı çalışma farklı kaynaklardan gelince tekilleşiyor.

### HITL kapısı
- Dedup raporu gözden geçirme (yanlış merge kontrolü).

---

## Sprint 3 — Screening (title/abstract + full-text) (kılavuz Milestone 2 / 2. parça)

### Hedef
Include/exclude karar seti + gerekçeler + kappa.

### Araçlar
- Rayyan veya Covidence (önerilir)
- Alternatif: CSV tabanlı minimal süreç

### Adımlar
1) Pilot tarama (50–100 kayıt): kriter rafine.
2) Tam tarama:
   - include/exclude/unclear + dışlama kodu
3) Uyuşmazlık çözümü (3. hakem).
4) Kappa veya yüzde uyum.
5) Tam metin listesi ve PDF temini.

### Teslimatlar
- `screening/screening_decisions.csv`
- `screening/fulltext_needed.csv`
- PRISMA flow girdileri
- `screening/exclusion_codebook.md`

### Başarı kriterleri
- Kayıtların %100’ü kararlandı; kappa raporlandı.

### HITL kapısı
- Unclear kayıtlar için adjudication oturumu.

---

## Sprint 4 — Full-text ingestion + veri çıkarımı (kılavuz Milestone 3)

### Hedef
Extraction DB’yi doldur, iz sürülebilirliği garanti et.

### Adımlar
1) PDF arşivi düzeni:
   - `data/raw/pdfs/`
2) marker-pdf ile PDF→MD:
   - çıktı: `out/marker-md/`
3) Extraction form + data dictionary:
   - split-face, multi-arm, single-arm alanları
   - zaman noktaları
   - outcome 5 bileşen alanları + zaman penceresi
   - AE saptama yöntemi (aktif izlem/spontan), denominator (safety/ITT/PP), risk penceresi
4) Çift extraction:
   - SoF çıktılarında %100 çift kontrol
5) Evidence pointer:
   - `pdf:page`, `table`, `figure`, `supplement` zorunlu
6) Çoklu rapor/CSR/regülatif kaynak birleştirme:
   - aynı çalışmanın tüm raporları tek `study_id` altında toplanır; çelişkiler “ana kaynak” + gerekçe ile işaretlenir.
7) Eksik veri listesi + yazar iletişim şablonları.
8) Sentez hazırlığı (Cochrane):
   - “Characteristics of included studies” tablosu
   - çıktı/karşılaştırma bazlı `synthesis_matrix.csv` (k, n, zaman noktası, ölçüm aracı)
9) Analize hazır girdiler:
   - `analysis/input/pairwise_binary.csv`, `analysis/input/pairwise_continuous.csv`, `analysis/input/generic_iv.csv`, `analysis/input/single_arm.csv`

### Teslimatlar
- `extraction/extraction_form.xlsx` (veya CSV)
- `extraction/extracted_data.csv`
- `extraction/missing_data_requests.md`
- `extraction/data_dictionary.csv`
- `logs/extraction_changes.md`
- `report/characteristics_included_studies.md`
- `analysis/synthesis_matrix.csv`
- `analysis/input/*.csv`

### Başarı kriterleri
- Her veri noktası kanıt işaretçisi ile bağlı.

### HITL kapısı
- QA örneklem kontrolü (extraction ↔ PDF).

---

## Sprint 5 — RoB 2 / ROBINS-I + GRADE girdileri (kılavuz Milestone 4)

### Hedef
SoF çıktıları için result-level RoB gerekçeleri + GRADE domain girdileri.

### Adımlar
1) RCT vs non-RCT ayrımı.
2) RoB 2 (result-level) + gerekçe.
3) ROBINS-I (gerekiyorsa).
4) Seçici raporlama / “missing results” kontrolü:
   - registry/protokol/CSR ↔ yayın karşılaştırması; RoB 2 gerekçelerinde kullan.
5) GRADE domain girdisi taslağı.

### Teslimatlar
- `rob/rob2_results.csv`
- `rob/robins_i.csv` (ops.)
- `grade/grade_inputs.csv`

### Başarı kriterleri
- SoF 7 çıktı için RoB gerekçeleri tamam.

### HITL kapısı
- RoB consensus toplantısı.

---

## Sprint 6 — Pairwise + single-arm meta-analiz (kılavuz Milestone 5)

### Hedef
Kılavuzdaki istatistik kurallarla ana sonuçları üret.

### Analiz standartları (kılavuz)
- Model: random-effects
- Küçük k: HKSJ
- τ²:
  - sürekli: REML
  - ikili: Paule–Mandel
- Rapor: Q, I², τ², prediction interval
- Duyarlılık:
  - leave-one-out
  - yüksek RoB çıkar
  - fixed vs random
  - τ² alternatifleri
  - RR vs OR
- Split-face:
  - paired
  - korelasyon yoksa r=0.25/0.5/0.75
- Seyrek olay:
  - continuity correction stratejisi + duyarlılık
- Publication bias:
  - k≥10 ise funnel + testler
- Klinik anlamlılık:
  - önceden tanımlı eşikler + NNH raporu

### R uygulama standardı (kitaplarla uyumlu)
1) Analiz girdilerini yükle: `analysis/input/*.csv`
2) Pairwise ikili çıktılar (primer RR):
   - `meta::metabin(sm = "RR", method = "MH", method.tau = "PM", hakn = TRUE)`
   - OR duyarlılığı: `update.meta(m, sm = "OR")`
3) Pairwise sürekli çıktılar:
   - ham mean/SD varsa: `meta::metacont(sm = "MD"|"SMD", method.smd="Hedges", method.tau="REML", hakn=TRUE)`
   - TE+SE varsa (paired/cross-over/adjusted): `meta::metagen(...)`
4) Single-arm oranlar:
   - `meta::metaprop(sm = "PLOGIT", method = "GLMM")` (raw havuzlamadan kaçın)
5) Robustluk:
   - `dmetar::find.outliers(m)` + `dmetar::InfluenceAnalysis(m, random = TRUE)`
   - τ² duyarlılığı: `update.meta(m, method.tau = "REML")` vb.
6) Publication bias / small-study effects (k≥10 ise):
   - `funnel.meta(m)` (opsiyonel contour-enhanced)
   - `metabias(m, method.bias = "linreg")` (sürekli/generic) veya `method.bias = "peters"` (ikili)
   - `trimfill.meta(m)` yalnızca keşif/duyarlılık
7) Reprodüksiyon:
   - Her ana model objesini `saveRDS()` ile `analysis/results/models/*.rds` altına kaydet
   - Sonuç tablolarını `analysis/results/*.csv`, plotları `analysis/plots/` altına yaz

### Teslimatlar
- `analysis/scripts/*.R`
- `analysis/results/*.csv`
- `analysis/plots/forest_*.png`, `funnel_*.png`
- `analysis/results/clinical_thresholds.md`
- `analysis/results/sensitivity_summary.md` (özet tablo)
- `analysis/results/models/*.rds`

### Başarı kriterleri
- SoF çıktılarının her biri için nicel sonuç veya narratif eşik gerekçesi.

### HITL kapısı
- İstatistikçi doğrulaması + replikasyon.

---

## Sprint 7 — NMA (opsiyonel) (kılavuz Milestone 6)

### Gate koşulları
- Ağ bağlantılı (connected network)
- Transitivity makul
- Tutarlılık kontrol edilebilir

### Adımlar
1) Karar bağlamı (decision-making):
   - hedef popülasyon (hastalık evresi/önceki tedaviler) + “decision space” (hangi tedaviler arasında karar?) netleştir.
   - node tanımı (doz/formülasyon/uygulama rejimi/konkomitan tedaviler) finalize et; protokol sapması varsa logla.
2) “Unique set of trials” ile ağ kurulumu:
   - ağ geometrisini incele (spur/loop; bağlantısız bileşen var mı?).
   - “evidence space” için gerekli link tedavileri dahil et; sıralama/yorumları decision space’e odakla.
3) Transitivity risk matrisi:
   - temel etki değiştiriciler için (örn. akne şiddeti, yaş, takip süresi, eşlik eden bakım) dengesizlikleri değerlendir.
4) Tutarlılık (inconsistency) kontrolü:
   - lokal kontroller: node-splitting/Bucher mantığı (uygunsa)
   - global kontroller: design-by-treatment (uygunsa)
   - tutarsızlık varsa: node revizyonu, ağ daraltma, meta-regresyon/alt grup gibi yanıt stratejileri uygula ve gerekçelendir.
5) NMA ana analiz + rapor:
   - göreli etkiler (league table) + ağ grafiği
   - sıralama çıktıları (rank olasılıkları/SUCRA) **yalnızca belirsizlik farkındalığı** için
6) Göreli → mutlak etki:
   - hedef popülasyon için baseline risk varsayımı/kaynağı seç
   - decision-relevant çıktılar için mutlak risk/risk farkı/NNH tabloları üret.
7) NMA için certainty:
   - karar alanındaki kontrastlar için direct/indirect/network mantığıyla GRADE girdilerini derle (incoherence varsa düşürme düşün).

### Teslimatlar
- `analysis/nma/network_plot.*`
- `analysis/nma/league_table.*`
- `analysis/nma/rank_probs.*` (ops.)
- `analysis/nma/absolute_effects.*`
- `analysis/nma/inconsistency_checks.*`
- `analysis/nma/grade_nma_inputs.*` (ops.)
- `analysis/nma/models/*.rds` (ops.)

### Başarı kriterleri
- NMA yapılırsa tutarlılık raporlandı; yapılmazsa gerekçe loglandı.
- Ranking çıktıları “tek başına karar dayanağı değil” notuyla birlikte raporlandı.
- Decision-relevant çıktılar için mutlak etki tablosu (baseline risk varsayımıyla) üretildi.

---

## Sprint 8 — GRADE/SoF + PRISMA 2020 raporu (kılavuz Milestone 7)

### Hedef
Yayınlanabilir paket.

### Adımlar
1) SoF tablosu + GRADE certainty.
2) PRISMA 2020 checklist self-audit.
3) Manuskript (Quarto): Methods/Results/Discussion.
4) Ek materyaller (kılavuz Ek 1–7).

### Teslimatlar
- `report/manuscript.qmd` (PDF/Word çıktıları)
- `report/supplements/`
- `report/prisma_checklist_completed.*`

### Başarı kriterleri
- PRISMA 2020 tam uyum; SoF ve ekler tamam.

---

# 6) Operasyonel yönetim (loglama, versiyonlama, QA)

## 6.1 Protocol sapmaları
`logs/protocol_changes.csv`:

- `date`
- `change`
- `rationale`
- `impacted_section`
- `approved_by`

## 6.2 Audit log
Her kritik kararın kanıt bağlantısı:

- `evidence_pointer` (PDF sayfa/tablo/URL)
- `decision`
- `rationale`
- `who/when`

## 6.3 QA minimum set (kılavuz)
- Extraction ↔ PDF doğrulama (rastgele örneklem kontrol)
- Kod/çıktı replikasyonu
- Regülatif checklist (eğer ruhsat amaçlı kullanılacaksa)

## 6.4 Veri gizliliği ve paylaşım
- Kişisel veri içeriyorsa veri seti anonimize edilir ve erişim sınırları `logs/data_access.md` içinde dokümante edilir.
- Paylaşılabilir veri için “de-identification” notu rapor ekinde belirtilir.

---

# 7) Riskler ve mitigasyon (kılavuzla hizalı)

1) **k küçük / kısa takip** → RE+HKSJ, geniş CI, narratif eşik, GRADE imprecision
2) **Dolaylılık** → sağlıklı gönüllü vs klinik pop. ayrıştırma
3) **Split-face bağımlılığı** → paired + r senaryoları
4) **Ölçek heterojenliği** → SMD + yön standardizasyonu
5) **Eksik veri** → yazar iletişimi + konservatif imputasyon + belirsizlik bayrağı

---

# 8) Repo içinde “hemen başlamak” için ilk komutlar

0) Sprint 0 bootstrap (klasör + script iskeleti): `sprintler/SPRINT-0-BACKLOG.md`

1) Ortam teşhisi (Sprint 0 ile eklenir):

```bash
./scripts/doctor.sh
```

2) PDF pipeline kurulumu (opsiyonel; Sprint 0 ile eklenir):

```bash
./scripts/marker_setup.sh
```

3) PDF → Markdown dönüşümü örneği (opsiyonel):

```bash
./scripts/marker_batch.sh reference/Adaclin out/marker-md/adaclin
```

---

# 9) Notlar (repo bağlamı)

- Seed set (Zheng 2018; Andres 2008) yalnızca “scoping / retrieval sanity check” içindir; PRISMA sayıları resmî export + dedup + screening log’larından üretilmelidir.
- `sprintler/SPRINT-0-BACKLOG.md` repo bootstrap (klasör/Makefile/script şablonları) için pratik rehberdir.
- `ARAMA-VERI-KAYNAKLARI-VE-API-ERISIMI.md` arama kaynakları + API erişimi + PRISMA-S loglama standardı için pratik rehberdir.
