---
name: prisma-logging
description: Arama ve eleme sürecini PRISMA uyumlu şekilde loglama yönergesi (query, dedup, screening, inclusion).
---

# PRISMA Logging

## Amaç

PRISMA akış şemasını üretmeye uygun şekilde arama ve eleme sayımlarını düzenli tutmak.

## Log öğeleri

1. Arama çalıştırma
   - kaynak, query, filtre, tarih, sonuç sayısı
2. Birleştirme ve duplikasyon temizliği
   - toplam, duplikasyon, kalan
3. Screening kararları
   - T/A include/exclude/maybe sayıları
4. Full-text kararları
   - include/exclude + gerekçeler

## Önerilen dosyalar

- `logs/search_log.csv` (halihazırda var)
- `logs/screening_log.jsonl` (eklenebilir)
- `logs/prisma_counts.json` (eklenebilir)
