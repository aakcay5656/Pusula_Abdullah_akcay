import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.model_selection import train_test_split
import os
import warnings
warnings.filterwarnings('ignore')

def advanced_missing_value_handler(df, target_col='TedaviSuresi',hasta_no='HastaNo'):
    """
    eksik değer işleme stratejileri
    """
    print("Eksik veri analizi...")
    print("="*50)
    
    df_cleaned = df.copy()
    
    # Eksik değer durumunu analiz et
    missing_info = df_cleaned.isnull().sum()
    total_rows = len(df_cleaned)
    
    print("Eksik Değer Durumu:")
    print("-" * 30)
    for col in missing_info.index:
        missing_count = missing_info[col]
        missing_percent = (missing_count / total_rows) * 100
        if missing_count > 0:
            print(f"{col}: {missing_count} (%{missing_percent:.1f})")
    
    # Sayısal değişkenler için KNN imputation
    numerical_cols = df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
    if target_col in numerical_cols:
        numerical_cols.remove(target_col)  
 
    if hasta_no in numerical_cols:
        numerical_cols.remove(hasta_no)  
    
    if len(numerical_cols) > 0:
        print(f"\n Sayısal sütunlar için KNN imputation: {numerical_cols}")
        
        # KNN Imputer (5 komşu)
        knn_imputer = KNNImputer(n_neighbors=5)
        df_cleaned[numerical_cols] = knn_imputer.fit_transform(df_cleaned[numerical_cols])
        
        print("Sayısal değişkenler KNN ile dolduruldu")
    
    # Hedef değişken için median imputation
    if target_col in df_cleaned.columns and df_cleaned[target_col].isnull().sum() > 0:
        median_val = df_cleaned[target_col].median()
        df_cleaned[target_col].fillna(median_val, inplace=True)
        print(f"{target_col} median ile dolduruldu: {median_val}")
    
    # Kategorik değişkenler için mode imputation
    categorical_cols = df_cleaned.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_cleaned[col].isnull().sum() > 0:
            mode_val = df_cleaned[col].mode()
            if len(mode_val) > 0:
                df_cleaned[col].fillna(mode_val.iloc[0], inplace=True)
            else:
                df_cleaned[col].fillna('Unknown', inplace=True)
            print(f"{col} mode ile dolduruldu")
    
    return df_cleaned

def advanced_feature_engineering(df):
    """
    özellik mühendisliği
    """
    print("\n ÖZELLİK MÜHENDİSLİĞİ...")
    print("="*50)
    
    df_engineered = df.copy()
    
    # 1. Yaş bazlı özellikler
    if 'Yas' in df_engineered.columns:
        print(" Yaş bazlı özellikler oluşturuluyor...")
        
        # Yaş grupları
        bins = [0, 18, 30, 45, 60, 75, 100]
        labels = ['Çocuk', 'Genç_Yetişkin', 'Yetişkin', 'Orta_Yaş', 'Yaşlı', 'İleri_Yaş']
        df_engineered['Yas_Grubu'] = pd.cut(df_engineered['Yas'], bins=bins, labels=labels, right=False)
        
        # Yaşlı mı? (65+ yaş)
        df_engineered['Yasli_Mi'] = (df_engineered['Yas'] >= 65).astype(int)
        
        # Çocuk mu? (18- yaş)
        df_engineered['Cocuk_Mu'] = (df_engineered['Yas'] < 18).astype(int)
        
        print(f" Yaş grupları: {df_engineered['Yas_Grubu'].value_counts().to_dict()}")
    
    # 2. Tedavi süresi bazlı özellikler
    if 'TedaviSuresi' in df_engineered.columns:
        print("\n Tedavi süresi bazlı özellikler oluşturuluyor...")
        
        # Tedavi kategorileri
        tedavi_bins = [0, 3, 7, 15, 30, float('inf')]
        tedavi_labels = ['Çok_Kısa', 'Kısa', 'Orta', 'Uzun', 'Çok_Uzun']
        df_engineered['Tedavi_Kategori'] = pd.cut(df_engineered['TedaviSuresi'], 
                                                bins=tedavi_bins, labels=tedavi_labels, right=False)
        
        # Uzun tedavi mi? (15+ seans)
        df_engineered['Uzun_Tedavi'] = (df_engineered['TedaviSuresi'] >= 15).astype(int)
        
        print(f" Tedavi kategorileri: {df_engineered['Tedavi_Kategori'].value_counts().to_dict()}")
    
    # 3. Sağlık durumu bazlı özellikler
    health_features = ['KronikHastalik', 'Alerji', 'Tanilar']
    
    for col in health_features:
        if col in df_engineered.columns:
            print(f"\n {col} için özellikler oluşturuluyor...")
            
            # Var mı yok mu?
            df_engineered[f'{col}_Var'] = df_engineered[col].apply(
                lambda x: 1 if pd.notna(x) and isinstance(x, str) and x.strip() and x.strip().lower() not in ['yok', 'none', 'nan'] else 0
            )
            
            # Sayısı (virgülle ayrılmış)
            df_engineered[f'{col}_Sayisi'] = df_engineered[col].apply(
                lambda x: len([item.strip() for item in str(x).split(',') if item.strip()]) if pd.notna(x) and str(x).lower() not in ['yok', 'none', 'nan'] else 0
            )
            
            # Uzunluğu (karakter sayısı)
            df_engineered[f'{col}_Uzunluk'] = df_engineered[col].apply(
                lambda x: len(str(x)) if pd.notna(x) else 0
            )
            
            print(f" {col} için 3 yeni özellik oluşturuldu")
    
    # 4. Kombinasyon özellikleri
    print(f"\n Kombinasyon özellikleri oluşturuluyor...")
    
    # Toplam sağlık sorunu
    health_cols = [col for col in df_engineered.columns if col.endswith('_Sayisi')]
    if health_cols:
        df_engineered['Toplam_Saglik_Sorunu'] = df_engineered[health_cols].sum(axis=1)
        print(f" Toplam sağlık sorunu özelliği oluşturuldu")
    
    # Yüksek riskli hasta
    risk_conditions = []
    if 'Yasli_Mi' in df_engineered.columns:
        risk_conditions.append('Yasli_Mi')
    if 'KronikHastalik_Var' in df_engineered.columns:
        risk_conditions.append('KronikHastalik_Var')
    
    if risk_conditions:
        df_engineered['Yuksek_Riskli'] = df_engineered[risk_conditions].sum(axis=1)
        df_engineered['Yuksek_Riskli'] = (df_engineered['Yuksek_Riskli'] >= 1).astype(int)
        print(f" Yüksek riskli hasta özelliği oluşturuldu")
    
    print(f"\n Toplam {len(df_engineered.columns) - len(df.columns)} yeni özellik oluşturuldu!")
    return df_engineered

