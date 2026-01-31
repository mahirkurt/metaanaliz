---
name: audit-log-evidence-pointer
description: Her karar/çıkarım için kanıt referansı (evidence_pointer) standardı ve JSONL audit log formatı.
---

# Audit Log + Evidence Pointer Standardı

## Amaç

LLM/insan kararlarının ve çıkarımlarının her zaman bir kanıt parçasına (PDF sayfa, satır, tablo, DOI/PMID linki, query run) bağlanması.

## evidence_pointer şeması (öneri)

```json
{
  "evidence_pointer": {
    "source_type": "pdf|html|abstract|database_record",
    "source_locator": {
      "path": "data/raw/pdfs/.../paper.pdf",
      "url": "https://...",
      "document_id": "doi:...|pmid:..."
    },
    "location": {
      "page": 4,
      "table": "Table 2",
      "figure": null,
      "quote": "verbatim excerpt..."
    }
  }
}
```

## Audit log (JSONL) formatı

`logs/audit_log.jsonl` her satır bir event:

```json
{
  "timestamp": "YYYY-MM-DDTHH:mm:ssZ",
  "actor": "agent|human",
  "action": "screening_decision|data_extraction|risk_of_bias|analysis_choice",
  "record_id": "canonical_id|source_id",
  "payload": {},
  "evidence_pointer": {"source_type":"pdf","source_locator":{"path":"..."},"location":{"page":4}},
  "notes": "..."
}
```
