# SPRINT-0-BACKLOG — Milestone 0
## Repo ve Yürütme İskeleti (Reproducible + Auditable Meta-Analiz Pipeline)

**Kaynaklar:**
- `META-ANALIZ-KILAVUZU.md` → Ek A / Milestone 0 + Bölüm 14 (AI-Agent pipeline) + Bölüm 13 (QA)
- `META-ANALIZ-ICRA-PLANI.md` → Sprint 0 hedefleri/teslimatlar/kriterler
- Seed set (Zheng 2018; Andres 2008) → `META-ANALIZ-KILAVUZU.md` Bölüm 1.1 (Sprint 1 retrieval sanity check)

**Amaç:**
Sprint 0 bilimsel analiz yapmaz; **reprodüksiyon, denetlenebilirlik ve tek kaynaklı gerçek (SSOT)** altyapısını kurar.

---

# 0) Sprint meta

## 0.1 Sprint adı
Sprint 0 / Milestone 0: **Repo ve yürütme iskeleti**

## 0.2 Sprint çıktı hedefi (high-level)
Sprint sonunda repo şunları sağlamalı:

1. **Tek kaynaklı protokol config’i:** `config/protocol.yml`
2. **Standart klasör yapısı:** `data/`, `screening/`, `extraction/`, `rob/`, `analysis/`, `report/`, `logs/`…
3. **R ortam kilidi:** `renv.lock` (minimum paket seti)
4. **Audit log şeması + örnek kayıtlar**
5. **Pipeline komutları:** `Makefile` ile “uçtan uca” iskelet (dummy veriyle)
6. **Reprodüksiyon kanıtı:** çıktı manifest + hash
7. **Metodolojik kalite işaretleri:** PRISMA-S/PRESS hazırlığı + dışlama kod sözlüğü şablonu

## 0.3 Tanımlar
- **SSOT:** Protokol kararlarının tek dosyada tutulması (`config/protocol.yml`).
- **Audit log:** Kritik kararların `{who, when, stage, evidence_pointer, decision, rationale}` formatıyla izlenmesi.
- **HITL:** İnsan onayı olmadan kritik kararların final olmaması.

---

# 1) Hedefler, teslimatlar, başarı kriterleri

## 1.1 Hedef
**Reprodüksiyon + denetlenebilirlik + SSOT altyapısı** kurulumu.

## 1.2 Teslimatlar (Deliverables)
- `config/protocol.yml`
- `logs/protocol_changes.csv`
- `logs/audit_log.csv`
- Standart klasör yapısı
- `scripts/doctor.sh` (ortam doğrulama)
- (ops.) `scripts/marker_setup.sh`, `scripts/marker_batch.sh` (PDF→metin)
- `renv.lock`
- `Makefile` + dummy analiz scripti
- `logs/output_manifest.sha256`
- `screening/search_strategies/press_checklist.md`
- `screening/exclusion_codebook.md`

## 1.3 Başarı kriterleri (Done)
- Protokol kararları tek dosyada ve parse edilebilir.
- Audit log ve protocol change log mevcut.
- `make all` sıfır exit code ile tamamlanıyor.
- Dummy çıktı üretildi ve manifest oluşturuldu.

## 1.4 HITL kapısı
- **Protocol Freeze:** Sprint sonunda `config/protocol.yml` PI onayı.

---

# 2) Görevler (Sprint 0 Backlog)

## 2.0 Repo script iskeleti (`scripts/`)
**Amaç:** Kılavuz ve icra planında referans verilen “tek komut” işlerini standartlaştırmak.

**Komut:**
```bash
mkdir -p scripts
```

### `scripts/doctor.sh` (kopyala-yapıştır)
```bash
#!/usr/bin/env bash
set -euo pipefail

hr() { printf '\n%s\n' '------------------------------------------------------------'; }
say() { printf '%s\n' "$*"; }
has() { command -v "$1" >/dev/null 2>&1; }

show_cmd() {
  local name="$1"
  if has "$name"; then
    # Bazı komutlar --version çıktısını stderr’e basar.
    local v
    v="$("$name" --version 2>&1 | sed -n '1p' || true)"
    say "[OK] $name: ${v:-version unknown}"
  else
    say "[MISSING] $name"
  fi
}

hr
say "Meta-Analysis repo doctor (environment diagnostics)"
say "pwd: $(pwd)"
hr

show_cmd python
show_cmd pip
show_cmd R
show_cmd Rscript
show_cmd quarto
show_cmd make
show_cmd git

hr
say "Notes:"
say "- R/Quarto yoksa analiz/raporlama adımları çalışmaz; önce kurulum yapılmalıdır."
say "- Bu script bilgilendiricidir; mümkün olduğunca non-fatal davranır."
```

