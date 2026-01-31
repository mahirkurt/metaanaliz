---
name: missing-data-conversions
description: Eksik varyans ölçümlerinde SD/SE/CI/p-value dönüşümleri ve imputasyon SOP'u.
---

# Missing Data + SD/SE/CI Dönüşümleri SOP

## Amaç

Çalışmaların raporlamadığı SD gibi değerleri, raporlanan SE/CI/p-value/median-IQR gibi ölçülerden dönüştürmek ve audit edilebilir şekilde kaydetmek.

## Çıktı formatı

```json
{
  "study_id": "...",
  "outcome": "...",
  "reported": {"type": "SE|CI95|p_value|median_iqr", "value": "..."},
  "derived": {"sd": 12.3, "method": "sd = se * sqrt(n)"},
  "assumptions": ["normality"],
  "evidence_pointer": {},
  "notes": []
}
```

## Dönüşüm örnekleri

- SD = SE * sqrt(n)
- SE = (upper - lower) / (2 * 1.96)
- SD = SE * sqrt(n)

## SOP

1. Dönüşüm formülünü ve girdileri mutlaka kaydet.
2. Belirsizlik yüksekse duyarlılık analizi planla.
3. Median/IQR → mean/SD dönüşümü gerekiyorsa protokolde yöntem seç (örn. Wan/Luo).
