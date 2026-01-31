# Elsevier / Scopus API erişim kapsamı raporu

- Tarih (UTC): **2026-01-31T13:36:09Z**
- API Key: **6385…7e30**
- Not: Bu rapor sadece HTTP durumları + servis hata kodlarına göre bir *erişim matrisi* çıkarır. Bazı uçlar için kurumsal abonelik/InstToken gerekebilir.

## Özet

Bu anahtarla gözlenen durum (kısa):

- ✅ Scopus **Search API** çalışıyor (query çalıştırma / listeleme).
- ✅ **Serial Title API** çalışıyor (dergi/ISSN metadata).
- ✅ **Abstract Retrieval** için **view=META** çalışıyor (sınırlı metadata).
- ❌ Abstract Retrieval **view=FULL / view=REF** yetkisiz (401 AUTHORIZATION_ERROR).
- ❌ **Citation Count** ve **Citations Overview** erişimi yok (403 AUTHENTICATION_ERROR: configuration insufficient).
- ✅ **Article Retrieval** için **view=META** çalışıyor (core metadata).
- ❌ Article Retrieval **view=FULL** bu servis için geçersiz (400 INVALID_INPUT).

## Test Matrisi (HTTP / hata kodları)

| Endpoint/Test | HTTP | service-error.statusCode | service-error.statusText |
|---|---:|---|---|
| Scopus Search (simple) /content/search/scopus | 200 |  |  |
| Scopus Search (phrase quotes) TITLE-ABS-KEY("benzoyl peroxide") | 200 |  |  |
| Scopus Search (phrase braces) {benzoyl peroxide} | 200 |  |  |
| ScienceDirect Search /content/search/sciencedirect | 401 | AUTHORIZATION_ERROR | The requestor is not authorized to access the requested view or fields of the resource |
| Serial Title Search /content/serial/title | 200 |  |  |
| (referans kayıt) EID | n/a | 2-s2.0-105026158625 | |
| (referans kayıt) DOI | n/a | 10.1016/j.compbiolchem.2025.108868 | |
| Abstract Retrieval view=META /content/abstract/eid/{eid} | 200 |  |  |
| Abstract Retrieval view=FULL /content/abstract/eid/{eid} | 401 | AUTHORIZATION_ERROR | The requestor is not authorized to access the requested view or fields of the resource |
| Abstract Retrieval view=REF /content/abstract/eid/{eid} | 401 | AUTHORIZATION_ERROR | The requestor is not authorized to access the requested view or fields of the resource |
| Citation Count /content/abstract/citation-count | 403 | AUTHENTICATION_ERROR | Requestor configuration settings insufficient for access to this resource. |
| Citations Overview /content/abstract/citations | 403 | AUTHENTICATION_ERROR | Requestor configuration settings insufficient for access to this resource. |
| Article Retrieval view=META /content/article/doi/{doi} | 200 |  |  |
| Article Retrieval view=FULL /content/article/doi/{doi} | 400 | INVALID_INPUT | View parameter specified in request is not valid |

## Yorum / Ne anlama geliyor?

- **Search API** erişimi olduğu için sistematik arama sorgularını (PRISMA-S) API ile çalıştırıp sonuç listesini alabilirsiniz.
- **Abstract Retrieval (META)** ile en azından temel bibliyografik alanlar ve bazı ilişkilendirmeleri çekebilirsiniz; fakat **FULL/REF** görünümleri için ayrıca yetki gerekiyor.
- **Citation** uçları (citation-count/citations) için portal tarafında hesabın/anahtarın ‘configuration settings’inin yükseltilmesi veya kurum/abonelik tanımlanması gerekiyor gibi görünüyor. Bu, çoğu kurumda **InstToken** veya abonelik ilişkisi gerektirir.
- **Article Retrieval (META)** core metadata döndürüyor; tam metin/ileri VIEW’lar bu anahtarda açık değil (veya bu servis için bu VIEW yok).

## Sonraki adım önerileri

1) Eğer hedefin Scopus atıf metrikleri ise (citation-count/citations): kurumunun Elsevier/Scopus aboneliği ile **InstToken** edinmen gerekebilir (veya API key ayarlarının yükseltilmesi).
2) Abstract Retrieval’da FULL view için: ‘Abstract Retrieval API’ tarafındaki erişim haklarını kontrol et (kurumsal entitlement).
3) ScienceDirect Search sonucu bu anahtarda kapalıysa: ScienceDirect entitlement gerekebilir.