### (Opsiyonel) `scripts/marker_setup.sh` ve `scripts/marker_batch.sh`
Bu repo’da PDF→metin dönüşümü için `marker-pdf` yaklaşımı kullanılıyorsa, script şablonları `META-ANALIZ-ICRA-PLANI.md` Bölüm 3.2 ile uyumlu şekilde Sprint 0’da eklenebilir.

---

## 2.1 Ortam doğrulaması (doctor)
**Amaç:** R/Python/Quarto ve temel bağımlılıkları doğrula.

**Komut:**
```bash
./scripts/doctor.sh | tee logs/doctor_$(date +%Y%m%d_%H%M).txt
```

**Kabul kriterleri:**
- Fatal hata yok; varsa `logs/doctor_*.txt` ile dokümante.

---

## 2.2 Klasör standardını oluştur
**Amaç:** Kılavuzdaki klasör standardını tek doğru yapı olarak kurmak.

**Komut:**
```bash
mkdir -p config \
  data/raw data/processed \
  screening/exports screening/search_strategies \
  extraction rob grade \
  analysis/scripts analysis/results analysis/plots \
  report/supplements \
  out logs
```

**Doğrulama:**
```bash
find config data screening extraction rob grade analysis report out logs -maxdepth 2 -type d | sort
```

**Kabul kriterleri:**
- Tüm klasörler mevcut.

---

## 2.3 SSOT protokol config’i oluştur (`config/protocol.yml`)
**Amaç:** Protokol kararlarını tek YAML dosyasında toplamak.

**Not:** Bu dosya Sprint sonunda **freeze** edilir; değişiklikler `logs/protocol_changes.csv` ile loglanır.

**Dosya şablonu (kopyala-yapıştır):**
```yaml
meta:
  title: "A/BPO %5 (Adapalene 0.1% + Benzoyl Peroxide 5%) Safety & Tolerability Meta-Analysis"
  version: "v0.1"
  created_at: "YYYY-MM-DD"
  timezone: "Europe/Istanbul"
  owners:
    - name: "PI"
      role: "principal_investigator"
    - name: "Reviewer-1"
      role: "reviewer"
    - name: "Reviewer-2"
      role: "reviewer"

research_question:
  scope_one_sentence: >-
    A/BPO %5 topikal kombinasyonunun güvenlilik/tolerabilite profilini karşılaştırmalı meta-analiz ve
    kanıt sınırlıysa tek kollu güvenlilik meta-analizi ile sentezlemek; gerekirse NMA ile bağlamsallaştırmak.

picos:
  population: "Akne vulgaris hastaları (tüm yaş grupları, tüm cilt tipleri)"
  intervention:
    - "Adapalene 0.1% + Benzoyl Peroxide 5% fixed-dose combination (topikal)"
    - "Protokolde tanımlı eşzamanlı kullanım (adapalene 0.1% + BPO 5%)"
  comparators:
    - "vehicle/placebo"
    - "BPO 5% monoterapi"
    - "adapalene 0.1% monoterapi"
    - "A/BPO 2.5%"
    - "diğer topikal akne tedavileri"
  study_designs:
    include:
      - "RCT"
      - "non-RCT/quasi-experimental"
      - "cohort"
      - "single-arm case series (n>=10)"
    exclude:
      - "in vitro/animal"
      - "case report (n<10)"

sof_core_outcomes:
  max_n: 7
  outcomes:
    - id: "discontinuation_due_to_ae"
      label: "AE nedeniyle tedavi kesilmesi"
      type: "binary"
      priority: 1
    - id: "moderate_severe_local_irritation"
      label: "Orta-şiddetli lokal irritasyon"
      type: "binary_or_ordinal"
      priority: 2
    - id: "erythema"
      label: "Eritem"
      type: "binary_or_continuous"
      priority: 3
    - id: "dryness_scaling"
      label: "Kuruluk/deskuamasyon"
      type: "binary_or_continuous"
      priority: 4
    - id: "burning_stinging"
      label: "Yanma/batma"
      type: "binary_or_continuous"
      priority: 5
    - id: "contact_dermatitis"
      label: "Kontakt dermatit"
      type: "binary"
      priority: 6
    - id: "sae"
      label: "Ciddi advers olay (SAE)"
      type: "binary"
      priority: 7

timepoints:
  primary_timepoint_rule: "önceden belirlenen ana zaman noktası; birden fazla varsa protokol kuralına göre seçilir"
  preferred_windows:
    - label: "week_1"
      range_days: [5, 10]
    - label: "week_2_4"
      range_days: [11, 28]
    - label: "week_8_12"
      range_days: [56, 84]
    - label: "week_24_52"
      range_days: [168, 364]

analysis_plan:
  primary_track: "pairwise"
  secondary_track: "single_arm"
  effect_measures:
    binary:
      primary: "RR"
      alternatives: ["OR", "RD"]
    continuous:
      same_scale: "MD"
      different_scale: "SMD_Hedges_g"
  model_defaults:
    main: "random_effects"
    small_k_ci: "HKSJ"
    tau2:
      continuous: "REML"
      binary: "Paule-Mandel"
      sensitivity: ["DerSimonian-Laird"]
  heterogeneity_reporting: ["Q", "I2", "tau2", "prediction_interval"]
  publication_bias:
    min_k: 10
    methods: ["funnel_plot", "egger_or_peters"]

special_designs:
  split_face:
    handle_as_paired: true
    assumed_correlations: [0.25, 0.5, 0.75]
  multi_arm:
    avoid_double_counting: true
    approach: "split_shared_control_or_multivariate"
  clustered:
    adjust_for_design_effect: true
  crossover:
    prefer_paired: true

nma:
  enabled: false
  enable_conditions:
    - "connected_network"
    - "transitivity_plausible"
    - "consistency_check_passable"

paths:
  raw_data_dir: "data/raw"
  processed_data_dir: "data/processed"
  screening_dir: "screening"
  extraction_dir: "extraction"
  rob_dir: "rob"
  analysis_dir: "analysis"
  report_dir: "report"
  logs_dir: "logs"
```

