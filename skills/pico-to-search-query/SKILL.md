---
name: pico-to-search-query
description: PICO sorusunu veritabanı sorgularına (EuropePMC, preprint) dönüştürmek için standart adımlar ve çıktı formatı.
---

# PICO → Search Query

## Amaç

Bir PICO tanımını tekrarlanabilir, loglanabilir ve revize edilebilir arama sorgularına dönüştürmek.

## Girdi

- P (Population)
- I (Intervention)
- C (Comparator)
- O (Outcome)
- Zaman aralığı (opsiyonel)
- Çalışma tasarımı filtreleri (opsiyonel; RCT, cohort, vb.)
- Dil/insan/yaş grubu filtreleri (opsiyonel)

## Çıktı

Her kaynak için aşağıdaki alanları üreten bir JSON nesnesi:

```json
{
  "question": "...",
  "pico": {"P":"...","I":"...","C":"...","O":"..."},
  "queries": {
    "europepmc": {
      "query": "...",
      "filters": {"year_from": null, "year_to": null, "study_type": []}
    },
    "preprints": {
      "query": "...",
      "filters": {"server": ["biorxiv","medrxiv"]}
    }
  },
  "notes": ["..."],
  "version": "v1"
}
```

## Adımlar

1. Terimleri genişlet:
   - Eşanlamlılar (synonyms), kısaltmalar, varyant yazımlar
2. Terimleri gruplandır:
   - (P) AND (I) AND (C?) AND (O?) yaklaşımı; gereksiz daraltmadan kaçın
3. Filtre stratejisi:
   - Önce geniş, sonra iteratif daralt
4. Loglanabilirlik:
   - Query string + filtreler + tarih/saat + kaynak adı her zaman kaydedilmeli
