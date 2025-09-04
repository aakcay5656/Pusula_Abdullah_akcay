import pandas as pd
import numpy as np
import re
import os

def extract_numbers_from_text(series):
    """
    Metin içinden sayıları çıkarır
    """
    def extract_number(text):
        if pd.isna(text):
            return np.nan
        if isinstance(text, (int, float)):
            return text
        if isinstance(text, str):
            # Sayı arama regex'i
            numbers = re.findall(r'\d+\.?\d*', text.strip())
            if numbers:
                return float(numbers[0])
            else:
                return np.nan
        return np.nan
    
    return series.apply(extract_number)

def clean_all_numeric_columns_advanced(df):
    """
    sayısal sütun temizleme - metin içinden sayı çıkarma ile
    """
    print("SAYISAL SÜTUN TEMİZLEME BAŞLIYOR...")
    print("=" * 50)
    
    df_cleaned = df.copy()
    
    # Sayısal olması gereken sütunlar
    numeric_columns = {
        'TedaviSuresi': 'Tedavi Süresi',
        'UygulamaSuresi': 'Uygulama Süresi'
    }
    
    for col, description in numeric_columns.items():
        if col in df_cleaned.columns:
            print(f"\n {description} ({col}) temizleniyor...")
            
            # Mevcut örnekleri göster
            print(f"Örnek değerler: {df_cleaned[col].head().tolist()}")
            print(f"Mevcut tip: {df_cleaned[col].dtype}")
            
            # Sayıları çıkar
            cleaned_values = extract_numbers_from_text(df_cleaned[col])
            
            # NaN sayısı
            nan_count = cleaned_values.isna().sum()
            print(f"Çıkarılan sayısal değerler: {cleaned_values.dropna().head().tolist()}")
            
            if nan_count > 0:
                print(f"{nan_count} değer dönüştürülemedi")
                
                # Median ile doldur
                median_val = cleaned_values.median()
                if not pd.isna(median_val):
                    cleaned_values.fillna(median_val, inplace=True)
                    print(f"NaN değerler median ile dolduruldu: {median_val}")
                else:
        
                    cleaned_values.fillna(0, inplace=True)
                    print(f"Diğer değerler 0 ile dolduruldu")
            
            df_cleaned[col] = cleaned_values
            print(f"{description} başarıyla temizlendi! Yeni tip: {df_cleaned[col].dtype}")
        else:
            print(f"{col} sütunu bulunamadı")
    
    return df_cleaned

def clean_categorical_columns(df):
    """
    Kategorik sütunları temizler
    """
    print("\n KATEGORİK SÜTUNLAR TEMİZLENİYOR...")
    print("=" * 40)
    
    df_cleaned = df.copy()
    
    # Kategorik sütunlar
    categorical_columns = {
        'Cinsiyet': 'Cinsiyet',
        'KanGrubu': 'Kan Grubu', 
        'Uyruk': 'Uyruk',
        'Bolum': 'Bölüm',
        'TedaviAdi': 'Tedavi Adı'
    }
    
    for col, description in categorical_columns.items():
        if col in df_cleaned.columns:
            print(f"\n {description} ({col}):")
            
            # Boş değerleri 'Bilinmiyor' ile doldur
            null_count = df_cleaned[col].isna().sum()
            if null_count > 0:
                df_cleaned[col] = df_cleaned[col].fillna('Bilinmiyor')
                print(f"{null_count} boş değer 'Bilinmiyor' ile dolduruldu")
            
            # String tipine çevir
            df_cleaned[col] = df_cleaned[col].astype(str)
            
            # Benzersiz değer sayısını göster
            unique_count = df_cleaned[col].nunique()
            print(f"Benzersiz değer sayısı: {unique_count}")
            
            if unique_count <= 10:
                print(f"En sık değerler: {df_cleaned[col].value_counts().head().to_dict()}")
    
    return df_cleaned