**Kabul kriterleri:**
- YAML parse edilebilir.
- PICOS + SoF + analiz varsayılanları + özel tasarım kuralları mevcut.
- PRISMA-S/PRESS ve dışlama kodları yapılandırma notu içerir.

---

## 2.4 Protokol sapma günlüğü (`logs/protocol_changes.csv`)
**Amaç:** Protokol değişikliklerini izlemek.

**Şablon:**
```csv
date,change,rationale,impacted_section,approved_by
```

**Kural:** `config/protocol.yml` değişirse aynı commit’te güncelle.

---

## 2.5 Audit log altyapısı (`logs/audit_log.csv`)
**Amaç:** Denetlenebilirlik için her kritik karar kanıta bağlanmalı.

**Şablon:**
```csv
who,when,stage,evidence_pointer,decision,rationale
"system","YYYY-MM-DDTHH:MM:SS+03:00","bootstrap","N/A","created_audit_log","Initial scaffold"
```

**evidence_pointer standardı:**
- PDF: `pdf:<filename>#page=<n>`
- Tablo: `pdf:<filename>#page=<n>#table=<id>`
- Web: `url:<https://...>`

**Kabul kriterleri:**
- Dosya mevcut ve en az 1 kayıt içeriyor.

---

## 2.6 R ortam kilidi (renv)
**Amaç:** R paket sürümlerini kilitlemek.

**Komutlar:**
```bash
Rscript -e 'if (!requireNamespace("renv", quietly=TRUE)) install.packages("renv", repos="https://cloud.r-project.org")'
Rscript -e 'renv::init(bare=TRUE)'
Rscript -e 'renv::install(c("meta","metafor","dmetar","netmeta","tidyverse","readxl","janitor","knitr","rmarkdown"))'
Rscript -e 'renv::snapshot()'
```

**Doğrulama:**
```bash
test -f renv.lock && echo "renv.lock OK"
Rscript -e 'cat("R version:", R.version.string, "\n"); renv::status()'
```

---

## 2.7 Pipeline orkestrasyonu (Makefile + dummy analiz)
**Amaç:** Tek komutla çalıştırılabilir iskelet.

