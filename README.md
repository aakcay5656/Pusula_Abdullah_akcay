

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
- **Yas:** Hasta yaşı
- **Cinsiyet:** Hasta cinsiyeti  
- **KanGrubu:** Kan grubu bilgisi
- **Uyruk:** Hasta uyruğu
- **KronikHastalik:** Kronik hastalıklar (virgülle ayrılmış)
- **Bolum:** Tedavi görülen bölüm/klinik
- **Alerji:** Alerjiler (tekil veya virgülle ayrılmış)
- **Tanilar:** Teşhisler
- **TedaviAdi:** Uygulanan tedavi adı
- **TedaviSuresi:**  **HEDEF DEĞİŞKEN** - Tedavi süresi (seans sayısı)
- **UygulamaYerleri:** Tedavi uygulama bölgeleri
- **UygulamaSuresi:** Uygulama süresi





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
- **Özellik Sayısı:** 13 orijinal özellik
- **Eksik Değer Durumu:** Sistemik eksik değer analizi gerçekleştirildi
- **Veri Tipleri:** Sayısal, kategorik ve metin tipli değişkenler belirlendi

#### Hedef Değişken (TedaviSuresi) Analizi:
- **Dağılım:** Normal dağılıma yakın, sağa çarpık
- **Aralık:** Minimum 1 seans, maksimum değer veri setine göre
- **Aykırı Değerler:** IQR yöntemi ile tespit edildi
- **İstatistiksel Özellikler:** Ortalama, medyan, standart sapma hesaplandı

#### Kategorik Değişken Bulguları:
- **Cinsiyet Dağılımı:** Erkek/kadın hasta oranları analiz edildi
- **Kan Grubu:** En sık görülen kan grupları belirlendi
- **Uyruk:** Hasta uyruğu dağılımı incelendi
- **Bölüm:** En yoğun tedavi bölümleri tespit edildi


#### Metin Değişken Analizi:
- **Kronik Hastalık:** En sık görülen kronik hastalıklar
- **Alerji:** Alerji türleri ve sıklığı
- **Tanılar:** Teşhis dağılımı analizi
- **Uygulama Yerleri:** Tedavi uygulama bölgeleri

### ⚙️ Veri Ön İşleme Sonuçları

#### Eksik Değer İşleme:
- **Yöntem:** KNN Imputation (sayısal), Mode/Median (kategorik)
- **Sonuç:** Tüm eksik değerler uygun yöntemlerle dolduruldu
- **Kalite:** Veri bütünlüğü korunarak işlem tamamlandı

#### Özellik Mühendisliği:
- **Yaş Kategorileri:** Çocuk, Genç, Orta yaş, Yaşlı grupları
- **Tedavi Kategorileri:** Kısa, Orta, Uzun, Çok uzun sınıflandırması
- **Sağlık Durumu:** Kronik hastalık sayısı, alerji varlığı, risk skorları
- **Kombinasyon Özellikleri:** Çapraz özellik etkileşimleri

#### Kategorik Kodlama:
- **Binary Değişkenler:** Label Encoding uygulandı
- **Çok Kategorili:** One-Hot Encoding ve Frequency Encoding
- **Yüksek Kardinalite:** Top-category yaklaşımı ile optimize edildi

#### Özellik Ölçeklendirme:
- **Yöntem:** StandardScaler (z-score normalizasyonu)
- **Kapsam:** Tüm sayısal özellikler ölçeklendirildi
- **Hedef Korunma:** TedaviSuresi orijinal ölçekte bırakıldı

#### Model-Ready Veri:
- **Train-Test Split:** %80 eğitim, %20 test
- **Final Boyut:** X_train, X_test, y_train, y_test setleri



## 💡 İş Değeri ve Uygulamalar

### 🏥 Hastane Yönetimi İçin:
- **Kaynak Planlama:** Tedavi süresi tahminleri ile personel ve ekipman planlaması
- **Hasta Yönetimi:** Risk gruplarının önceden belirlenmesi
- **Maliyet Kontrolü:** Tedavi maliyeti tahmini için veri hazırlığı
- **Kapasite Optimizasyonu:** Bölümler arası hasta dağılım analizi

### 📈 Klinik Karar Destek:
- **Risk Değerlendirme:** Yüksek riskli hastaların profil analizi
- **Tedavi Protokolü:** Hasta özelliklerine göre tedavi süresi pattern'leri
- **Kalite İyileştirme:** Tedavi sonuçları ile hasta özellikleri ilişkisi

### 🔬 Araştırma ve Geliştirme:
- **Hipotez Testi:** Klinik varsayımların veri ile doğrulanması
- **Trend Analizi:** Hasta demografisi ve tedavi süresi trendleri
- **Benchmark:** Sektör karşılaştırmaları için temiz veri sağlama



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






