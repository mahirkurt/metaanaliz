---
name: risk-of-bias-robins-i
description: Non-randomize çalışmalar için ROBINS-I değerlendirme SOP'u ve çıktı şablonu.
---

# Risk of Bias — ROBINS-I (Non-randomized)

## Amaç

Gözlemsel / non-randomize çalışmalar için ROBINS-I ile bias değerlendirmesini standardize etmek.

## Çıktı şablonu

```json
{
  "study_id": "doi:...|pmid:...",
  "outcome": "...",
  "tool": "ROBINS-I",
  "domains": [
    {"domain": "confounding", "judgement": "low|moderate|serious|critical|no_info", "support": "...", "evidence_pointer": {}},
    {"domain": "selection_of_participants", "judgement": "low|moderate|serious|critical|no_info", "support": "...", "evidence_pointer": {}},
    {"domain": "classification_of_interventions", "judgement": "low|moderate|serious|critical|no_info", "support": "...", "evidence_pointer": {}},
    {"domain": "deviations_from_intended_interventions", "judgement": "low|moderate|serious|critical|no_info", "support": "...", "evidence_pointer": {}},
    {"domain": "missing_data", "judgement": "low|moderate|serious|critical|no_info", "support": "...", "evidence_pointer": {}},
    {"domain": "measurement_of_outcomes", "judgement": "low|moderate|serious|critical|no_info", "support": "...", "evidence_pointer": {}},
    {"domain": "selection_of_reported_result", "judgement": "low|moderate|serious|critical|no_info", "support": "...", "evidence_pointer": {}}
  ],
  "overall_judgement": "low|moderate|serious|critical|no_info",
  "notes": []
}
```

## Not

ROBINS-I confounding domain’u için protokole “minimum confounder set” (örn. yaş, hastalık şiddeti, baseline risk) eklemek önerilir.
