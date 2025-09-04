

# Fiziksel Tıp ve Rehabilitasyon Veri Analizi Projesi

**Ad:** Abdullah Akçay

**Email:** aakcay5656@gmail.com

**Tarih:** Eylül 2025  

**Proje:** Pusula Data Science Vaka Çalışması  



## 🎯 Proje Hakkında

Bu proje, **2235 gözlem** ve **13 özellik** içeren fiziksel tıp ve rehabilitasyon veri seti üzerinde kapsamlı keşifsel veri analizi (EDA) ve veri ön işleme çalışmaları gerçekleştirmektedir. 

**Ana Hedef:** `TedaviSuresi` (tedavi seans sayısı) hedef değişkeni etrafında veriyi analiz etmek, temizlemek ve gelecekteki modelleme çalışmaları için hazır hale getirmek.

### 🏥 Veri Seti Özellikleri
- **HastaNo:** Anonim hasta kimlik numarası
- **Yas:** Hasta yaşı (Ortalama: 47.3 yaş)
- **Cinsiyet:** Hasta cinsiyeti (Kadın %57.0, Erkek %35.4)
- **KanGrubu:** Kan grubu bilgisi
- **Uyruk:** Hasta uyruğu
- **KronikHastalik:** Kronik hastalıklar (virgülle ayrılmış)
- **Bolum:** Tedavi görülen bölüm/klinik
- **Alerji:** Alerjiler (tekil veya virgülle ayrılmış)
- **Tanilar:** Teşhisler
- **TedaviAdi:** Uygulanan tedavi adı
- **TedaviSuresi:** 🎯 **HEDEF DEĞİŞKEN** - Tedavi süresi (Ortalama: 14.6 seans)
- **UygulamaYerleri:** Tedavi uygulama bölgeleri (En sık: Bel %23.6)
- **UygulamaSuresi:** Uygulama süresi (Ortalama: 16.6 dakika)

### 🔬 Feature Engineering Sonucu Eklenen Özellikler:
- **KronikHastalik_Count:** Kronik hastalık sayısı (Ortalama: 1.87)
- **Alerji_Count:** Alerji sayısı (Ortalama: 0.72)
- **Tanilar_Count:** Tanı sayısı (Ortalama: 2.50)
- **UygulamaYerleri_Count:** Tedavi bölgesi sayısı (Ortalama: 0.93)




## 🚀 Kurulum ve Kullanım

### Gereksinimler
```
pip install -r requirements.txt
```



### Adım Adım Çalıştırma

#### 1️⃣ Keşifsel Veri Analizi (EDA)
```
jupyter notebook notebooks/01_EDA.ipynb
```
**Ne yapar:**
- Veri setinin genel yapısını inceler (boyut, veri tipleri, bellek kullanımı)
- Eksik değer analizi ve görselleştirmesi
- Hedef değişken (TedaviSuresi) detaylı analizi
- Kategorik değişkenlerin dağılım analizi
- Sayısal değişkenlerin istatistiksel analizi
- Korelasyon analizi ve heatmap görselleştirme
- Metin/liste değişkenlerinin (KronikHastalik, Alerji) incelenmesi
- Aykırı değer tespiti ve analizi

#### 2️⃣ Veri Ön İşleme (Preprocessing)
```
jupyter notebook notebooks/02_Preprocessing.ipynb
```
**Ne yapar:**
- Gelişmiş eksik değer işleme (KNN Imputation, Simple Imputation)
- Özellik mühendisliği (yaş grupları, tedavi kategorileri, sağlık durumu özellikleri)
- Akıllı kategorik değişken kodlama (Label Encoding, One-Hot Encoding, Frequency Encoding)
- Aykırı değer tespiti ve işleme (IQR ve Z-Score yöntemleri)
- Özellik ölçeklendirme (StandardScaler, MinMaxScaler)
- Model-ready veri seti oluşturma (Train-Test Split)



## 📊 Sonuçlar ve Bulgular

