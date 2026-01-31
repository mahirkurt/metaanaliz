---
name: screening-inclusion-exclusion
description: Başlık/özet ve tam metin taraması için dahil etme/dışlama karar şeması ve kayıt formatı.
---

# Screening (Inclusion/Exclusion)

## Amaç

Sistematik taramada başlık/özet ve full-text düzeyinde kararları standardize etmek ve denetlenebilir hale getirmek.

## Kayıt formatı

Her kayıt için:

```json
{
  "record_id": "...",
  "source": "EuropePMC|Scholar|...",
  "stage": "title_abstract|full_text",
  "decision": "include|exclude|maybe",
  "reasons": ["population mismatch", "not comparative", "review article"],
  "reviewer": "agent|human",
  "timestamp": "YYYY-MM-DDTHH:mm:ssZ",
  "notes": "..."
}
```

## Kurallar

- Dışlama gerekçesi mutlaka kodlanmalı (reasons boş bırakılmaz).
- “Maybe” kayıtları bir sonraki iterasyonda tekrar ele alınır.