**Makefile şablonu:**
```makefile
.PHONY: help doctor dirs renv_restore dummy_data analysis_dummy report_dummy all

help:
	@echo "Targets:" \
	  "\n  doctor         - Run environment diagnostics" \
	  "\n  dirs           - Create standard directories" \
	  "\n  renv_restore   - Restore R packages from renv.lock" \
	  "\n  dummy_data     - Create minimal dummy dataset" \
	  "\n  analysis_dummy - Run a placeholder analysis script" \
	  "\n  report_dummy   - Render placeholder report (optional)" \
	  "\n  all            - Run everything (bootstrap pipeline)"

doctor:
	./scripts/doctor.sh | tee logs/doctor_$$(date +%Y%m%d_%H%M).txt

dirs:
	mkdir -p config \
	  data/raw data/processed \
	  screening/exports screening/search_strategies \
	  extraction rob grade \
	  analysis/scripts analysis/results analysis/plots \
	  report/supplements \
	  out logs

renv_restore:
	Rscript -e 'renv::restore()'

dummy_data:
	Rscript -e 'write.csv(data.frame(x=1:3, y=c(0.1,0.2,0.3)), "data/processed/dummy.csv", row.names=FALSE)'

analysis_dummy:
	Rscript analysis/scripts/00_dummy_analysis.R

report_dummy:
	@echo "(optional) Add Quarto render target later"

all: doctor dirs renv_restore dummy_data analysis_dummy
	@echo "Bootstrap pipeline done"
```

**Dummy analiz scripti (`analysis/scripts/00_dummy_analysis.R`):**
```r
df <- read.csv("data/processed/dummy.csv")

out <- list(
  n = nrow(df),
  mean_y = mean(df$y),
  created_at = format(Sys.time(), tz = "Europe/Istanbul")
)

dir.create("analysis/results", showWarnings = FALSE, recursive = TRUE)
writeLines(jsonlite::toJSON(out, auto_unbox = TRUE, pretty = TRUE), "analysis/results/dummy_summary.json")

cat("Wrote analysis/results/dummy_summary.json\n")
```

> Not: `jsonlite` eklemek için:
```bash
Rscript -e 'renv::install("jsonlite"); renv::snapshot()'
```

---

## 2.9 Metodolojik kalite artefaktları
**Amaç:** Sprint 1 için PRISMA-S/PRESS ve dışlama kodlarını hazır şablonlarla güvence altına almak.

**Şablonlar:**
- `screening/search_strategies/press_checklist.md`
- `screening/exclusion_codebook.md`

**Kabul kriterleri:**
- Şablonlar repo içinde mevcut ve Sprint 1 başlangıcında doldurulabilir.

---

## 2.8 Reprodüksiyon kanıtı (output manifest)
**Amaç:** Çıktıların hash’ini saklamak.

**Komut:**
```bash
find analysis/results data/processed -type f -maxdepth 2 -print0 | xargs -0 sha256sum | sort > logs/output_manifest.sha256
```

**Kabul kriterleri:**
- `logs/output_manifest.sha256` oluştu.

---

# 3) HITL Onay Kapısı (Sprint 0 kapanış)

**Checklist (PI/ekip onayı):**
- [ ] `config/protocol.yml` içerik kontrolü (PICOS + SoF + analiz varsayılanları)
- [ ] `logs/protocol_changes.csv` mevcut ve header doğru
- [ ] `logs/audit_log.csv` mevcut ve satır formatı doğru
- [ ] Klasör standardı oluşturulmuş
- [ ] `renv.lock` oluşturulmuş
- [ ] `make all` çalışıyor
- [ ] PRISMA-S/PRESS şablonları ve dışlama kod sözlüğü hazır

**Onay formatı (`logs/audit_log.csv`):**
```csv
"PI","YYYY-MM-DDTHH:MM:SS+03:00","protocol_freeze","config/protocol.yml","approved","Sprint 0 freeze"
```

---

# 4) Sprint 1’e geçiş notu (Seed sanity check)

Sprint 1’de arama stratejileri hazırlanırken **seed sanity check** için aşağıdaki ana çalışmaların yakalandığı doğrulanacak:

- Zheng et al., 2018 (split-face RCT)
- Andres et al., 2008 (split-face tolerabilite)

**Kaynak:** `META-ANALIZ-KILAVUZU.md` Bölüm 1.1 (seed set / scoping)
