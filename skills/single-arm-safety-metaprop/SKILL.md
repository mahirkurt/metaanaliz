---
name: single-arm-safety-metaprop
description: Single-arm güvenlik sonuçları için metaprop (PLOGIT/GLMM) ve sıfır olay yönetimi SOP'u.
---

# Single-arm Safety Meta-analysis (metaprop)

## Amaç

Tek kollu advers event oranlarını (proportion) uygun dönüşüm ve model ile birleştirmek.

## Girdi

```json
{
  "studies": [
    {"study_id": "...", "event": 3, "total": 100, "follow_up": "12w"}
  ],
  "method": {"transform": "PLOGIT|FT", "model": "random", "ci": "HKSJ|DL"}
}
```

## Çıktı

```json
{
  "pooled_proportion": {"estimate": 0.03, "ci_low": 0.01, "ci_high": 0.06},
  "transform": "PLOGIT",
  "model": "random",
  "tau2": 0.01,
  "i2": 45,
  "notes": ["zero-event çalışmalarda continuity correction veya GLMM tercih"]
}
```

## SOP

1. Düşük/0 event durumlarında:
   - GLMM (binomial-normal) veya appropriate continuity correction.
2. Duyarlılık: farklı dönüşümler (PLOGIT vs FT).
3. Heterojenite raporu: I2, tau2.
