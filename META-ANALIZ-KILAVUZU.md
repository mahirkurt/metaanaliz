# Adapalen %0,1 + Benzoil Peroksit %5 (A/BPO %5) Güvenlilik ve Tolerabilite Meta-Analizi
## Birleşik Protokol + Metodolojik Kılavuz + AI-Agent Uygulama Haritası (v3)

> Bu doküman, proje için **SSOT (single source of truth)** niteliğinde; protokol kararlarını, metodolojik standartları ve AI-agent pipeline/TODO backlog’u **tek yerde** birleştirir. Uygulama fazları için `META-ANALIZ-ICRA-PLANI.md`, arama otomasyonu için `ARAMA-VERI-KAYNAKLARI-VE-API-ERISIMI.md` esas alınır.
>
> **Amaç:** İnsan denetimini koruyan (human-in-the-loop), yeniden üretilebilir (reproducible) ve PRISMA 2020 + Cochrane Handbook ilkeleriyle uyumlu; analizleri **R (meta/metafor/dmetar)** ile yürütülen bir meta-analiz hattını standartlaştırmak.

---

## İçindekiler

- [0. Kapsam (tek cümle)](#0-kapsam-tek-cümle)
- [1. Evidence landscape (seed haritası) ve protokol sonuçları](#1-evidence-landscape-seed-haritası-ve-protokol-sonuçları)
- [2. Protokol geliştirme, ön-kayıt ve yönetişim](#2-protokol-geliştirme-ön-kayıt-ve-yönetişim)
- [2.4 Metodolojik standartlar ve raporlama çerçevesi](#24-metodolojik-standartlar-ve-raporlama-çerçevesi)
- [3. PICOS ve çıktı önceliklendirme (SoF çekirdeği)](#3-picos-ve-çıktı-önceliklendirme-sof-çekirdeği)
- [4. Sistematik literatür taraması](#4-sistematik-literatür-taraması)
- [4.4 Arama kalite güvencesi ve güncelleme](#44-arama-kalite-güvencesi-ve-güncelleme)
- [5. Çalışma seçimi (screening) ve PRISMA akışı](#5-çalışma-seçimi-screening-ve-prisma-akışı)
- [5.4 Dışlama kodları ve karar sözlüğü](#54-dışlama-kodları-ve-karar-sözlüğü)
- [6. Veri çıkarımı ve veri yönetimi](#6-veri-çıkarımı-ve-veri-yönetimi)
- [6.5 Veri sözlüğü, versiyonlama ve gizlilik](#65-veri-sözlüğü-versiyonlama-ve-gizlilik)
- [7. Yanlılık riski değerlendirmesi (RoB 2 / ROBINS-I)](#7-yanlılık-riski-değerlendirmesi-rob-2-robins-i)
- [8. İstatistiksel sentez (pairwise + single-arm)](#8-istatistiksel-sentez-pairwise-single-arm)
- [8.7 Klinik anlamlılık ve eşik değerler](#87-klinik-anlamlılık-ve-eşik-değerler)
- [8.8 R ile analiz uygulaması (R: meta/metafor/dmetar)](#88-r-ile-analiz-uygulaması-r-meta-metafor-dmetar)
- [9. Özel tasarımlar ve teknik kurallar (split-face vb.)](#9-özel-tasarımlar-ve-teknik-kurallar-split-face-vb)
- [10. Network Meta-Analiz (NMA) modülü — ne zaman devreye alınır?](#10-network-meta-analiz-nma-modülü-ne-zaman-devreye-alınır)
- [11. GRADE ve Summary of Findings (SoF)](#11-grade-ve-summary-of-findings-sof)
- [12. Raporlama (PRISMA 2020) ve ek materyaller](#12-raporlama-prisma-2020-ve-ek-materyaller)
- [13. Regülatif uyum ve kalite güvencesi (QA)](#13-regülatif-uyum-ve-kalite-güvencesi-qa)
- [14. AI-Agent destekli uygulama haritası (pipeline)](#14-ai-agent-destekli-uygulama-haritası-pipeline)
- [15. Zaman çizelgesi, ekip ve sorumluluklar](#15-zaman-çizelgesi-ekip-ve-sorumluluklar)
- [16. Riskler, varsayımlar ve mitigasyon](#16-riskler-varsayımlar-ve-mitigasyon)
- [17. Özel analizler (temporal tolerabilite, doz-yanıt)](#17-özel-analizler-temporal-tolerabilite-doz-yanıt)
- [18. Hedef dergiler](#18-hedef-dergiler)
- [19. Potansiyel zorluklar ve çözümler](#19-potansiyel-zorluklar-ve-çözümler)
- [Ek A. TODO Backlog (uygulanabilir görev listesi)](#ek-a-todo-backlog-uygulanabilir-görev-listesi)
- [Ek B. Yazılım ve araçlar](#ek-b-yazılım-ve-araçlar)
- [Ek C. Hızlı sorun giderme (VS Code / Cline Terminal)](#ek-c-hızlı-sorun-giderme-vs-code-cline-terminal)
- [Kaynaklar](#kaynaklar)

---

## 0) Kapsam (tek cümle)

A/BPO %5 topikal kombinasyonunun **lokal irritasyon**, **advers olay (AE) nedeniyle tedavi kesilmesi** ve **ciddi advers olay (SAE)** başta olmak üzere güvenlilik/tolerabilite profilini; uygun olduğunda **karşılaştırmalı meta-analiz** ve kanıt sınırlı ise **tek kollu (single-arm) güvenlilik meta-analizi** ile sentezlemek; gerekiyorsa daha geniş topikal akne tedavi ağında **network meta-analiz (NMA)** ile bağlamsallaştırmak.

---

## 1) Evidence landscape (seed haritası) ve protokol sonuçları

### 1.1 Doğrudan A/BPO %5 klinik veri sinyali
Ön kanıt haritası (seed evidence map) ve mevcut literatür işaretleri, A/BPO **%5** için doğrudan klinik verinin sınırlı olabileceğini; büyük ölçekli faz II–III RCT literatürünün çoğunlukla A/BPO **%2,5** etrafında yoğunlaştığını düşündürür.

**Seed set (scoping; PRISMA sayısı değildir):**
Aşağıdaki çalışmalar, konuya dair erken “işaret” setidir; Sprint 1’de arama stratejisinin duyarlılık kontrolü (retrieval sanity check) ve protokol alt grup hipotezleri için kullanılır. Nihai dahil/çıkar kararı Sprint 3–4’te full-text üzerinden verilir.

| Çalışma | Popülasyon | Tasarım (unit-of-analysis) | Müdahale / karşılaştırıcı | Takip | Projede kullanımı |
|---|---|---|---|---|---|
| Zheng et al., 2018 | Akne vulgaris (n=31) | Randomize split-face; open-label (paired) | A/BPO %5 vs %2 supramoleküler salisilik asit | 28 gün | Primary pairwise (paired) + kısa süre alt grubu; bariyer ölçütleri varsa ikincil |
| Andres et al., 2008 | Sağlıklı gönüllü (n=60) | Bilateral split-face; doz değerlendirme (paired) | A/BPO jelinde BPO dozu (%2,5 vs %5 vs %10) | Kısa tolerabilite dönemi | Özel analiz 17.2 (doz-yanıt) + dolaylı tolerabilite sinyali (primary SoF’e girmez) |

**Protokol etkisi:**
- Küçük örneklem ve kısa takip süreleri sık görülebileceğinden **random-effects** ana yaklaşım olmalıdır.
- Kesinlik (imprecision) ve dolaylılık (indirectness) nedeniyle GRADE’de düşürme olasılığı artar.
- Tasarıma göre ayrı sentez ihtiyacı kuvvetlenir (karşılaştırmalı vs. tek kollu; klinik akne popülasyonu vs. sağlıklı gönüllüler).

### 1.2 Tipik çalışma tipleri
- Split-face / bilateral tasarımlar (aynı bireyde iki farklı topikal rejim; örn. Zheng 2018).
- Açık etiketli, tek kollu veya pragmatik uygulama serileri.
- Sağlıklı gönüllülerde tolerabilite ve doz değerlendirme (dolaylı kanıt; örn. Andres 2008).

### 1.3 Kanıt boşlukları
- ≥12 hafta üstü uzun dönem güvenlilik verisi sınırlı.
- Büyük ölçekli faz III RCT eksikliği.
- Yaş uçlarında (çocuk/yaşlı) ve belirli cilt tiplerinde veri azlığı.
- Doğrudan karşılaştırmalı kanıt, heterojen aktif karşılaştırıcılarla gelebilir → havuzlama sınırlı kalabilir; gerektiğinde NMA/narratif sentez.
- BPO konsantrasyonu ile irritasyon arasında doz-yanıt ilişkisi olası (%5’in %2,5’e göre daha irritan olabileceği sinyali).
- Non-English literatür erişim/çeviri kaynak ihtiyacı doğurabilir.

---

## 2) Protokol geliştirme, ön-kayıt ve yönetişim

### 2.1 PROSPERO kaydı
Meta-analiz protokolü PROSPERO’ya kaydedilmelidir. Kayıt; metodolojik şeffaflığı artırır ve protokol sapmalarının izlenebilirliğini sağlar.

**Kayıt için çekirdek bilgiler:**
- Çalışma başlığı ve araştırma sorusu
- Dahil etme/dışlama kriterleri
- Primer/sekonder çıktılar ve zaman noktası seçim kuralları
- Veri çıkarım yaklaşımı ve çift kontrol planı
- Yanlılık riski (RoB) değerlendirme yöntemi
- Planlanan istatistiksel analizler (pairwise, single-arm, NMA koşulları)

### 2.2 Ön-kayıt (preregistration) ve sapma yönetimi
Protokolde aşağıdaki karar kuralları **başlangıçta** tanımlanır:
- Birincil/ikincil sonlanımlar ve önceliklendirme
- Birden fazla zaman noktası varsa “hangi zaman noktası ana analiz” kuralı
- Etki ölçütleri ve dönüşüm kuralları (RR/OR/RD; MD/SMD; log dönüşümler)
- Varsayılan model: random-effects + küçük örneklem düzeltmesi
- Heterojenite raporlama standardı (I², τ², prediction interval)
- Alt grup/meta-regresyon değişkenleri (önceden belirlenmiş)
- Eksik veri stratejileri ve duyarlılık analizleri
- Yayın yanlılığı/küçük çalışma etkisi testleri için eşik (genellikle k≥10)

**Protokol sapmaları** için değişiklik günlüğü tutulur:
- `{tarih, değişiklik, gerekçe, etkilediği sonuç/bölüm, onaylayan kişi}`

### 2.3 Çalışma yönetimi ve denetlenebilirlik
- En az iki bağımsız araştırmacı ile tarama ve veri çıkarımı.
- Kritik adımlarda üçüncü araştırmacı/hakem ile uyuşmazlık çözümü.
- Kararların kanıt parçasına bağlanması (PDF sayfa no, tablo, ek veri, kayıt numarası).

### 2.4 Metodolojik standartlar ve raporlama çerçevesi
- **PRISMA 2020** kontrol listesi (raporlama) ve **PRISMA-S** (arama stratejisi raporu) birlikte takip edilir.
- **MOOSE** ilkeleri (observational veri varsa) ek raporlama standardı olarak kullanılır.
- **Cochrane Handbook** önerileri (özellikle RoB, heterojenite ve analiz seçimleri) karar noktası olarak referanslanır.
- Protokol değişiklikleri ve sapmaları, PRISMA 2020 “Protocol and registration” maddeleriyle eşleştirilerek raporda özetlenir.

---

## 3) PICOS ve çıktı önceliklendirme (SoF çekirdeği)

### 3.1 PICOS

| Bileşen | Tanım |
|---------|-------|
| **P (Population)** | Akne vulgaris tanısı almış hastalar (tüm yaş grupları, tüm cilt tipleri) |
| **I (Intervention)** | Adapalen %0,1 + Benzoil peroksit %5 sabit doz kombinasyonu (topikal jel) **ve/veya** eşzamanlı uygulama (protokolde tanımlı koşullarla) |
| **C (Comparator)** | Vehikül/plasebo, BPO %5 monoterapisi, adapalen %0,1 monoterapisi, A/BPO %2,5, diğer retinoid/BPO kombinasyonları, diğer topikal tedaviler |
| **O (Outcomes)** | Güvenlilik/tolerabilite çıktıları (aşağıdaki SoF çekirdeği ve ikincil çıktılar) |
| **S (Study Design)** | RKÇ’ler öncelikli; ayrıca yarı-deneysel/kohort ve uygun tek kollu seriler (n≥10) — tasarıma göre ayrı sentez planı ile |

**Analiz için ön tanımlı gruplanma (seed sinyali ile hizalı):**
- A/BPO %5 **FDC (tek tüp)** ve A/BPO %5 **separate-application (iki ürün)** klinik olarak ayrıştırılır (alt grup / NMA node tanımı).
- **Klinik akne popülasyonu (primary)** ile **sağlıklı gönüllü tolerabilite** çalışmaları (secondary/indirect) karıştırılmaz; sağlıklı gönüllüler yalnızca ayrı sentez/özel analiz modüllerine girer.
- Takip süresi önceden sınıflanır: **≤4 hafta**, **5–12 hafta**, **>12 hafta** (uzun dönem boşluğu raporlanır).

### 3.2 Summary of Findings (SoF) için öncelikli çıktılar (≤7)
SoF tablosu için “hasta açısından önemli” ve protokolün omurgasını oluşturan 5–7 çıktı seçilir.

**Önerilen SoF çekirdeği (7 sınırı):**
1. **AE nedeniyle tedavi kesilmesi**
2. **Orta–şiddetli lokal irritasyon** (çalışma tanımıyla)
3. **Eritem**
4. **Kuruluk/deskuamasyon**
5. **Yanma/batma (stinging/burning)**
6. **Kontakt dermatit** (irritan/alergjik)
7. **Ciddi advers olay (SAE)**

> Not: PIH/pigmentasyon gibi çıktılar (özellikle Fitzpatrick IV–VI) çalışma sayısı düşükse SoF dışı ikincil/narratif olarak raporlanabilir.

### 3.3 Birincil ve ikincil analiz hatları
Kanıt sınırlılığı göz önüne alınarak iki paralel sentez hattı tanımlanır:
1) **Karşılaştırmalı meta-analiz (primary)**
2) **Tek kollu güvenlilik meta-analizi (secondary)**: yalnızca karşılaştırıcı içermeyen/tek kollu güvenlilik verileri için.

### 3.4 Advers etkiler (harms) yaklaşımı — confirmatory + exploratory (hibrit)
Cochrane yaklaşımı, advers etkiler için protokolde **yaklaşımı önceden belirtmeyi** önerir: *confirmatory* (önceden tanımlı çıktılar), *exploratory* (çalışmalarda geçen tüm/çok sayıda AE) veya *hibrit*.

Bu proje için yaklaşım:
- **Confirmatory (primer):** SoF çekirdeğindeki 5–7 güvenlilik çıktısı (ve protokolde ayrıca tanımlanan kritik AE’ler). Etki ölçütü + zaman noktası + analiz kuralı önceden belirlenir.
- **Exploratory (ikincil/sinyal):** dahil edilen çalışmalarda raporlanan diğer AE’ler; yalnızca sinyal taraması amacıyla “keşifsel” etiketle raporlanır (çoklu karşılaştırma riski nedeniyle).
- **Seçim kuralı (exploratory raporlama):** (i) klinik/regülatif olarak önemli, (ii) ≥2 çalışmada raporlanan veya (iii) olay yükü yüksek (örn. ≥%5) AE’ler önceliklendirilir; kalanlar ek materyalde listelenir.

> Not: AE tanımı/izlem yöntemi (aktif izlem vs spontan rapor) ve zaman penceresi değişken olabileceğinden extraction’da bu bilgiler ayrı alanlar olarak toplanır (bkz. 6.7).

---

## 4) Sistematik literatür taraması

> Bu bölümdeki veri tabanlarına **UI + export** ile erişim yanında, mümkün olan yerlerde **API/programatik erişim** ile yeniden üretilebilir arama yürütmek için ayrıca bkz:
> **`ARAMA-VERI-KAYNAKLARI-VE-API-ERISIMI.md`**

### 4.1 Veri tabanları ve kaynaklar

**Primer veri tabanları:** PubMed/MEDLINE, Embase, Cochrane CENTRAL, Web of Science, Scopus.

**Sekonder kaynaklar:** ClinicalTrials.gov, EudraCT, WHO ICTRP, FDA Drugs@FDA, EMA EPAR, ulusal ruhsat kaynakları (örn. TİTCK/Galenos).

**Gri literatür:** kongre özetleri, tezler, üretici teknik dosyaları, referans listesi taraması (snowballing) ve ileri/geri atıf taraması.

### 4.2 Arama stratejisi (örnek)
PubMed için örnek arama algoritması:

```txt
(("adapalene"[MeSH Terms] OR "adapalene"[Title/Abstract] OR "differin"[Title/Abstract])
AND
("benzoyl peroxide"[MeSH Terms] OR "benzoyl peroxide"[Title/Abstract] OR "BPO"[Title/Abstract])
AND
("5%"[Title/Abstract] OR "5 percent"[Title/Abstract] OR "50 mg/g"[Title/Abstract])
AND
("safety"[MeSH Subheading] OR "tolerability"[Title/Abstract] OR "adverse effects"[MeSH Subheading]
 OR "side effects"[Title/Abstract] OR "irritation"[Title/Abstract] OR "erythema"[Title/Abstract]
 OR "scaling"[Title/Abstract] OR "dryness"[Title/Abstract] OR "burning"[Title/Abstract] OR "stinging"[Title/Abstract]))
```

**Arama filtreleri:**
- Dil kısıtlaması: yok (gerekirse tercüme)
- Tarih kısıtlaması: başlangıçtan günümüze
- Yayın tipi kısıtlaması: yok (önce geniş, sonra tarama ile daraltma)

### 4.3 Arama yönetimi ve kayıt
- Her veri tabanı için: sorgu metni, tarih/saat, sonuç sayısı, export formatı kaydedilir.
- Arama güncellemesi: son analiz öncesi belirlenmiş bir zaman penceresinde tekrarlanır.
- Seed set kontrolü (scoping): Zheng et al., 2018; Andres et al., 2008 aramada yakalanıyor mu? (retrieval sanity check; bkz. 1.1)

### 4.4 Arama kalite güvencesi ve güncelleme
- **PRESS kontrolü** (bilgi uzmanı/ikinci araştırmacı) ile arama stratejisinin duyarlılık ve özgüllük dengesi gözden geçirilir.
- Arama güncellemesi için **cut-off tarihi** belirlenir ve “last search date” açıkça raporlanır.
- Gri literatür ve kayıt taramalarında tekrar üretilebilirlik için **kaynak listesi + erişim tarihi** loglanır.

### 4.5 (Uygulama notu) Scopus/Elsevier API ile yeniden üretilebilir arama

Scopus, projede “primer veri tabanı” olarak yer aldığından, mümkünse UI export’a ek olarak **Elsevier Developer Portal** üzerinden **API tabanlı** arama da yapılabilir. Bu, PRISMA-S kapsamında sorgu/sonuçların daha denetlenebilir şekilde loglanmasını kolaylaştırır.

**Bu repo için önerilen Elsevier API kapsamı:**
- **Search (discovery):** Scopus’ta sorgu çalıştırma ve kayıt listesi alma
  - `GET https://api.elsevier.com/content/search/scopus`
- **Retrieval (enrichment):** DOI/PMID/EID üzerinden abstrakt/metadata zenginleştirme
  - `GET https://api.elsevier.com/content/abstract/doi/{doi}`
  - `GET https://api.elsevier.com/content/abstract/pubmed_id/{pubmed_id}`
  - `GET https://api.elsevier.com/content/abstract/eid/{eid}`
- **Metadata (opsiyonel):** atıf sinyali ve kaynak başlığı doğrulama
  - `GET https://api.elsevier.com/content/abstract/citation-count`
  - `GET https://api.elsevier.com/content/abstract/citations`

**Kimlik bilgileri (repo standardı):**
- `.env` içinde `ELSEVIER_API_KEY` ve `ELSEVIER_EMAIL` tutulur.
- Kurumsal aboneliğe göre `InstToken` gerekebilir (örn. `.env` içinde `ELSEVIER_INSTTOKEN`).

**Loglama kuralı (PRISMA-S):**
- Scopus araması çalıştırıldığında `logs/search_log.csv` içine şu minimum alanlar yazılır:
  - `source=Scopus`, `interface=API`, `datetime_utc`, `query`, `filters`, `results_total`, `exported_format`, `notes`.

Detaylı erişim rehberi için: `ARAMA-VERI-KAYNAKLARI-VE-API-ERISIMI.md`.

---

## 5) Çalışma seçimi (screening) ve PRISMA akışı

### 5.1 PRISMA akış diyagramı
1. Tanımlama (Identification)
2. Tarama (Screening)
3. Uygunluk (Eligibility)
4. Dahil etme (Inclusion)

> Not: Consensus gibi AI arama araçlarından gelen “ham kayıt sayıları” PRISMA akışına taşınmaz. PRISMA sayıları yalnızca bu projede üretilen export + dedup + screening log’larından otomatik hesaplanır.

### 5.2 Bağımsız tarama ve kalibrasyon
- En az iki araştırmacı tarafından bağımsız başlık/özet ve tam metin taraması.
- Pilot tarama (örn. 50–100 kayıt) ile dahil/dışla kurallarının rafine edilmesi.
- Tarayıcılar arası uyum: Cohen’s kappa veya yüzde uyum.

### 5.3 Dahil etme/dışlama kriterleri

**Dahil etme:**
- Akne vulgaris hastaları (yaş/cinsiyet/etnisite kısıtlaması yok)
- (Sekonder/indirect) Sağlıklı gönüllü tolerabilite/dose-assessment çalışmaları: yalnızca ayrı sentez/özel analiz modülleri için (primary SoF’e girmez)
- A/BPO %5 sabit doz kombinasyonu **veya** protokolde tanımlı eşzamanlı kullanım
- En az bir güvenlilik/tolerabilite sonlanımı raporlanmış
- Çalışma tasarımı: RKÇ; ayrıca uygun non-RKÇ ve tek kollu seriler (n≥10)

**Dışlama:**
- BPO konsantrasyonu ≠ %5 (ana analiz için)
- Güvenlilik verisi olmayan yayınlar
- İn vitro/hayvan çalışmaları
- Vaka raporları (n<10)
- Aynı popülasyonun duplikasyon raporları
- Tam metin erişimi yok (veri çıkarımı yapılamıyorsa)

### 5.4 Dışlama kodları ve karar sözlüğü
- Her dışlama kararına **standardize kod** atanır (örn. `E01: Uygun popülasyon değil`, `E02: Müdahale uygunsuz`, `E03: Sonlanım yok`, `E04: Tasarım dışı`, `E05: Duplikasyon`, `E06: Tam metin yok`).
- **Karar sözlüğü** (kısa açıklama + örnek) oluşturulur; tarama eğitiminde kullanılır.
- PRISMA akışında **tam metin dışlama gerekçeleri** kodlarla raporlanır.

---

## 6) Veri çıkarımı ve veri yönetimi

### 6.1 Veri çıkarım formu — çekirdek alanlar
**Çalışma karakteristikleri:** yazar/yıl, tasarım, ülke, süre, örneklem (ITT/PP), sponsor.

**Popülasyon:** yaş, cinsiyet, akne şiddeti (IGA vb.), Fitzpatrick dağılımı, etnisite, dışlama kriterleri.

**Müdahale:** formülasyon (FDC vs eşzamanlı), uygulama rejimi, süre, eşlik eden bakım.

**Güvenlilik çıktıları:**
- Toplam AE insidansı
- Eritem, kuruluk/deskuamasyon, yanma/batma, kaşıntı, soyulma (skor veya olay)
- Toplam irritasyon skoru (TSS)
- AE nedeniyle tedavi kesilmesi
- SAE, kontakt dermatit, PIH vb.

### 6.2 Çift veri çıkarımı ve kalite kontrol
- Veri çıkarımı iki araştırmacı tarafından bağımsız yapılır.
- Uyuşmazlıklar konsensüsle, gerekirse üçüncü kişiyle çözülür.
- Pilot çıkarım turu ile form ve veri sözlüğü rafine edilir.
- Her veri noktası için iz sürülebilirlik: sayfa/tablo/ek referansı.

### 6.3 Eksik veri yönetimi
**Yazarla iletişim:** en az 2 girişim, 2 hafta aralıklı.

**İmpütasyon:**
- SD eksikse pooled SD / p-değerinden hesaplama.
- Medyan verilmişse ortalama tahmini (uygun yöntemle).
- Grafik verisi: WebPlotDigitizer.

**Duyarlılık senaryoları:** eksik sonuç verisi için konservatif ve alternatif varsayımlar (önceden planlı).

### 6.4 Veri dönüşümleri (minimum standart)
- `SD = SE * sqrt(n)`
- 95% CI → SD: uygun t-dağılımı ile geri hesaplama
- Ölçek yönü standardizasyonu: yüksek skor = daha kötü tolerabilite olacak şekilde harmonizasyon
- Farklı ölçekler: SMD (Hedges’ g) + küçük örneklem düzeltmesi
- Değişim skoru (baseline→takip): korelasyon raporlanmıyorsa varsayım + duyarlılık

### 6.5 Veri sözlüğü, versiyonlama ve gizlilik
- **Veri sözlüğü** (değişken adı, tanım, tür, birim, kodlama) `extraction/data_dictionary.csv` olarak tutulur.
- Extraction veri seti **versiyonlanır** (ör. `extracted_data_v1.csv`, `v2.csv`); ana değişiklikler `logs/extraction_changes.md` ile loglanır.
- Kişisel veri varsa **anonimizasyon** ve erişim kısıtları uygulanır; veri paylaşımı için “de-identification” notu rapora eklenir.

### 6.6 Çıktı (outcome) tanımı: 5 bileşen standardı (Cochrane)
Seçici raporlama ve “çoklu olası analiz” riskini azaltmak için her kritik çıktı, extraction aşamasında aşağıdaki **5 bileşenle** tam tanımlanır:

1) **Domain/başlık:** (örn. eritem, AE nedeniyle tedavi kesilmesi).  
2) **Ölçüm aracı/definasyon:** ölçek adı ve aralığı (0–3/0–4), “yüksek=iyi/kötü” yönü, eşik/cut-point tanımı, klinik endpoint tanımı.  
3) **Katılımcı düzeyi metrik:** post-treatment, baseline→takip değişim, “≥1 AE yaşayan” vb.  
4) **Toplulaştırma yöntemi:** oran/proportion, risk, ortalama, HR vb.  
5) **Zaman noktası:** hedef zaman penceresi (örn. hafta 4/8/12) + pencere kuralı.

**Uygulama kuralları:**
- Çalışma birden fazla ölçek veya cut-point raporluyorsa mümkünse **ham kategori dağılımı** (0/1/2/3 gibi) da çıkarılır; cut-point seçimi duyarlılık analizine bağlanır.
- Aynı çalışmayı aynı meta-analize birden fazla zaman noktasıyla sokma: protokoldeki **ana zaman penceresi** kullanılır; alternatifler duyarlılıkta raporlanır.
- “Daha iyi/kötü” yönü standardize edilir (bkz. 6.4).

### 6.7 Advers olay verisi: çıkarım ve kodlama standartları (Cochrane odaklı)
Advers etkiler, çalışmalarda birincil çıktılara kıyasla daha heterojen ve daha eksik raporlanabildiğinden extraction’da aşağıdaki minimum set uygulanır:

- **Terminoloji:** çalışma hangi terimi kullanıyorsa (AE/ADR/side effect/complication) aynen kaydedilir; “AE” nedensellik gerektirmeyebilir.
- **Saptama/izlem yöntemi:** aktif izlem (önceden tanımlı) vs spontan rapor; kim raporladı (hasta/araştırmacı); izlem sıklığı.
- **Payda + risk penceresi:** güvenlilik analizi için kullanılan denominator (safety set/ITT/PP), takip süresi ve AE’nin kapsadığı zaman aralığı kaydedilir.
- **Veri tipi:** mümkünse **katılımcı sayısı (≥1 olay yaşayan)**; yalnızca olay sayısı varsa “event count/rate” olarak işaretlenir.
- **Ciddiyet/şiddet:** SAE, AE nedeniyle çekilme, şiddet derecesi (mild/moderate/severe) ve nedensellik değerlendirmesi (varsa).
- **Kodlama:** AE’ler mümkünse ortak bir sözlüğe (örn. MedDRA SOC/PT veya proje içi kod kitabı) map edilir; birleştirme kuralları + belirsizlik bayrakları loglanır.
- **Çoklu rapor/CSR/regülatif kaynak:** aynı çalışmanın farklı raporları arasında güvenlilik verisi çelişirse “ana kaynak” ve gerekçe belirtilir; tüm raporlar saklanır.

---

## 7) Yanlılık riski değerlendirmesi (RoB 2 / ROBINS-I)

### 7.1 RoB 2 (RKÇ’ler)
RoB 2 değerlendirmesi **sonuç (result)** düzeyinde yürütülür; özellikle SoF’e giren çıktılar için gerekçe metni zorunludur.

**Domain’ler:**
- Randomizasyon süreci
- Planlanan müdahaleden sapmalar
- Eksik sonlanım verisi
- Sonlanım ölçümü
- Seçici raporlama

**Kategori:** düşük risk / bazı endişeler / yüksek risk.

### 7.2 ROBINS-I (non-RKÇ)
Konfounding, katılımcı seçimi, müdahale sınıflandırması, sapmalar, eksik veri, ölçüm yanlılığı, seçici raporlama domain’leri ile.

### 7.3 Yayın yanlılığı / küçük çalışma etkisi
- Görsel: funnel plot (gerekirse contour-enhanced).
- Testler: Egger, Peters, Begg-Mazumdar vb. (genellikle k≥10).
- Trim-and-fill vb. düzeltmeler yalnızca duyarlılık/keşif amaçlı raporlanır.

### 7.4 Finansman/çıkar çatışması ve “missing results” sinyali
- **Finansman + COI:** sponsor, sponsor rolü ve yazar çıkar çatışmaları extraction alanı olarak tutulur; raporda şeffaf raporlanır (gerekirse keşifsel alt grup/duyarlılık: endüstri vs akademik).
- **Seçici raporlama/missing results:** trial registry/protokol/CSR ile yayın karşılaştırılır; RoB 2 “seçici raporlama” gerekçesi buna dayandırılır ve GRADE “publication bias” tartışmasına girdi sağlar.

---

## 8) İstatistiksel sentez (pairwise + single-arm)

### 8.0 Sentez çerçevesi: meta-analize başlamadan önce (Cochrane)
Meta-analiz “ilk adım” değildir. Sentez öncesi minimum çerçeve:

1) Dahil edilen çalışmalar için standardize **PICO karakteristikleri tablosu** (popülasyon, müdahale, karşılaştırıcı, çıktılar, tasarım).
2) Her karşılaştırma için çalışmaların **gruplandırılabilirliğini** (klinik/metodolojik benzerlik) açıkça kontrol et.
3) Her çıktı için **hangi çalışmaların veri sağladığını** gösteren bir “synthesis matrix” oluştur (k, n, zaman noktası, ölçüm aracı).
4) Unit-of-analysis sorunlarını erken yakala (split-face, çok kollu, cluster, cross-over) ve analiz kuralını uygula (bkz. 9).
5) Veri tutarlılık kontrolleri: paydalar, tanımlar, zaman pencereleri, duplikasyon popülasyonlar, imputation bayrakları.
6) Planlanan karşılaştırmalar/çıktılarda sapma gerekiyorsa `logs/protocol_changes.csv` ile **gerekçeli** logla.
7) Meta-analiz uygun değilse, **yapılandırılmış narratif sentez** (çıktı bazlı, yön + büyüklük + belirsizlik) uygula.

### 8.1 Etki ölçütleri
**İkili çıktılar:** RR (primer), OR (nadir olaylar), RD, NNH.

**Sürekli çıktılar:** MD (aynı ölçek), SMD/Hedges’ g (farklı ölçekler).

### 8.2 Varsayılan modelleme yaklaşımı
**Ana yaklaşım:** random-effects.

**Küçük çalışma sayısı (k küçük) düzeltmesi:**
- Güven aralıklarında **Hartung–Knapp / HKSJ** yaklaşımı önceliklidir.

**τ² (tau-squared) tahmincisi (öneri):**
- Sürekli çıktılar: REML.
- İkili çıktılar: Paule–Mandel.
- DerSimonian–Laird: replikasyon/duyarlılık olarak raporlanabilir.

### 8.2.1 Model seçimi: fixed-effect vs random-effects (hangi soruyu cevaplıyoruz?)
- **Fixed-effect** yaklaşımı, tüm çalışmaların aynı “tek” gerçek etkiyi paylaştığını varsayar; özet etki bu ortak etkinin tahminidir ve çıkarım **dahil edilen çalışmaların temsil ettiği popülasyonla** sınırlıdır. Büyük çalışmalar ağırlığı belirgin biçimde domine edebilir.
- **Random-effects** yaklaşımı, gerçek etkinin çalışmalar arasında değiştiğini ve çalışmaların “muhtemel etkiler” dağılımından bir örnek olduğunu varsayar; özet etki bu dağılımın **ortalamasının** tahminidir ve çıkarım “benzer” çalışma/bağlam evrenine genellenebilir. Ağırlıklar daha dengelidir ve belirsizlik daha büyüktür.
- **Model seçimi, heterojenite testine (Q p-değeri) göre yapılmamalıdır.** Q testi düşük güçte olabilir; bu nedenle “önce fixed, heterojenite çıkarsa random” yaklaşımı yanlıştır. Random-effects seçilip τ²=0 bulunursa analiz zaten fixed-effect’e indirgenir.
- **k çok küçükse** τ² hassasiyeti düşer; bu durumda (i) havuzlamayı bırakıp yapılandırılmış narratif sentez, (ii) fixed-effect’i yalnızca “descriptive” olarak raporlama (genelleme yapmadan) veya (iii) dış bilgiyle τ² için Bayesyen yaklaşım gibi seçenekler düşünülür; tercih ve sınırlılıklar açıkça raporlanır.

**Prediction interval:** random-effects sonuçları için raporlanır.

### 8.3 Heterojenite raporlama standardı
- Cochran’s Q (p<0.10 yorumlayıcı)
- I² (eşiklerle birlikte, mümkünse CI)
- τ² (mutlak)
- Prediction interval (klinik yorum)
- Not: **Q ve p-değeri heterojenitenin “varlığına” işaret eder; büyüklüğünü vermez.** I² bir **oran** ölçüsüdür; klinik yorum için τ/τ² ve özellikle **prediction interval** (klinik eşikler/NNH ile birlikte) daha bilgilendiricidir.

### 8.4 Alt grup / meta-regresyon (önceden tanımlı)
**Alt gruplar (örnekler):**
- Formülasyon: sabit doz vs eşzamanlı kullanım
- Süre: ≤4 hafta vs 5–12 hafta vs >12 hafta
- Yaş: pediatrik vs adolesan vs erişkin
- Fitzpatrick: I–III vs IV–VI
- Tasarım: RKÇ vs non-RKÇ
- Sponsor: endüstri vs akademik

**Meta-regresyon:** genellikle k≥10; sonuçlar hipotez üreticidir.
- Alt grup ve meta-regresyon bulguları çoğu durumda **gözlemsel** niteliktedir; nedensellik iddiası yerine açıklayıcı/hipotez üretici olarak raporlanır. Veri odaklı (post-hoc) çoklu alt grup analizlerinden kaçınılır.

### 8.5 Duyarlılık analizleri
- Leave-one-out
- Yüksek RoB çalışmaların çıkarılması
- Fixed vs random-effects
- Farklı τ² tahmincileri
- ITT vs PP
- Outlier/influence diagnostics
- Etki ölçütü duyarlılığı (RR vs OR)
- Raporlama: her duyarlılık analizini ayrı forest plot ile “çoğaltmak” yerine **özet bir tablo + kısa yorum** tercih edilir.

### 8.6 Tek kollu (single-arm) güvenlilik meta-analizi
Karşılaştırıcı yoksa:
- Olay oranları/proportions için **logit dönüşümü** tercih edilir; ham oranların havuzlanması (raw) genellikle kaçınılmalıdır.
- R uygulaması için: `meta::metaprop(sm = "PLOGIT")` ve varsayılan GLMM yaklaşımı (opsiyonel olarak inverse-variance).
- Freeman–Tukey (double arcsine) gibi dönüşümler **yalnızca duyarlılık** olarak düşünülür; bazı senaryolarda yanıltıcı sonuç üretebileceği not edilir.
- Klinik ve metodolojik heterojenite yüksekse narratif sentez.

### 8.7 Klinik anlamlılık ve eşik değerler
- İstatistiksel anlamlılık tek başına yeterli değildir; **klinik anlamlılık** için önceden tanımlı eşikler (örn. mutlak risk farkı, NNH, TSS artışı) kullanılır.
- NNH hesapları raporlanır ve kısa/uzun dönem tolerabilite için ayrı yorumlanır.
- Klinik yorumda **prediction interval** öncelikli olarak kullanılır; heterojenite yüksekse klinik çıkarımlar sınırlandırılır.

### 8.8 R ile analiz uygulaması (R: meta/metafor/dmetar)
Bu projede istatistiksel analizler **R** ile yürütülür. Uygulama yaklaşımı, iki pratik referansla hizalanır:
- `reference/Doing Meta-Analysis with R.md` (Harrer ve ark.) — uygulama odaklı workflow + \{meta\}/\{dmetar\}
- `reference/Meta-Analysis with R.md` (Schwarzer, Carpenter, Rücker) — \{meta\} odaklı “standart yöntemler”

**Temel prensip:** Mümkünse ham veriyle (`n`, `event`, `mean`, `sd`) analiz; mümkün değilse **generic inverse-variance** (ön-hesaplı etki + SE) ve `metagen`.

#### 8.8.1 Paket seti (minimum)
- **Zorunlu:** `meta`, `metafor`, `dmetar`, `tidyverse`, `readr`, `janitor`
- **Önerilen (opsiyonel):** `clubSandwich` (bağımlı etkiler için robust SE), `here` (path), `arrow` (büyük veri)

#### 8.8.2 Veri formatı (analiz tabanı)
Analiz dosyaları, çıktı ve tasarım farklarını yönetebilmek için “uzun (long) format” mantığında hazırlanır:

- `analysis/synthesis_matrix.csv`: hangi çalışma hangi karşılaştırma + çıktı + zaman penceresi ile katkı verdi?
- `analysis/input/pairwise_binary.csv`: `study_id`, `studlab`, `outcome_id`, `time_window`, `event_e`, `n_e`, `event_c`, `n_c`, (opsiyonel: `design`, `risk_of_bias`, `subgroup_*`)
- `analysis/input/pairwise_continuous.csv`: `study_id`, `studlab`, `outcome_id`, `time_window`, `mean_e`, `sd_e`, `n_e`, `mean_c`, `sd_c`, `n_c`
- `analysis/input/generic_iv.csv`: `study_id`, `studlab`, `outcome_id`, `time_window`, `TE`, `seTE` (opsiyonel `lower`, `upper`)
- `analysis/input/single_arm.csv`: `study_id`, `studlab`, `outcome_id`, `time_window`, `event`, `n`

> Not: `meta` ikili çıktılarda RR/OR’u içerde **log ölçekte** taşır. Objeden değer çekerken (örn. `m$TE.random`) geri dönüşüm için `exp(...)` gerekir.

#### 8.8.3 Pairwise ikili çıktılar (RR/OR) — `meta::metabin`
Sparse veri olasılığı nedeniyle (özellikle güvenlilik çıktılarında) varsayılan havuzlama:
- Etki ölçütü: `sm = "RR"` (primer), `sm = "OR"` (duyarlılık/nadir olay)
- Yöntem: `method = "MH"` (Mantel–Haenszel)
- Heterojenite: `method.tau = "PM"` (primer) + `REML` duyarlılığı
- Küçük k: `hakn = TRUE` (HKSJ)

Örnek şablon:
```r
library(meta)

m_rr <- metabin(
  event.e = event_e, n.e = n_e,
  event.c = event_c, n.c = n_c,
  studlab = studlab,
  data = dat,
  sm = "RR",
  method = "MH",
  MH.exact = TRUE,
  comb.fixed = FALSE,
  comb.random = TRUE,
  method.tau = "PM",
  hakn = TRUE
)
```

#### 8.8.4 Pairwise sürekli çıktılar (MD/SMD) — `meta::metacont` veya `meta::metagen`
- Aynı ölçek: `sm = "MD"`
- Farklı ölçek: `sm = "SMD"` ve `method.smd = "Hedges"`
- Heterojenite: `method.tau = "REML"` (primer)
- Küçük k: `hakn = TRUE`

Örnek (ham mean/SD varsa):
```r
library(meta)

m_smd <- metacont(
  n.e = n_e, mean.e = mean_e, sd.e = sd_e,
  n.c = n_c, mean.c = mean_c, sd.c = sd_c,
  studlab = studlab,
  data = dat,
  sm = "SMD",
  method.smd = "Hedges",
  comb.fixed = FALSE,
  comb.random = TRUE,
  method.tau = "REML",
  hakn = TRUE
)
```

Örnek (paired/cross-over/adjusted etki gibi ön-hesaplı TE+SE varsa):
```r
library(meta)

m_giv <- metagen(
  TE = TE, seTE = seTE,
  studlab = studlab,
  data = dat,
  sm = "MD",
  comb.fixed = FALSE,
  comb.random = TRUE,
  method.tau = "REML",
  hakn = TRUE
)
```

#### 8.8.5 Tek kollu oranlar (single-arm) — `meta::metaprop`
Güvenlilik tek kollu havuzlamada varsayılan:
- `sm = "PLOGIT"` (logit dönüşüm)
- `method = "GLMM"` (varsayılan yaklaşım; inverse-variance gerekirse seçenek)

```r
library(meta)

m_prop <- metaprop(
  event = event, n = n,
  studlab = studlab,
  data = dat,
  sm = "PLOGIT",
  method = "GLMM",
  comb.fixed = FALSE,
  comb.random = TRUE
)
```

#### 8.8.6 Heterojenite keşfi, outlier/influence ve duyarlılık (R)
- Outlier tarama: `dmetar::find.outliers(m)`
- Influence analizi: `m.inf <- dmetar::InfluenceAnalysis(m, random = TRUE)` ve `plot(m.inf, "es")`, `plot(m.inf, "i2")`
- τ² duyarlılığı / etki ölçütü duyarlılığı: `update.meta(m, method.tau = "REML")`, `update.meta(m, sm = "OR")` vb.

#### 8.8.7 Yayın yanlılığı / küçük çalışma etkisi (R)
- Funnel: `funnel.meta(m)` (gerekirse contour-enhanced)
- Testler:
  - Sürekli/generic: `metabias(m, method.bias = "linreg")` (Egger)
  - İkili: `metabias(m_bin, method.bias = "peters")`
- Kural: testler için **k ≥ 10** değilse yalnızca görsel + nitel tartışma.
- Düzeltme: `trimfill.meta(m)` yalnızca **duyarlılık/keşif** ve heterojenite yüksekken dikkatle.

---

## 9) Özel tasarımlar ve teknik kurallar (split-face vb.)

### 9.1 Split-face / bilateral tasarım (kritik)
Split-face çalışmalarında bağımsızlık varsayımı bozulur. Bu nedenle:
- Mümkünse **eşleştirilmiş (paired)** etki ölçütü hesaplanır.
- Paired korelasyon raporlanmıyorsa, duyarlılık analizinde varsayımsal korelasyon senaryoları (örn. r=0.25/0.5/0.75) kullanılır.

**İkili olaylar:** paired/bağımlı analiz (örn. McNemar temelli yaklaşımlar; uygun olduğunda paired RD/OR).

**Sürekli çıktılar:** paired MD; korelasyon varsayımları ile.

### 9.2 Çok kollu çalışmalar
- Ortak kontrol kolu bölünerek (split) çift sayım engellenir **veya** çok değişkenli yaklaşım kullanılır.

### 9.3 Kümelenmiş çalışmalar
- Tasarım etkisi/ICC ile düzeltme yapılır.

### 9.4 Çapraz (cross-over) çalışmalar
- Eşleştirilmiş analiz tercih edilir; mümkün değilse paralel tasarıma indirgeme açıkça not edilir.

### 9.5 Seyrek olaylar ve sıfır hücreler
- Çift sıfır olay: çalışma dışlama veya alternatif yöntemler (arcsine farkı vb.)
- Continuity correction: seçilen yaklaşım raporlanır, duyarlılık yapılır.
- Peto OR: yalnızca olayların çok nadir olduğu, grup büyüklüklerinin kabaca dengeli olduğu ve etkinin küçük/orta olduğu senaryolarda alternatif olarak düşünülür; aksi durumda continuity correction stratejisi + duyarlılık raporlaması öne çıkar.

### 9.6 Çoklu zaman noktaları
- Önceden belirlenen ana zaman noktası kullanılır.
- Alternatif zaman noktaları duyarlılık analizinde raporlanır.

---

## 10) Network Meta-Analiz (NMA) modülü — ne zaman devreye alınır?

### 10.1 NMA için ön koşullar
- Tedavi ağı **bağlantılı** olmalı (connected network).
- Transitivity (değiş-tokuş edilebilirlik): etki değiştiriciler karşılaştırmalar arasında makul dengede.
- Tutarlılık: direct ve indirect kanıt uyumlu.

### 10.2 Ağın şeffaf kurulumu: “unique set of trials”
NMA trial dahil etme süreci manipülasyon şüphesi doğurmayacak şekilde şeffaf yürütülür:
1) Karşılaştırıcıları tanımla
2) Bu karşılaştırıcıların ikisini veya fazlasını kıyaslayan tüm RCT’leri bul
3) Çok kollu çalışmalarda ilgi dışı kolları çıkar; ağ bağlantılı ise dur
4) Ağ bağlantılı değilse bağlayıcı “link” tedavileri tanımla ve sete ekle; yinele

### 10.3 NMA çıktıları (opsiyonel)
- League table
- Sıralama (SUCRA)
- Tutarlılık kontrolleri: node-splitting, net heat plot, design-by-treatment
- Frequentist (örn. `netmeta`) ana; gerekirse Bayesian duyarlılık

### 10.4 Karar verme perspektifi: hedef popülasyon, node tanımı, “evidence space” vs “decision space”
NMA, karar verme bağlamında tipik olarak şu soruya hizmet eder: **“Bu önceden tanımlı hedef popülasyonda hangi tedavi daha iyi?”** Bu nedenle:
- **Hedef popülasyon** (hastalığın evresi, daha önceki tedaviler/başarısızlık, klinik yolak) NMA dahil etme kriterini şekillendirir; çok heterojen popülasyonları karıştırmak klinik olarak anlamsız özetlere yol açabilir.
- **Müdahaleler (node’lar)** “doz, formülasyon, uygulama sıklığı, eşlik eden tedaviler” açısından net tanımlanır; klinik olarak farklı varyantlar tek node’a zorla birleştirilmez.
- **Evidence space** (kanıt ağı) ile **decision space** (karar verilecek seçenekler) aynı olmak zorunda değildir: ağı bağlamak için ek “link” tedaviler kanıt setine dahil edilebilir; fakat sıralama/sonuç yorumları karar alanındaki tedavilere odaklanır. Bu ayrım protokolde önceden belirtilir.

### 10.5 Göreli → mutlak etki: karar vermede gerekli ikinci adım
NMA çıktıları çoğunlukla **göreli etki** (OR/RR/MD/SMD) verir. Karar vermede çoğu zaman ihtiyaç duyulan ise:
- Hedef popülasyona uygun **baseline risk** (referans tedavide olay olasılığı) varsayımı
- Bu risk üzerinden her tedavi için **mutlak etki** (risk, risk farkı, NNH) ve belirsizliği

Bu nedenle NMA modülü devreye girerse, decision-relevant çıktılar için relatif sonuçlara ek olarak mutlak etki tabloları üretilir ve baseline risk kaynağı/varsayımı şeffaf loglanır.

### 10.6 Ranking/SUCRA ve “probability best” — nasıl kullanılmalı?
- Sıralama olasılıkları ve “probability best” değerleri **yüksek belirsizlikte kararsız** olabilir; tek başına karar dayanağı yapılmamalıdır.
- Sıralama metrikleri, esas olarak **belirsizliği görünür kılmak** ve tedaviler arası farkların küçük olduğu alanlarda “ne kadar emin değiliz?” sorusuna yanıt vermek için raporlanır.
- Karar, mümkün olduğunca **beklenen etki** (ve varsa maliyet/yan etki dengesi) üzerinden, etki büyüklüğü + belirsizlik + kanıt gücü birlikte değerlendirilerek verilir.

### 10.7 Tutarlılık (inconsistency) kontrolü: ağ yapısını “okuma” ve yanıt
NMA yapılırsa:
- Önce ağ geometrisi incelenir (spur/loop yapıları; hangi karşılaştırmalar gerçekten “ağ” tarafından güçleniyor?).
- Yerel kontroller (örn. node-splitting/Bucher mantığı) ve global kontroller (örn. design-by-treatment) ile tutarlılık değerlendirilir.
- Tutarsızlık varsa tipik yanıtlar: node tanımını revize etmek, etki değiştiriciler için meta-regresyon/alt grup, klinik olarak uyumsuz çalışmaların ayrıştırılması veya ağın daraltılmasıdır. Heterojenite ve tutarsızlığın ilişkisi raporlanır.

### 10.8 NMA için GRADE/certainty yaklaşımı (decision-relevant kontrastlar)
NMA’da certainty değerlendirmesi çoğu zaman **karar alanı (decision space)** içindeki kontrastlara odaklanır:
- “Direct” ve “indirect” kanıt için GRADE domain’leri (RoB, inconsistency/heterogeneity, indirectness, imprecision, publication bias) değerlendirilir.
- “Network” tahminleri için direct/indirect kanıtın **en güçlü** bileşeni temel alınır; direct–indirect **uyumsuzluğu** (incoherence) varsa düşürme düşünülür.
- Çok sayıda kontrast üretildiğinden, certainty çıktıları karar için kritik kontrastlar/çıktılarla sınırlandırılır; sonuçların “sürücülerini” göstermek için duyarlılık analizleri (ve gerekiyorsa katkı matrisi mantığı) kullanılır.

---

## 11) GRADE ve Summary of Findings (SoF)

### 11.1 GRADE domain’leri
- Yanlılık riski
- Tutarsızlık (heterojenite)
- Dolaylılık
- Kesinlik eksikliği (imprecision)
- Yayın yanlılığı

### 11.2 SoF üretim kuralları
- SoF’e giren çıktılar için result-level RoB gerekçesi zorunlu.
- İstatistiksel belirsizlik: CI genişliği, OIS, prediction interval birlikte yorumlanır.
- GRADEpro GDT ile tablo üretimi önerilir.
- SoF’teki her çıktı için (bkz. 6.6) ölçüm aracı + metrik + zaman noktası açık yazılır; relatif etki yanında mutlak etki (varsayılan risk) ve dipnotlarla gerekçeler verilir.

---

## 12) Raporlama (PRISMA 2020) ve ek materyaller

### 12.1 PRISMA 2020 kontrol listesi
27 maddelik kontrol listesinin tam uyumu hedeflenir.

### 12.2 Ek materyaller (önerilen minimum)
- Ek 1: Tüm veri tabanları için tam arama stratejileri
- Ek 2: Dışlanan tam metinler listesi (gerekçeli)
- Ek 3: RoB tabloları
- Ek 4: Forest plot’lar
- Ek 5: Funnel plot’lar (uygunsa)
- Ek 6: GRADE kanıt profilleri/SoF
- Ek 7: Duyarlılık analizleri

---

## 13) Regülatif uyum ve kalite güvencesi (QA)

### 13.1 Regülatif çerçeve
Ruhsat başvurularında kullanılacaksa:
- ICH E9(R1), ICH E17
- EMA missing data kılavuzları
- CHMP/EWP/2330/99
- FDA safety meta-analiz guidance

### 13.2 QA yaklaşımı (minimum)
- Veri çıkarımı ↔ PDF doğrulama (rastgele örneklem kontrolü)
- Kod/çıktı replikasyonu
- Karar logları: `{who, when, evidence_pointer, decision, rationale}`

---

## 14) AI-Agent destekli uygulama haritası (pipeline)

### 14.1 Tasarım ilkeleri
1. **Tek kaynaklı gerçek:** Protokol kararları tek bir config dosyasında tutulur (YAML/JSON).
2. **Denetlenebilirlik:** Her otomatik karar kanıt + gerekçe + zaman damgası ile loglanır.
3. **Human-in-the-loop:** include/exclude, veri çıkarımı ve RoB kararlarında çift kontrol.
4. **Reproducibility:** R ortamı sürüm kilidi (`renv`) ve çıktı hash’leme.

### 14.2 Ajan modülleri (önerilen)
- **A0 Orchestrator:** config okur, görevleri sıraya koyar, çıktı/log versiyonlar.
- **A1 Search & Retrieval:** arama sorguları ve günlükleri, seed sanity check.
- **A2 Deduplication & Record Manager:** RIS/CSV import, DOI/PMID/başlık fuzzy eşleme, PRISMA sayıları.
- **A3 Screening Agent:** include/exclude/unclear + gerekçe kodları + kappa.
- **A4 Full-text Ingestion & Data Extraction:** PDF tablo/figür çıkarımı, split-face işaretleme, belirsizlik bayrağı.
- **A5 Risk-of-Bias Agent:** RoB 2/ROBINS-I şablonları, SoF çıktıları için result-level matris.
- **A6 Stats/Meta-analysis Agent:** etki ölçütleri, RE+HKSJ, τ² duyarlılıkları, prediction interval, publication bias, NMA.
- **A7 GRADE & SoF Agent:** GRADE domain girdilerini bağlar, SoF tablosu üretir.
- **A8 Reporting Agent:** PRISMA self-audit, Methods/Results taslakları, ek materyaller.
- **A9 QA/Compliance Agent:** extraction↔PDF doğrulama, replikasyon, regulatif kontrol listeleri.

---

## 15) Zaman çizelgesi, ekip ve sorumluluklar

### 15.1 Zaman çizelgesi (örnek)

| Aşama | Süre | Çıktı |
|-------|------|------|
| Protokol + PROSPERO | 2 hafta | Kayıtlı protokol |
| Sistematik arama | 2 hafta | Arama sonuçları |
| Başlık/özet taraması | 2 hafta | Tam metin listesi |
| Tam metin değerlendirmesi | 2 hafta | Dahil edilen çalışmalar |
| Veri çıkarımı | 3 hafta | Veri tabanı |
| RoB | 2 hafta | RoB tabloları |
| İstatistiksel analiz | 3 hafta | Sonuçlar/plotlar |
| GRADE/SoF | 1 hafta | Kanıt profili |
| Manuskript | 4 hafta | Taslak |
| Revizyon | 2 hafta | Yayına hazır |

### 15.2 Roller
- Birinci araştırmacı: protokol, arama, analiz, yazım
- İkinci araştırmacı: bağımsız tarama/çıkarım/RoB
- Üçüncü araştırmacı (hakem): uyuşmazlık çözümü, QA
- Biyoistatistikçi: analiz planı + doğrulama
- Bilgi uzmanı: arama stratejisi optimizasyonu
- Kıdemli danışman: metodoloji + son onay

---

## 16) Riskler, varsayımlar ve mitigasyon

1. **k küçük / sınırlı çalışma sayısı:** HKSJ + geniş CI; narratif eşik ve kanıt sınırı net raporlama.
2. **Dolaylılık:** sağlıklı gönüllü tolerabilitesi ana analizden ayrıştırılır.
3. **Ağ bağlantısızlığı:** NMA yalnızca bağlantılı ve klinik olarak makul ağlarda.
4. **Ölçek heterojenliği:** SMD ve ölçek dönüşüm kuralları + duyarlılık.
5. **Eksik veri:** yazar iletişimi + konservatif imputasyon + belirsizlik bayrağı.

---

## 17) Özel analizler (temporal tolerabilite, doz-yanıt)

Bu bölüm opsiyoneldir; yalnızca veri yeterliliği ve klinik anlamlılık koşulları sağlandığında devreye alınır. Önceden tanımlanmış analizler “keşifsel” olarak etiketlenmeli ve çoklu test riski gözetilmelidir.

### 17.1 Temporal tolerabilite profili (retinizasyon / adaptasyon kinetiği)

**Amaç:** A/BPO kombinasyonlarında irritasyonun zaman içindeki değişimini (pik ve adaptasyon dönemi) karakterize etmek.

**Önerilen zaman noktaları:**
- Baseline
- Hafta 1 (pik irritasyon beklentisi)
- Hafta 2–4 (adaptasyon)
- Hafta 8–12 (stabilizasyon)
- Hafta 24–52 (uzun dönem; varsa)

**Yaklaşımlar (uygun olduğunda):**
- Zaman noktasına göre ayrı meta-analizler (aynı çıktı, farklı zaman)
- Tek çalışmada tekrar ölçüm varsa: uygun özetleme/bağımlılık notlarıyla raporlama
- Veri yeterliyse: meta-regresyon (zaman=kovaryat) veya çok düzeyli modeller

### 17.2 Doz-yanıt meta-analizi (BPO konsantrasyonu ↔ irritasyon)

**Amaç:** BPO konsantrasyonu ile irritasyon ilişkisini (%2,5 vs %5 vs %10) nicel olarak değerlendirmek.

**Yöntem notları:**
- Uygun eşik: yeterli çalışma sayısı ve karşılaştırma çeşitliliği.
- Non-lineer ilişkiler için fraksiyone polinomial veya spline tabanlı meta-regresyon düşünülebilir.
- Çoklu karşılaştırmalar için FDR/Bonferroni gibi düzeltmelerin keşifsel bağlamda raporlanması önerilir.

---

## 18) Hedef dergiler

Bu liste yalnızca planlama amaçlıdır; hedef dergi seçimi çalışmanın kapsamı, veri gücü ve rapor formatına göre güncellenmelidir.

| Dergi | Yaklaşık etki (IF) | Not |
|-------|---------------------|-----|
| *Journal of the American Academy of Dermatology* | ~15 | Dermatoloji primer |
| *JAMA Dermatology* | ~15 | Yüksek etkili klinik |
| *British Journal of Dermatology* | ~11 | Avrupa odaklı |
| *Journal of the European Academy of Dermatology and Venereology* | ~9 | Avrupa perspektifi |
| *International Journal of Dermatology* | ~3 | Global erişim |
| *Journal of Dermatological Treatment* | ~3 | Tedavi odaklı |

---

## 19) Potansiyel zorluklar ve çözümler

| Zorluk | Olası çözüm/mitigasyon |
|--------|-------------------------|
| **Sınırlı sayıda %5 BPO çalışması** | Eşzamanlı kullanım çalışmalarını protokolde tanımlı şekilde dahil etme; kanıt sınırlılığını GRADE’de açık işleme; gerektiğinde narratif sentez |
| **Heterojen sonlanım tanımları** | Ölçek harmonizasyonu; SMD kullanımı; sonuçları SoF çekirdeğinde standardize raporlama |
| **Farklı ölçekler (0–3 vs 0–4)** | SMD veya önceden tanımlı dönüşüm; duyarlılık analizleri |
| **Eksik varyans verileri** | SD impütasyonu; yazar iletişimi; konservatif varsayımlar |
| **Yayın yanlılığı** | Gri literatür + kayıtlı klinik çalışma taraması; testlerin düşük güçte olabileceğini not et |
| **Yüksek heterojenite** | Önceden planlı alt gruplar; meta-regresyon (k yeterliyse); klinik olarak anlamlı açıklamalar yoksa narratif eşik |
| **Az sayıda çalışma (k küçük)** | HKSJ ile daha korumalı CI; prediction interval; aşırı yorumdan kaçınma |


## Ek A. TODO Backlog (uygulanabilir görev listesi)

### Milestone 0 — Repo ve yürütme iskeleti
- [ ] Protokol kararlarını `config/protocol.yml` içine taşı
- [ ] Çıktı klasör standardı: `data/raw`, `data/processed`, `screening/`, `extraction/`, `rob/`, `analysis/`, `report/`, `logs/`
- [ ] R ortam kilidi (`renv`) + paketler (`meta`, `metafor`, `dmetar`, `netmeta`)
- [ ] Audit log şeması: `{who, when, evidence_pointer, decision, rationale}`

### Milestone 1 — Arama stratejisi ve kayıt
- [ ] Veri tabanı bazlı arama sorguları üret
- [ ] Seed check (bilinen çalışmalar yakalanıyor mu?)
- [ ] Gri literatür kaynak listesi
- [ ] PROSPERO kayıt metni taslağı

### Milestone 2 — Tarama
- [ ] Tarama aracıyla senkron veri seti (Rayyan/Covidence)
- [ ] Pilot tarama + rehber rafine
- [ ] Tam tarama + dışlama kodları + uyuşmazlık çözümü
- [ ] PRISMA sayıları otomatik üret

### Milestone 3 — Veri çıkarımı
- [ ] Extraction form (split-face/tek-kollu/çok-kollu alanlarıyla)
- [ ] Çift veri çıkarımı (kritik çıktılarda %100)
- [ ] Eksik veri listesi + yazar iletişim şablonları
- [ ] Ölçek harmonizasyon kuralları

### Milestone 4 — RoB ve GRADE girdileri
- [ ] RoB 2 result-level matris (SoF çıktıları için)
- [ ] ROBINS-I (gerekirse)
- [ ] GRADE domain girdileri taslağı

### Milestone 5 — Pairwise + single-arm meta-analiz
- [ ] Etki ölçütü hesaplayıcı (RR/OR/RD; MD/SMD; paired hesaplar)
- [ ] Random-effects + HKSJ ana analiz
- [ ] τ² duyarlılıkları (REML/PM/DL)
- [ ] Prediction interval raporlaması
- [ ] Publication bias (k yeterliyse)

### Milestone 6 — NMA (opsiyonel)
- [ ] “Unique set of trials” ile ağ kurulumu
- [ ] Transitivity risk matrisi
- [ ] Consistency kontrolleri
- [ ] SUCRA + league table

### Milestone 7 — Raporlama ve paketleme
- [ ] PRISMA 2020 self-audit
- [ ] Manuskript taslağı
- [ ] Regülatif kontrol listesi + evidence package

---

## Ek B. Yazılım ve araçlar

### Literatür yönetimi
- EndNote/Zotero (referans + duplikasyon)
- Rayyan/Covidence (tarama)

### Veri çıkarımı
- REDCap / Excel
- WebPlotDigitizer

### İstatistik
- R: `meta`, `metafor`, `dmetar`, `netmeta`
- Alternatif: Stata, RevMan, CMA

### Reprodüksiyon
- Script tabanlı analiz, versiyon kontrol
- `sessionInfo()` raporu
- Sabit seed (rastgelelik içeren adımlarda)

---

## Ek C. Hızlı sorun giderme (VS Code / Cline Terminal)

Bu repo WSL/uzak ortamda çalıştırıldığında bazen terminal işlemleri hata kodu ile kapanabilir. En sık görülenler:

- **Exit code 127 (command not found):** Komut PATH içinde yok (özellikle non-interactive `bash -lc` çağrılarında `nvm`/Node yüklenmediğinde).
- **Exit code 1:** Komut bulundu ama başarısız oldu (örn. `python -m venv` sırasında `ensurepip` eksikliği; `pip install` sırasında iptal `^C`; eksik paket/izin vb.).

Önleyici kontroller:

- Ortam teşhisi: `sprintler/SPRINT-0-BACKLOG.md` Bölüm 2.1 (doctor)
- PDF→metin kurulum notları: `META-ANALIZ-ICRA-PLANI.md` Bölüm 3.2

Notlar:

- `set -euo pipefail` kullanırken `... | head` gibi boru hatlarında SIGPIPE yüzünden beklenmedik çıkışlar olabilir; gerekirse `| head` kısmını kaldırın veya ilgili satıra `|| true` ekleyin.
- `pip install marker-pdf` ilk kurulumda uzun sürebilir. Kurulumu `^C` ile iptal ederseniz `exit code 1` normaldir; yeniden çalıştırın.

---

## Kaynaklar

- PRISMA 2020
- Cochrane Handbook for Systematic Reviews of Interventions (2. Baskı, 2019) — özellikle Bölüm 4 (arama/seçim), 5 (veri toplama), 6 (etki ölçütleri + unit-of-analysis), 7–8 (yanlılık riski), 9–10 (sentez/meta-analiz), 14 (SoF+GRADE), 19 (advers etkiler)
- Systematic Reviews in Health Research: Meta-Analysis in Context (3. Baskı, 2022)
- Doing Meta-Analysis with R
- Meta-Analysis with R
- Introduction to Meta-Analysis
- Network Meta‐Analysis for Decision Making
- Seed klinik çalışmalar (scoping; dahil/çıkar kararı Sprint 3–4’te): Zheng et al., 2018; Andres et al., 2008
