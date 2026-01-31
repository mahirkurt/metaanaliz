# logs/ — Şablonlar ve çalışma çıktıları

Bu klasör meta-analiz sürecindeki tüm denetlenebilir çıktıları tutmak için kullanılır.

## Önerilen akış

1. Arama çalıştırmaları: `search_log.csv`
2. Deduplikasyon sayımları: `dedup_report.json`
3. Kayıt eşlemeleri (canonical_id ↔ source_id): `record_map.jsonl`
4. Screening kararları: `screening_log.jsonl`
5. Audit trail (kanıt referanslı): `audit_log.jsonl`
6. Protokol değişiklikleri: `protocol_changes.csv`
7. PRISMA sayımları: `prisma_counts.json`

> Not: Bu dosyalar şablon olarak eklenmiştir; pipeline/agent’ler bu dosyaları doldurabilir.
