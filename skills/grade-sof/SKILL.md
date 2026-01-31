---
name: grade-sof
description: GRADE certainty değerlendirmesi ve Summary of Findings (SoF) tablosu üretimi için SOP ve çıktı formatı.
---

# GRADE + Summary of Findings (SoF)

## Amaç

Her kritik outcome için kanıt kesinliğini (certainty) GRADE ile derecelendirmek ve SoF tablosu üretmek.

## Girdi

- Meta-analiz sonuçları (effect, CI, heterojenite)
- RoB değerlendirmeleri
- İndirectness / imprecision / publication bias sinyalleri

## Çıktı (SoF JSON)

```json
{
  "sof": {
    "population": "...",
    "intervention": "...",
    "comparator": "...",
    "outcomes": [
      {
        "outcome": "...",
        "effect_measure": "RR|OR|MD|SMD",
        "relative_effect": {"estimate": 0.85, "ci_low": 0.72, "ci_high": 1.00},
        "absolute_effect": {"baseline_risk": 0.20, "risk_with_intervention": 0.17, "difference": -0.03},
        "n_participants": 1234,
        "n_studies": 5,
        "certainty": "high|moderate|low|very_low",
        "downgrade_reasons": ["risk_of_bias", "imprecision"],
        "notes": []
      }
    ]
  }
}
```

## SOP

1. Başlangıç certainty:
   - RCT: High
   - Observational: Low
2. Downgrade alanları: RoB, inconsistency, indirectness, imprecision, publication bias.
3. Upgrade (observational): large effect, dose-response, residual confounding.