def smart_encoding(df, target_col='TedaviSuresi'):
    """
    Akıllı kategorik değişken kodlama
    """
    print("\n AKILLI KATEGORİK KODLAMA...")
    print("="*40)
    
    df_encoded = df.copy()
    encoding_info = {}
    
    # Kategorik sütunları tespit et
    categorical_cols = df_encoded.select_dtypes(include=['object', 'category']).columns.tolist()
    
    for col in categorical_cols:
        unique_count = df_encoded[col].nunique()
        print(f"\n {col} - Benzersiz değer: {unique_count}")
        
        if unique_count <= 2:
            # Binary encoding
            print(f"Binary Label Encoding")
            le = LabelEncoder()
            df_encoded[f'{col}_encoded'] = le.fit_transform(df_encoded[col].astype(str))
            encoding_info[col] = {'type': 'label', 'encoder': le}
            
        elif unique_count <= 10:
            # One-hot encoding
            print(f"One-Hot Encoding")
            dummies = pd.get_dummies(df_encoded[col], prefix=col, drop_first=True)
            df_encoded = pd.concat([df_encoded, dummies], axis=1)
            encoding_info[col] = {'type': 'onehot', 'columns': dummies.columns.tolist()}
            
        else:
            # Target encoding için en sık görülen kategorileri al
            print(f"Frequency + Top Categories Encoding")
            
            # Frekans encoding
            freq_map = df_encoded[col].value_counts().to_dict()
            df_encoded[f'{col}_frequency'] = df_encoded[col].map(freq_map)
            
            # En sık görülen 10 kategori
            top_categories = df_encoded[col].value_counts().head(10).index.tolist()
            df_encoded[f'{col}_is_top'] = df_encoded[col].apply(
                lambda x: 1 if x in top_categories else 0
            )
            
            # Top kategoriler için one-hot
            df_encoded[f'{col}_top_category'] = df_encoded[col].apply(
                lambda x: x if x in top_categories else 'Other'
            )
            
            dummies = pd.get_dummies(df_encoded[f'{col}_top_category'], prefix=f'{col}_top', drop_first=True)
            df_encoded = pd.concat([df_encoded, dummies], axis=1)
            
            encoding_info[col] = {
                'type': 'frequency_top',
                'top_categories': top_categories,
                'frequency_map': freq_map
            }
    
    print(f"\n {len(categorical_cols)} kategorik değişken kodlandı!")
    return df_encoded, encoding_info

