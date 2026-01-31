# Strateji-1 (Cline/VS Code) — BioContextAI Knowledgebase MCP + Skill-to-MCP + Paper-Search MCP

Bu repo için önerilen minimum kurulum:

- **Knowledgebase MCP**: literatür + biyomedikal kaynaklara araç (tool) erişimi
- **Skill-to-MCP**: bu repo içindeki `skills/` SOP/şablonlarını LLM’e MCP “resource” olarak sunar
- **Paper-Search MCP**: çoklu kaynaktan arama + PDF indirme/okuma (Semantic Scholar API key destekli)

> Not: Bu kurulum **Cline/VS Code MCP** standardına göre `.vscode/mcp.json` ile yapılır.

---

## 0) Önkoşullar

- Python (tercihen 3.11+)
- `uv` / `uvx`

Bu workspace’te `uv/uvx` yolu:

- `~/.local/bin/uv`
- `~/.local/bin/uvx`

Eğer terminaliniz `uvx` görmüyorsa:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## 1) uv/uvx kurulumu (bir kere)

```bash
python -m pip install --user uv
```

Doğrulama:

```bash
~/.local/bin/uv --version
~/.local/bin/uvx --version
```

---

## 2) MCP konfigürasyonu (VS Code / Cline)

Bu repo’da hazır dosya:

- `.vscode/mcp.json`

İçeriği üç server tanımlar:

1. `biocontext_kb` (Knowledgebase)
2. `meta-analysis-skills` (Skill-to-MCP, `skills/` klasörü)
3. `paper-search` (paper-search-mcp; `search` ve `fetch` başta olmak üzere çoklu tool)

VS Code içinde MCP özelliğini etkinleştirdikten sonra bu dosya otomatik keşfedilmelidir.

---

## 3) Skills klasörü

Repo’da örnek skill’ler mevcut:

- `skills/pico-to-search-query/SKILL.md`
- `skills/screening-inclusion-exclusion/SKILL.md`
- `skills/data-extraction-effect-size/SKILL.md`
- `skills/prisma-logging/SKILL.md`

Eklenen süreç-hizalı skill’ler:

- `skills/dedup-record-manager/SKILL.md`
- `skills/prisma-s-press-search-qa/SKILL.md`
- `skills/protocol-freeze-change-log/SKILL.md`
- `skills/audit-log-evidence-pointer/SKILL.md`
- `skills/risk-of-bias-rob2/SKILL.md`
- `skills/risk-of-bias-robins-i/SKILL.md`
- `skills/grade-sof/SKILL.md`
- `skills/split-face-paired-design/SKILL.md`
- `skills/single-arm-safety-metaprop/SKILL.md`
- `skills/missing-data-conversions/SKILL.md`

Yeni SOP eklemek için:

1. `skills/<skill-adi>/` klasörü aç
2. İçine `SKILL.md` koy
3. YAML frontmatter alanlarını doldur:

```md
---
name: my-skill
description: Ne işe yarar, ne zaman kullanılır?
---
```

---

## 4) Hızlı terminal doğrulaması

### 4.1 Skill-to-MCP (resource server)

```bash
export PATH="$HOME/.local/bin:$PATH"
uvx --python 3.12 skill_to_mcp --skills-dir "$(pwd)/skills"
```

Beklenen: process çalışır ve MCP stdio üzerinden istemci bağlantısı bekler.

### 4.2 Knowledgebase MCP

```bash
export PATH="$HOME/.local/bin:$PATH"
uvx --python 3.12 biocontext_kb@latest
```

Beklenen: process çalışır ve MCP stdio üzerinden istemci bağlantısı bekler.

### 4.3 Paper-Search MCP

Paper-search MCP bu repo’da `uvx --from paper-search-mcp python -m paper_search_mcp.server` şeklinde çalıştırılacak şekilde konfigüre edilmiştir.

Doğrulama:

```bash
export PATH="$HOME/.local/bin:$PATH"
uvx --python 3.12 --from paper-search-mcp python -m paper_search_mcp.server
```

Beklenen: process çalışır ve MCP stdio üzerinden istemci bağlantısı bekler.

> Not: İndirilen PDF’ler default olarak `.vscode/mcp.json` içindeki `PAPER_SEARCH_DOWNLOAD_DIR` dizinine iner.

