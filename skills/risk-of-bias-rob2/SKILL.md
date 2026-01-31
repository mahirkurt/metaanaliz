---
name: risk-of-bias-rob2
description: RCT'ler için RoB 2 domain bazlı değerlendirme SOP'u ve çıktı şablonu.
---

# Risk of Bias — RoB 2 (RCT)

## Amaç

Randomize kontrollü çalışmalar için RoB 2 ile bias değerlendirmesini standardize etmek.

## Girdi

- Çalışma PDF / full text
- Outcome tanımı (primary/secondary)

## Çıktı (domain bazlı)

```json
{
  "study_id": "doi:...|pmid:...",
  "outcome": "...",
  "tool": "RoB2",
  "domains": [
    {
      "domain": "randomization_process",
      "judgement": "low|some_concerns|high",
      "support_for_judgement": "...",
      "evidence_pointer": {"source_type":"pdf","source_locator":{"path":"..."},"location":{"page":2,"quote":"..."}}
    },
    {
      "domain": "deviations_from_intended_interventions",
      "judgement": "low|some_concerns|high",
      "support_for_judgement": "...",
      "evidence_pointer": {"source_type":"pdf","source_locator":{"path":"..."},"location":{"page":3,"quote":"..."}}
    },
    {
      "domain": "missing_outcome_data",
      "judgement": "low|some_concerns|high",
      "support_for_judgement": "...",
      "evidence_pointer": {"source_type":"pdf","source_locator":{"path":"..."},"location":{"page":5,"quote":"..."}}
    },
    {
      "domain": "measurement_of_outcome",
      "judgement": "low|some_concerns|high",
      "support_for_judgement": "...",
      "evidence_pointer": {"source_type":"pdf","source_locator":{"path":"..."},"location":{"page":6,"quote":"..."}}
    },
    {
      "domain": "selection_of_reported_result",
      "judgement": "low|some_concerns|high",
      "support_for_judgement": "...",
      "evidence_pointer": {"source_type":"pdf","source_locator":{"path":"..."},"location":{"page":7,"quote":"..."}}
    }
  ],
  "overall_judgement": "low|some_concerns|high",
  "notes": []
}
```

## SOP (kısa)

1. Her outcome için ayrı değerlendirme (ölçüm/eksik veri outcome’a bağlı).
2. Domain judgement + kısa gerekçe + evidence_pointer zorunlu.
3. Overall judgement: domain’lerin “worst case” yaklaşımı + tutarlı yorum.
