---
name: prisma-s-press-search-qa
description: PRISMA-S uyumlu arama raporlama + PRESS (Peer Review of Electronic Search Strategies) kalite kontrol checklist'i.
---

# PRISMA-S + PRESS Search QA

## Amaç

- Arama stratejisini **PRISMA-S**'e uygun raporlamak.
- Sorguların **PRESS** prensiplerine göre teknik kalite kontrolünü yapmak.

## Girdi

- Araştırma sorusu + PICO/PECO
- Kullanılan veri tabanları (EuropePMC/PubMed/Scopus/Embase/Semantic Scholar vb.)
- Her kaynak için query string + filtreler + tarih

## Çıktı (önerilen JSON)

```json
{
  "search_qa": {
    "protocol_id": "...",
    "run_id": "YYYYMMDD-HHMM",
    "databases": [
      {
        "name": "EuropePMC",
        "query": "...",
        "filters": {"year_from": null, "year_to": null},
        "ran_at": "YYYY-MM-DDTHH:mm:ssZ",
        "n_results": 1234
      }
    ],
    "press_check": {
      "translation_errors": [],
      "boolean_logic": [],
      "subject_headings": [],
      "text_word_searching": [],
      "spelling_syntax": [],
      "limits_filters": [],
      "overall_notes": []
    },
    "prisma_s_fields": {
      "information_sources": [],
      "full_strategies_reported": true,
      "date_last_searched": "YYYY-MM-DD"
    }
  }
}
```

## PRESS mini-checklist (uygulama)

1. Boolean/parentheses doğru mu? (AND/OR gruplama)
2. Field tags doğru mu? (title/abstract, MeSH vs)
3. Synonym/variant coverage yeterli mi?
4. Spelling/typo var mı?
5. Limits/filters protokole uygun mu? (yıl, dil, insan)
6. Çok daraltma var mı? (sıfır sonuç riski)
