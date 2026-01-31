---
name: dedup-record-manager
description: Çoklu kaynaklardan gelen kayıtları birleştirme, canonical ID üretme, deduplikasyon ve audit edilebilir record manager SOP'u.
---

# Deduplication & Record Manager

## Amaç

Farklı veri kaynaklarından (EuropePMC, PubMed, preprint, Scholar vb.) gelen kayıtların **tekil** hale getirilmesi, canonical kimliklendirme yapılması ve PRISMA sayımlarına uygun şekilde loglanması.

## Prensipler

- **Deterministik**: Aynı girdiden aynı canonical_id çıkmalı.
- **Geri izlenebilir**: Her canonical kaydın hangi kaynak kayıtlarından geldiği tutulmalı.
- **Kayıp veri toleransı**: DOI yoksa PMID/PMCID/Title+Year+FirstAuthor gibi fallback.

## Girdi

Kayıt listesi (JSON):

```json
{
  "records": [
    {
      "source": "EuropePMC",
      "source_id": "PMID:123456",
      "doi": "10.1000/xyz",
      "pmid": "123456",
      "title": "...",
      "year": 2022,
      "authors": ["A. Smith", "B. Jones"],
      "url": "...",
      "retrieved_at": "YYYY-MM-DDTHH:mm:ssZ"
    }
  ]
}
```

## Çıktı

1) Canonical kayıtlar

```json
{
  "canonical_records": [
    {
      "canonical_id": "doi:10.1000/xyz",
      "primary_ids": {"doi": "10.1000/xyz", "pmid": "123456", "pmcid": null},
      "title": "...",
      "year": 2022,
      "authors": ["A. Smith", "B. Jones"],
      "sources": [
        {"source": "EuropePMC", "source_id": "PMID:123456", "url": "..."},
        {"source": "SemanticScholar", "source_id": "...", "url": "..."}
      ],
      "match_confidence": "high|medium|low",
      "dedup_rule": "doi|pmid|title_year_author_fuzzy",
      "notes": []
    }
  ]
}
```

2) Deduplikasyon raporu (PRISMA için)

```json
{
  "dedup_report": {
    "input_records": 1000,
    "duplicates_removed": 250,
    "remaining": 750,
    "by_rule": {"doi": 200, "pmid": 30, "fuzzy": 20},
    "generated_at": "YYYY-MM-DDTHH:mm:ssZ"
  }
}
```

## SOP (önerilen eşleştirme sırası)

1. **DOI exact match** (normalize et: lower, trim, remove url prefix)
2. **PMID exact match**
3. **PMCID exact match**
4. **Title + year + first author** (normalize title: lowercase, punctuation removal)
5. Gerekirse **fuzzy title** (Levenshtein/Jaro-Winkler) + year tolerance (±1)

## Loglama

- `logs/search_log.csv`: arama düzeyi
- `logs/dedup_report.json`: dedup sayımları
- `logs/record_map.jsonl`: canonical_id ↔ source_id mapping (satır bazlı)