def feature_scaling(df, target_col='TedaviSuresi',hasta_no='HastaNo', scaling_method='standard'):
    """
    Özellik ölçeklendirme
    """
    print(f"\n ÖZELLİK ÖLÇEKLENDİRME ({scaling_method.upper()})...")
    print("="*40)
    
    df_scaled = df.copy()
    
    # Sayısal sütunları al (hedef değişken ve hasta no hariç)
    numerical_cols = df_scaled.select_dtypes(include=[np.number]).columns.tolist()
    
    # Hedef değişkeni çıkar
    if target_col in numerical_cols:
        numerical_cols.remove(target_col)
    
    # Hasta no çıkar
    if hasta_no in numerical_cols:
        numerical_cols.remove(hasta_no)
        
    # Encoded sütunları (0-1 arası) çıkar
    encoded_cols = [col for col in numerical_cols if any(x in col.lower() for x in ['_encoded', '_var', '_mu', '_mi'])]
    feature_cols = [col for col in numerical_cols if col not in encoded_cols]
    
    if len(feature_cols) > 0:
        print(f" Ölçeklendirilecek sütunlar: {feature_cols}")
        
        if scaling_method == 'standard':
            scaler = StandardScaler()
        elif scaling_method == 'minmax':
            scaler = MinMaxScaler()
        else:
            raise ValueError("scaling_method 'standard' veya 'minmax' olmalı")
        
        df_scaled[feature_cols] = scaler.fit_transform(df_scaled[feature_cols])
        
        print(f" {len(feature_cols)} özellik {scaling_method} scaler ile ölçeklendirildi!")
        
        # Ölçeklendirme istatistikleri
        print(f"\nÖlçeklendirme Sonrası İstatistikler:")
        print(f"Ortalama: {df_scaled[feature_cols].mean().mean():.3f}")
        print(f"Standart sapma: {df_scaled[feature_cols].std().mean():.3f}")
        
        return df_scaled, scaler
    else:
        print("Ölçeklendirilecek sayısal özellik bulunamadı!")
        return df_scaled, None

def outlier_detection_and_treatment(df, target_col='TedaviSuresi',hasta_no='HastaNo', method='iqr'):
    """
    Aykırı değer tespiti ve işleme
    """
    print(f"\n AYKIRI DEĞER TESPİTİ VE İŞLEME ({method.upper()})...")
    print("="*50)
    
    df_clean = df.copy()
    outlier_info = {}
    
    # Sayısal sütunları al
    numerical_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    numerical_cols.remove(hasta_no)
    
    for col in numerical_cols:
        print(f"\n {col} analiz ediliyor...")
        
        if method == 'iqr':
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df_clean[(df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)]
            
        elif method == 'zscore':
            z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
            outliers = df_clean[z_scores > 3]
            lower_bound = df_clean[col].mean() - 3 * df_clean[col].std()
            upper_bound = df_clean[col].mean() + 3 * df_clean[col].std()
        
        outlier_count = len(outliers)
        outlier_percentage = (outlier_count / len(df_clean)) * 100
        
        print(f"Aykırı değer sayısı: {outlier_count} (%{outlier_percentage:.1f})")
        
        if outlier_count > 0:
            if col == target_col and outlier_percentage > 5:
                # Hedef değişken için aykırı değerleri cap'le (sınırla)
                df_clean[col] = df_clean[col].clip(lower_bound, upper_bound)
                print(f"Hedef değişken sınırlandırıldı: [{lower_bound:.2f}, {upper_bound:.2f}]")
            elif outlier_percentage <= 5:
                # Az sayıda aykırı değeri cap'le
                df_clean[col] = df_clean[col].clip(lower_bound, upper_bound)
                print(f"Aykırı değerler sınırlandırıldı")
            else:
                print(f"Çok fazla aykırı değer, dokunulmadı")
        
        outlier_info[col] = {
            'outlier_count': outlier_count,
            'outlier_percentage': outlier_percentage,
            'bounds': (lower_bound, upper_bound)
        }
    
    return df_clean, outlier_info