def clean_text_columns(df):
    """
    Metin sütunlarını (virgülle ayrılmış listeler) temizler
    """
    print("\n METİN SÜTUNLARI TEMİZLENİYOR...")
    print("=" * 35)
    
    df_cleaned = df.copy()
    
    # Metin/liste sütunları
    text_columns = {
        'KronikHastalik': 'Kronik Hastalıklar',
        'Alerji': 'Alerjiler',
        'Tanilar': 'Tanılar',
        'UygulamaYerleri': 'Uygulama Yerleri'
    }
    
    for col, description in text_columns.items():
        if col in df_cleaned.columns:
            print(f"\n {description} ({col}):")
            
            # Boş değerleri 'Yok' ile doldur
            null_count = df_cleaned[col].isna().sum()
            if null_count > 0:
                df_cleaned[col] = df_cleaned[col].fillna('Yok')
                print(f" {null_count} boş değer 'Yok' ile dolduruldu")
            
            # String tipine çevir ve temizle
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
            
            # Virgülle ayrılmış değerlerin sayısını hesapla
            df_cleaned[f'{col}_Count'] = df_cleaned[col].apply(
                lambda x: len([item.strip() for item in x.split(',') if item.strip()]) if x and x != 'Yok' else 0
            )
            
            print(f" {description} temizlendi ve sayısal versiyonu ({col}_Count) oluşturuldu")
            print(f"Ortalama {description.lower()} sayısı: {df_cleaned[f'{col}_Count'].mean():.2f}")
    
    return df_cleaned

def full_data_cleaning_pipeline(df):
    """
    Tam veri temizleme pipeline'ı
    """
    print("TAM VERİ TEMİZLEME PIPELINE'I BAŞLIYOR...")
    print("=" * 60)
    
    # 1. Sayısal sütunları temizle
    df_step1 = clean_all_numeric_columns_advanced(df)
    
    # 2. Kategorik sütunları temizle
    df_step2 = clean_categorical_columns(df_step1)
    
    # 3. Metin sütunlarını temizle
    df_final = clean_text_columns(df_step2)
    
    print(f"\n  VERİ TEMİZLEME TAMAMLANDI!")
    print(f"Başlangıç boyutu: {df.shape}")
    print(f" Final boyutu: {df_final.shape}")
    
    # Temizlenmiş veriyi kaydet
    save_dataframe(df_final, 'cleaned_dataset.csv')
    
    return df_final

def load_data(file_path):
    """
    Excel veya CSV formatında veri setini yükler
    """
    try:
        # Dosya uzantısına göre okuma
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path, encoding='utf-8')
            
        print(f"Veri seti başarıyla yüklendi!")
        print(f" Veri seti boyutu: {df.shape}")
        
        # Sütun adlarını göster
        print(f"\n Sütun adları: {list(df.columns)}")
        
        return df
    except FileNotFoundError:
        print("Dosya bulunamadı! Lütfen dosya yolunu kontrol edin.")
        return None
    except Exception as e:
        print(f" Veri yükleme hatası: {e}")
        return None

def basic_info(df):
    """
    Veri seti hakkında temel bilgileri gösterir
    """
    print("=" * 60)
    print("VERİ SETİ TEMEL BİLGİLERİ")
    print("=" * 60)
    
    print(f" Satır sayısı: {df.shape[0]}")
    print(f" Sütun sayısı: {df.shape[1]}")
    print(f" Bellek kullanımı: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    print("\n Sütun Bilgileri:")
    print("-" * 40)
    for col in df.columns:
        non_null_count = df[col].count()
        null_count = df[col].isna().sum()
        unique_count = df[col].nunique()
        print(f"• {col}:")
        print(f"Tip: {df[col].dtype}")
        print(f"  Dolu: {non_null_count}, Boş: {null_count}, Benzersiz: {unique_count}")
        
        # İlk birkaç değeri göster
        sample_values = df[col].dropna().head(3).tolist()
        print(f"Örnekler: {sample_values}")
        print()

def save_dataframe(df, filename, folder='results'):
    """
    DataFrame'i CSV olarak kaydeder
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"Veri {filepath} olarak kaydedildi!")