### 🔍 Keşifsel Veri Analizi Bulguları

#### Veri Kalitesi:
- **Toplam Kayıt:** 2235 hasta
- **Özellik Sayısı:** 17 (13 orijinal + 4 yeni özellik)
- **Veri Tipleri:** 7 sayısal, 9 kategorik özellik

#### Hedef Değişken (TedaviSuresi) Analizi:
- **Ortalama:** 14.6 seans
- **Medyan:** 15.0 seans  
- **Standart Sapma:** 3.73 seans
- **Aralık:** 1-37 seans
- **Dağılım:** Normal dağılıma yakın
- **Aykırı Değerler:** 1 ve 37 seans arası değerler tespit edildi

#### Kategorik Değişken Bulguları:

**Cinsiyet Dağılımı:**
- **Kadın:** %57.0 (1274 hasta)
- **Erkek:** %35.4 (792 hasta)  
- **Bilinmiyor:** %7.6 (169 hasta)

**En Sık Tedavi Bölgeleri:**
- **Bel:** %23.6 (528 hasta)
- **Sol Ayak Bileği Bölgesi:** 58 hasta
- Diğer çeşitli anatomik bölgeler

---

### ⚙️ Veri Ön İşleme Sonuçları

#### Özellik Mühendisliği Detayları:
- **Başlangıç:** (2235, 17)
- **Sonuç:** (2235, 33)  
- **Eklenen özellik:** 16 yeni özellik (%94 artış)

**Yaş Bazlı Özellikler:**
- **Yetişkin (30-45 yaş):** 798 hasta (%35.7)
- **Orta Yaş (45-60 yaş):** 782 hasta (%35.0)
- **Yaşlı (60-75 yaş):** 346 hasta (%15.5)
- **Genç Yetişkin (18-30 yaş):** 145 hasta (%6.5)
- **İleri Yaş (75+ yaş):** 93 hasta (%4.2)
- **Çocuk (0-18 yaş):** 71 hasta (%3.2)

**Tedavi Süresi Kategorileri:**
- **Uzun Tedavi (15+ seans):** 1911 hasta (%85.5)
- **Orta Tedavi (7-15 seans):** 197 hasta (%8.8)
- **Kısa Tedavi (3-7 seans):** 62 hasta (%2.8)
- **Çok Kısa Tedavi (0-3 seans):** 48 hasta (%2.1)
- **Çok Uzun Tedavi (30+ seans):** 17 hasta (%0.8)

**Oluşturulan 16 Yeni Özellik:**
1. **Yas_Grubu** - Yaş kategorileri
2. **Yasli_Mi** - 65+ yaş binary flag
3. **Cocuk_Mu** - 18- yaş binary flag
4. **Tedavi_Kategori** - Tedavi süresi kategorileri
5. **Uzun_Tedavi** - 15+ seans binary flag
6. **KronikHastalik_Var** - Kronik hastalık varlığı
7. **KronikHastalik_Sayisi** - Kronik hastalık sayısı
8. **KronikHastalik_Uzunluk** - Açıklama uzunluğu
9. **Alerji_Var** - Alerji varlığı
10. **Alerji_Sayisi** - Alerji sayısı
11. **Alerji_Uzunluk** - Alerji açıklama uzunluğu
12. **Tanilar_Var** - Tanı varlığı
13. **Tanilar_Sayisi** - Tanı sayısı
14. **Tanilar_Uzunluk** - Tanı açıklama uzunluğu
15. **Toplam_Saglik_Sorunu** - Tüm sağlık sorunları toplamı
16. **Yuksek_Riskli** - Risk skoru

#### Kategorik Değişken Kodlama:
- **İşlenen değişken sayısı:** 11 kategorik değişken
- **Boyut değişimi:** (2235, 33) → (2235, 134)
- **Kodlama artışı:** %306 özellik artışı