def create_model_ready_dataset(df, target_col='TedaviSuresi', test_size=0.2):
    """
    Model-ready veri seti oluşturur
    """
    print(f"\n MODEL-READY VERİ SETİ OLUŞTURULUYOR...")
    print("="*50)
    
    # Hedef değişken ve özellikler
    if target_col not in df.columns:
        raise ValueError(f"Hedef değişken '{target_col}' bulunamadı!")
    
    # Sadece sayısal sütunları al (model için)
    feature_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Hedef değişkeni çıkar
    if target_col in feature_columns:
        feature_columns.remove(target_col)
    
    # Gereksiz sütunları çıkar
    exclude_patterns = ['HastaNo', 'Unnamed']
    feature_columns = [col for col in feature_columns 
                      if not any(pattern in col for pattern in exclude_patterns)]
    
    print(f"Özellik sayısı: {len(feature_columns)}")
    print(f"Hedef değişken: {target_col}")
    
    # X ve y oluştur
    X = df[feature_columns].copy()
    y = df[target_col].copy()
    
    # NaN kontrolü
    if X.isnull().sum().sum() > 0:
        print("Özelliklerde hala NaN var, temizleniyor...")
        X = X.fillna(X.median())
    
    if y.isnull().sum() > 0:
        print("Hedef değişkende NaN var, temizleniyor...")
        y = y.fillna(y.median())
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=None
    )
    
    print(f"Eğitim seti: {X_train.shape}")
    print(f"Test seti: {X_test.shape}")
    
    # İstatistikler
    print(f"\n Hedef Değişken İstatistikleri:")
    print(f"Eğitim - Ortalama: {y_train.mean():.2f}, Std: {y_train.std():.2f}")
    print(f"Test - Ortalama: {y_test.mean():.2f}, Std: {y_test.std():.2f}")
    
    return X_train, X_test, y_train, y_test, feature_columns

def full_preprocessing_pipeline(df, target_col='TedaviSuresi'):
    """
    Kapsamlı veri ön işleme pipeline'ı
    """
    print(" KAPSAMLI VERİ ÖN İŞLEME PIPELINE'I...")
    print("="*80)
    
    # Pipeline aşamaları
    pipeline_steps = []
    
    # 1. Eksik değer işleme
    print("EKSİK DEĞER İŞLEME")
    df_step1 = advanced_missing_value_handler(df, target_col)
    pipeline_steps.append(f"Eksik değerler işlendi: {df.shape} → {df_step1.shape}")
    
    # 2. Aykırı değer işleme
    print("\n AYKIRI DEĞER İŞLEME")
    df_step2, outlier_info = outlier_detection_and_treatment(df_step1, target_col)
    pipeline_steps.append(f"Aykırı değerler işlendi")
    
    # 3. Özellik mühendisliği
    print("\n ÖZELLİK MÜHENDİSLİĞİ")
    df_step3 = advanced_feature_engineering(df_step2)
    pipeline_steps.append(f"Özellik mühendisliği: {df_step2.shape} → {df_step3.shape}")
    
    # 4. Kategorik kodlama
    print("\n KATEGORİK KODLAMA")
    df_step4, encoding_info = smart_encoding(df_step3, target_col)
    pipeline_steps.append(f"Kategorik kodlama: {df_step3.shape} → {df_step4.shape}")
    
    # 5. Özellik ölçeklendirme
    print("\n ÖZELLİK ÖLÇEKLENDİRME")
    df_step5, scaler = feature_scaling(df_step4, target_col, 'standard')
    pipeline_steps.append(f"Özellik ölçeklendirme tamamlandı")
    
    # 6. Model-ready veri seti
    print("\n MODEL-READY VERİ SETİ")
    X_train, X_test, y_train, y_test, feature_columns = create_model_ready_dataset(df_step5, target_col)
    pipeline_steps.append(f"Model-ready veri seti: Train{X_train.shape}, Test{X_test.shape}")
    
    # Sonuçları kaydet
    results_folder = 'results'
    os.makedirs(results_folder, exist_ok=True)
    
    # Tüm işlenmiş veriyi kaydet
    df_step5.to_csv(f'{results_folder}/full_preprocessed_data.csv', index=False)
    
    # Model-ready veriyi kaydet
    X_train.to_csv(f'{results_folder}/X_train.csv', index=False)
    X_test.to_csv(f'{results_folder}/X_test.csv', index=False)
    pd.DataFrame({'TedaviSuresi': y_train}).to_csv(f'{results_folder}/y_train.csv', index=False)
    pd.DataFrame({'TedaviSuresi': y_test}).to_csv(f'{results_folder}/y_test.csv', index=False)
    
    # Pipeline özeti
    print("\n" + "="*80)
    print("VERİ ÖN İŞLEME PIPELINE'I TAMAMLANDI!")
    print("="*80)
    
    print("\n Pipeline Adımları:")
    for i, step in enumerate(pipeline_steps, 1):
        print(f"{i}. {step}")
    
    print(f"\n Kaydedilen dosyalar:")
    print(f"• full_preprocessed_data.csv - Tam işlenmiş veri")
    print(f"• X_train.csv, X_test.csv - Model özellikleri")
    print(f"• y_train.csv, y_test.csv - Hedef değişken")
    
    return {
        'full_data': df_step5,
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'feature_columns': feature_columns,
        'scaler': scaler,
        'encoding_info': encoding_info,
        'outlier_info': outlier_info,
        'pipeline_steps': pipeline_steps
    }