---

## 5) Cline içinde kullanım ipuçları

### Ne zaman hangi server?

- **Süreç/SOP/şablon** ihtiyacı: `meta-analysis-skills`
  - “PICO’dan sorgu üret”
  - “Screening karar formatı nedir?”
  - “Etki büyüklüğü çıkarım şablonu ver”

- **Gerçek kaynak taraması / harici veri**: `biocontext_kb`
  - EuropePMC üzerinden arama
  - Preprint taraması

- **Multi-source arama + PDF indirme/okuma**: `paper-search`
  - `search`: Arxiv/PubMed/bioRxiv/medRxiv/Semantic Scholar/Crossref vb. çoklu kaynaktan arama
  - `fetch`: Seçilen kaydın detayını (mümkünse full-text/PDF’den okuma) getir

### En iyi pratik

- Arama çıktılarınızı `logs/search_log.csv` gibi bir dosyada saklayın.
- Her sonuç için kaynak linkini ve kimliği (PMID/DOI) tutun.
- Scholar/KEGG gibi kaynaklarda rate limit/lisans kısıtlarına dikkat edin.

---

## 6) Örnek akış (Cline prompt iskeleti)

Aşağıdaki akış, tool + skill kombinasyonunu pratikte göstermeyi amaçlar. (Cline prompt’unuza olduğu gibi yapıştırıp değiştirerek kullanabilirsiniz.)

### 6.1 PICO → sorgular → arama QA (PRISMA-S/PRESS)

1) `meta-analysis-skills` kaynağından PICO → query üret:

- Skill: `pico-to-search-query`

2) Üretilen query’leri çalıştır:

- `biocontext_kb` ile EuropePMC/preprint
- veya `paper-search` ile multi-source arama

3) Query’leri QA’dan geçir:

- Skill: `prisma-s-press-search-qa`

### 6.2 Dedup + screening log + evidence pointer

1) Kayıtları birleştir ve dedup yap:

- Skill: `dedup-record-manager`

2) Screening kararlarını standart formatta logla:

- Skill: `screening-inclusion-exclusion`
- Audit log standardı: `audit-log-evidence-pointer`

### 6.3 Full-text fetch + veri çıkarımı + RoB

1) Full text’i getir:

- `paper-search.search` ile sonuçları bul
- `paper-search.fetch` ile seçtiğin `id` için detay getir

2) Veri çıkarımı:

- Skill: `data-extraction-effect-size`
- Eksik veri dönüşümü gerekiyorsa: `missing-data-conversions`

3) Risk of bias:

- RCT: `risk-of-bias-rob2`
- Non-randomize: `risk-of-bias-robins-i`

### 6.4 Analiz sonrası GRADE + SoF

- Skill: `grade-sof`

---

## 7) Log dosyalarını CLI ile doldurma (repo-local tools/)

Bu repo `tools/` altında stdlib tabanlı küçük bir CLI içerir:

```bash
python -m tools.prisma_log -h
```

### 7.1 PRISMA sayaçları

```bash
python -m tools.prisma_log prisma-set --field screening.records_screened --value 120
python -m tools.prisma_log prisma-set --field identification.records_removed_before_screening.duplicates --value 35
python -m tools.prisma_log prisma-add-excluded --reason "wrong population" --n 12
```

### 7.2 Screening kararları (JSONL append)

```bash
python -m tools.prisma_log screening-append \
  --record-id "doi:10.1000/xyz" \
  --source EuropePMC \
  --stage title_abstract \
  --decision exclude \
  --reasons "not comparative|wrong population"
```

### 7.3 Audit log (kanıt referanslı JSONL append)

```bash
python -m tools.prisma_log audit-append \
  --action screening_decision \
  --record-id "doi:10.1000/xyz" \
  --payload-json '{"decision":"exclude"}' \
  --evidence-json '{"source_type":"database_record","source_locator":{"url":"https://..."},"location":{}}'
```

### 7.4 Protokol değişikliği (CSV append)

```bash
python -m tools.prisma_log protocol-change-append \
  --section "Analysis.Model" \
  --old-value "DL" \
  --new-value "HKSJ" \
  --reason "Small k" \
  --impact-assessment "CI widen" \
  --approved-by "PI"
```