**Kodlama Stratejileri:**
- **One-Hot Encoding (≤10 kategori):**
  - Cinsiyet (3 kategori)
  - KanGrubu (9 kategori)  
  - Uyruk (5 kategori)
  - Yas_Grubu (6 kategori)
  - Tedavi_Kategori (5 kategori)

- **Frequency + Top-Category (>10 kategori):**
  - KronikHastalik (221 kategori)
  - Tanilar (348 kategori)
  - TedaviAdi (244 kategori)
  - UygulamaYerleri (38 kategori)
  - Alerji (39 kategori)
  - Bolum (11 kategori)

#### Model-Ready Veri Seti:
- **Final özellik sayısı:** 32 (önemli özellikler seçildi)
- **Train-Test split:** %80-20 oranı
- **Eğitim seti:** (1,788, 32)
- **Test seti:** (447, 32)
- **Hedef değişken korunması:** Orijinal ölçekte (seans sayısı)

**Hedef Değişken Train-Test Dağılımı:**
- **Eğitim seti ortalama:** 14.53 seans
- **Test seti ortalama:** 14.72 seans
- **Standart sapma:** ~3.7-3.9 seans (dengeli dağılım)



## 💡 İş Değeri ve Uygulamalar

### 🏥 Hastane Yönetimi İçin:

**Hasta Segmentasyonu İçgörüleri:**
- **Yetişkin hasta ağırlığı:** %70.7 (30-60 yaş arası)
- **Yaşlı hasta oranı:** %19.7 (60+ yaş)
- **Uzun tedavi ihtiyacı:** %85.5 hasta 15+ seans gerektiriyor
- **Kısa tedavi grubu:** Sadece %4.9 hasta 7 seans altı tedavi

**Kaynak Planlama Optimizasyonu:**
- **Standart tedavi planı:** 15+ seans için kapasite ayırma
- **Yaşlı hasta kapasitesi:** %20 yaşlı hasta için özel planlama  
- **Risk grubu takibi:** Çoklu sağlık sorunu olan hastalar

### 📈 Klinik Karar Destek:

**Tahmin Modeli Hazırlığı:**
- **32 özellikli model:** Optimum özellik sayısı
- **Dengeli veri seti:** Train-test benzer dağılım
- **Kategorik zenginlik:** Kapsamlı kodlanmış değişkenler
- **Risk skorlaması:** Yüksek riskli hasta tespiti

**Tedavi Protokol Optimizasyonu:**
- Yaş grubuna özel tedavi süreleri
- Kronik hastalık sayısına göre planlama
- Çoklu tanı durumunda özel yaklaşım



## 🔧 Teknik Özellikler

### Kullanılan Teknolojiler:
- **Python 3.8+** - Ana programlama dili
- **Pandas** - Veri manipülasyonu ve analiz
- **NumPy** - Sayısal hesaplamalar  
- **Matplotlib & Seaborn** - Görselleştirme
- **Scikit-learn** - Veri ön işleme araçları
- **Scipy** - İstatistiksel hesaplamalar
- **Jupyter Notebook** - İnteraktif geliştirme ortamı

### Veri Bilimi Yöntemleri:
- **Keşifsel Veri Analizi (EDA)** - Kapsamlı veri keşfi
- **İstatistiksel Analiz** - Tanımlayıcı istatistikler
- **Görselleştirme** - Histogram, box plot, scatter plot, heatmap
- **Özellik Mühendisliği** - Yeni özellik üretimi
- **Veri Temizleme** - Eksik değer ve aykırı değer işleme
- **Kategorik Kodlama** - Multiple encoding strategies
- **Veri Dönüşümleri** - Normalizasyon ve standardizasyon

### Kod Kalitesi:
- **Modüler Yapı** - Yeniden kullanılabilir fonksiyonlar
- **Dokümantasyon** - Detaylı açıklamalar ve docstring'ler
- **Hata Yönetimi** - Try-catch blokları ve validasyon
- **Reproducibility** - Sabit random state'ler
- **Clean Code** - PEP8 standartlarına uygun kod
