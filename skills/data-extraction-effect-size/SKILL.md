---
name: data-extraction-effect-size
description: Meta-analiz için veri çıkarımı (n, mean/sd, event counts) ve etki büyüklüğü seçimi için pratik rehber.
---

# Data Extraction & Effect Size

## Amaç

Meta-analize girecek çalışmalardan gerekli sayısal alanları standart biçimde çıkarmak.

## Minimum alan seti (öneri)

- Çalışma kimliği: DOI/PMID/başlık
- Tasarım: RCT, cohort, vb.
- Popülasyon özellikleri: yaş, cinsiyet, kriterler
- Kollar (arm) bazında:
  - Sürekli sonuçlar: n, mean, sd
  - İkili sonuçlar: event, total

## Etki büyüklüğü seçimi

- Binary: RR/OR (önceden protokolle sabitle)
- Continuous: MD/SMD

## Çıktı formatı (örnek)

```json
{
  "study_id": "PMID:...",
  "outcome": "...",
  "effect": {
    "type": "RR",
    "arm_1": {"event": 10, "total": 100},
    "arm_2": {"event": 20, "total": 100}
  },
  "notes": "..."
}
```
