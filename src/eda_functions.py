import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

def missing_data_analysis(df):
    """
    Eksik veri analizi yapar ve görselleştirir
    """
    print("=" * 60)
    print("EKSİK VERİ ANALİZİ")
    print("=" * 60)
    
    # Eksik veri sayısı ve yüzdesi
    missing_count = df.isnull().sum()
    missing_percent = (df.isnull().sum() / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Sütun': missing_count.index,
        'Eksik Sayısı': missing_count.values,
        'Eksik Yüzdesi (%)': missing_percent.values
    })
    
    missing_df = missing_df[missing_df['Eksik Sayısı'] > 0].sort_values('Eksik Sayısı', ascending=False)
    
    if len(missing_df) > 0:
        print("Eksik veriler:")
        print(missing_df.to_string(index=False))
        
        # Görselleştirme sadece eksik veri varsa
        try:
            plt.figure(figsize=(14, 6))
            
            # Eksik veri heatmap
            plt.subplot(1, 2, 1)
            sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')
            plt.title('Eksik Veri Haritası')
            
            # Eksik veri bar grafiği
            plt.subplot(1, 2, 2)
            missing_df.set_index('Sütun')['Eksik Yüzdesi (%)'].plot(kind='bar')
            plt.title('Eksik Veri Yüzdesi')
            plt.ylabel('Yüzde (%)')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            
            # Klasörü oluştur ve kaydet
            os.makedirs('results/plots', exist_ok=True)
            plt.savefig('results/plots/missing_data_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
            
        except Exception as e:
            print(f"Görselleştirme hatası: {e}")
            
    else:
        print("Hiç eksik veri yok!")
    
    return missing_df

def target_analysis(df, target_col='TedaviSuresi'):
    """
    Hedef değişkeni detaylı analiz eder 
    """
    print("=" * 60)
    print(f"HEDEF DEĞİŞKEN ANALİZİ: {target_col}")
    print("=" * 60)
    
    # Sütun varlık kontrolü
    if target_col not in df.columns:
        print(f"{target_col} sütunu bulunamadı!")
        print(f"Mevcut sütunlar: {list(df.columns)}")
        return None
    
    # Veri tipini kontrol et
    print(f"Sütun tipi: {df[target_col].dtype}")
    print(f"Sayısal mı: {pd.api.types.is_numeric_dtype(df[target_col])}")
    print(f"Toplam değer sayısı: {len(df[target_col])}")
    print(f"Boş olmayan değer sayısı: {df[target_col].count()}")
    
    # Hedef seri oluştur
    target_series = df[target_col].copy()
    
    # Eğer sayısal değilse hata ver 
    if not pd.api.types.is_numeric_dtype(target_series):
        print(f"{target_col} hala sayısal değil! Veri temizleme aşamasını kontrol edin.")
        print(f"Örnek değerler: {target_series.head().tolist()}")
        return None
    
    # NaN değerleri temizle
    clean_target = target_series.dropna()
    
    if len(clean_target) == 0:
        print("Analiz edilecek veri yok!")
        return None
    
    # Temel istatistikler
    print("\n Temel İstatistikler:")
    print("-" * 30)
    stats_summary = clean_target.describe()
    print(stats_summary)
    
    # Ek istatistikler
    print(f"\n Ek İstatistikler:")
    print(f"Mod: {clean_target.mode().iloc[0] if len(clean_target.mode()) > 0 else 'N/A'}")
    print(f"Çarpıklık (Skewness): {clean_target.skew():.3f}")
    print(f"Basıklık (Kurtosis): {clean_target.kurtosis():.3f}")
    
    # Aykırı değer tespiti
    try:
        Q1 = clean_target.quantile(0.25)
        Q3 = clean_target.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_mask = (clean_target < lower_bound) | (clean_target > upper_bound)
        outliers_count = outliers_mask.sum()
        
        print(f"\n Aykırı Değer Analizi:")
        print(f"Aykırı değer sayısı: {outliers_count} (%{outliers_count/len(clean_target)*100:.2f})")
        print(f"Alt sınır: {lower_bound:.2f}")
        print(f"Üst sınır: {upper_bound:.2f}")
        
        if outliers_count > 0:
            print(f"En büyük aykırı değer: {clean_target[clean_target > upper_bound].max() if (clean_target > upper_bound).any() else 'N/A'}")
            print(f"En küçük aykırı değer: {clean_target[clean_target < lower_bound].min() if (clean_target < lower_bound).any() else 'N/A'}")
        
    except Exception as e:
        print(f"Aykırı değer hesaplamasında hata: {e}")
    
    # Görselleştirmeler
    try:
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Histogram
        axes[0, 0].hist(clean_target, bins=min(50, len(clean_target.unique())), 
                       alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title(f'{target_col} Dağılımı')
        axes[0, 0].set_xlabel('Tedavi Süresi')
        axes[0, 0].set_ylabel('Frekans')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Box plot
        box_data = axes[0, 1].boxplot(clean_target, patch_artist=True)
        box_data['boxes'][0].set_facecolor('lightblue')
        axes[0, 1].set_title(f'{target_col} Box Plot')
        axes[0, 1].set_ylabel('Tedavi Süresi')
        axes[0, 1].grid(True, alpha=0.3)
        
        # QQ plot
        stats.probplot(clean_target, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title('Q-Q Plot (Normal Dağılım Testi)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Violin plot
        axes[1, 1].violinplot(clean_target)
        axes[1, 1].set_title(f'{target_col} Violin Plot')
        axes[1, 1].set_ylabel('Tedavi Süresi')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Kaydet
        os.makedirs('results/plots', exist_ok=True)
        plt.savefig('results/plots/target_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    except Exception as e:
        print(f"Görselleştirme hatası: {e}")
    
    return stats_summary

def categorical_analysis(df):
    """
    Kategorik değişkenleri analiz eder 
    """
    print("=" * 60)
    print("KATEGORİK DEĞİŞKEN ANALİZİ")
    print("=" * 60)
    
    # Kategorik sütunları otomatik tespit et
    categorical_cols = []
    for col in df.columns:
        if df[col].dtype == 'object' or df[col].dtype.name == 'category':
            categorical_cols.append(col)
    
    # Önemli kategorik sütunlar
    predefined_cats = ['Cinsiyet', 'KanGrubu', 'Uyruk', 'Bolum', 'TedaviAdi']
    for col in predefined_cats:
        if col in df.columns and col not in categorical_cols:
            categorical_cols.append(col)
    
    if not categorical_cols:
        print("Kategorik sütun bulunamadı!")
        return None
    
    print(f"Bulunan kategorik sütunlar: {categorical_cols}")
    
    # Her sütun için analiz
    for col in categorical_cols:
        if col in df.columns:
            print(f"\n {col} Analizi:")
            print("-" * 40)
            
            # Temel istatistikler
            total_count = len(df[col])
            non_null_count = df[col].count()
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            
            print(f"Toplam değer: {total_count}")
            print(f"Geçerli değer: {non_null_count}")
            print(f"Boş değer: {null_count}")
            print(f"Benzersiz değer: {unique_count}")
            
            # Value counts
            value_counts = df[col].value_counts()
            print(f"\n En sık görülen {min(10, len(value_counts))} değer:")
            print(value_counts.head(10))
            
            # Mode
            if not value_counts.empty:
                print(f"\n Mod (en sık): {value_counts.index[0]} ({value_counts.iloc[0]} kez, %{value_counts.iloc[0]/non_null_count*100:.1f})")
    
    # Görselleştirme
    available_cols = [col for col in categorical_cols if col in df.columns]
    if available_cols:
        try:
            # En fazla 6 sütun göster
            cols_to_plot = available_cols[:6]
            n_cols = 2
            n_rows = (len(cols_to_plot) + 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 6*n_rows))
            
            # Tek satır varsa axes'i liste yap
            if n_rows == 1:
                if len(cols_to_plot) == 1:
                    axes = [axes]
                else:
                    axes = [axes[0], axes[1]]
            else:
                axes = axes.flatten()
            
            for i, col in enumerate(cols_to_plot):
                if i < len(axes):
                    # En sık görülen 10 değeri göster
                    top_values = df[col].value_counts().head(10)
                    
                    # Bar plot
                    top_values.plot(kind='bar', ax=axes[i], color='skyblue')
                    axes[i].set_title(f'{col} Dağılımı (İlk 10)')
                    axes[i].set_xlabel(col)
                    axes[i].set_ylabel('Frekans')
                    axes[i].tick_params(axis='x', rotation=45)
                    axes[i].grid(True, alpha=0.3)
            
            # Kullanılmayan subplot'ları gizle
            for j in range(len(cols_to_plot), len(axes)):
                axes[j].set_visible(False)
            
            plt.tight_layout()
            plt.savefig('results/plots/categorical_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
            
        except Exception as e:
            print(f"Görselleştirme hatası: {e}")

def numerical_analysis(df):
    """
    Sayısal değişkenleri analiz eder
    """
    print("=" * 60)
    print("SAYISAL DEĞİŞKEN ANALİZİ")
    print("=" * 60)
    
    # Sayısal sütunları otomatik tespit et
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    numerical_cols.remove('HastaNo')
    
    if not numerical_cols:
        print("Sayısal sütun bulunamadı!")
        return None
    
    print(f"Bulunan sayısal sütunlar: {numerical_cols}")
    
    # Temel istatistikler
    print("\n Temel İstatistikler:")
    print("-" * 40)
    stats_df = df[numerical_cols].describe()
    print(stats_df)
    
    # Korelasyon analizi 
    correlation_matrix = None
    if len(numerical_cols) >= 2:
        print(f"\n Korelasyon Matrisi:")
        print("-" * 40)
        correlation_matrix = df[numerical_cols].corr()
        print(correlation_matrix)
        
        # Yüksek korelasyonları tespit et
        print(f"\n Yüksek Korelasyonlar (|r| > 0.5):")
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_val = correlation_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    print(f"{correlation_matrix.columns[i]} - {correlation_matrix.columns[j]}: {corr_val:.3f}")
    
    # Görselleştirmeler
    try:
        # Subplot sayısını belirle
        n_plots = min(4, len(numerical_cols) + 1)  
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()
        
        plot_idx = 0
        
        # Korelasyon heatmap
        if correlation_matrix is not None and plot_idx < len(axes):
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                       center=0, ax=axes[plot_idx], fmt='.2f')
            axes[plot_idx].set_title('Korelasyon Haritası')
            plot_idx += 1
        
        # Sayısal sütunların histogramları
        for col in numerical_cols[:3]:  
            if plot_idx < len(axes):
                axes[plot_idx].hist(df[col].dropna(), bins=30, alpha=0.7, 
                                   color='lightgreen', edgecolor='black')
                axes[plot_idx].set_title(f'{col} Dağılımı')
                axes[plot_idx].set_xlabel(col)
                axes[plot_idx].set_ylabel('Frekans')
                axes[plot_idx].grid(True, alpha=0.3)
                plot_idx += 1
        
        # Kullanılmayan subplot'ları gizle
        for i in range(plot_idx, len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        plt.savefig('results/plots/numerical_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    except Exception as e:
        print(f"Görselleştirme hatası: {e}")
    
    return correlation_matrix

def text_analysis(df):
    """
    Metin ve liste türündeki değişkenleri analiz eder
    """
    print("=" * 60)
    print("METİN/LİSTE DEĞİŞKENLERİ ANALİZİ")
    print("=" * 60)
    
    # Text sütunlarını tespit et
    text_cols = []
    potential_text_cols = ['KronikHastalik', 'Alerji', 'Tanilar', 'UygulamaYerleri']
    
    for col in potential_text_cols:
        if col in df.columns:
            text_cols.append(col)
    
    if not text_cols:
        print("Metin sütunu bulunamadı!")
        return {}
    
    print(f"Bulunan metin sütunları: {text_cols}")
    
    results = {}
    
    for col in text_cols:
        print(f"\n {col} Analizi:")
        print("-" * 40)
        
        # Temel istatistikler
        total_count = len(df[col])
        non_null_values = df[col].dropna()
        non_null_count = len(non_null_values)
        null_count = total_count - non_null_count
        
        print(f"Toplam değer: {total_count}")
        print(f"Geçerli değer: {non_null_count}")
        print(f"Boş değer: {null_count}")
        
        if len(non_null_values) > 0:
            # Virgülle ayrılmış değerleri parçala
            all_items = []
            for value in non_null_values:
                if isinstance(value, str):
                    if ',' in value:
                        items = [item.strip() for item in value.split(',') if item.strip()]
                        all_items.extend(items)
                    elif value.strip():  
                        all_items.append(value.strip())
            
            if all_items:
                # İstatistikler
                item_counts = pd.Series(all_items).value_counts()
                unique_items = len(item_counts)
                avg_length = pd.Series(all_items).str.len().mean()
                
                print(f"Toplam benzersiz değer: {unique_items}")
                print(f"Toplam parça sayısı: {len(all_items)}")
                print(f"Ortalama değer uzunluğu: {avg_length:.1f} karakter")
                print(f"Satır başına ortalama değer: {len(all_items)/non_null_count:.1f}")
                
                print(f"\nEn sık görülen {min(10, len(item_counts))} değer:")
                print(item_counts.head(10))
                
                results[col] = {
                    'item_counts': item_counts,
                    'unique_count': unique_items,
                    'total_items': len(all_items),
                    'avg_length': avg_length
                }
            else:
                print("Analiz edilecek geçerli veri bulunamadı")
                results[col] = None
        else:
            print("Bu sütunda hiç veri yok")
            results[col] = None
    
    return results

def complete_eda(df):
    """
    Kapsamlı EDA süreci 
    """
    # Results klasörünü oluştur
    os.makedirs('results/plots', exist_ok=True)
    
    print("KAPSAMLI KEŞİFSEL VERİ ANALİZİ BAŞLIYOR...")
    print("="*80)
    
    # Veri seti hakkında temel bilgi
    print(f"Veri Seti Boyutu: {df.shape}")
    print(f"Sütunlar: {list(df.columns)}")
    print(f"Bellek Kullanımı: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # 1. Eksik veri analizi
    try:
        missing_df = missing_data_analysis(df)
    except Exception as e:
        print(f"Eksik veri analizi hatası: {e}")
        missing_df = None
    
    # 2. Hedef değişken analizi
    try:
        target_stats = target_analysis(df)
    except Exception as e:
        print(f"Hedef değişken analizi hatası: {e}")
        target_stats = None
    
    # 3. Kategorik değişken analizi
    try:
        categorical_analysis(df)
    except Exception as e:
        print(f"Kategorik değişken analizi hatası: {e}")
    
    # 4. Sayısal değişken analizi
    try:
        correlation_matrix = numerical_analysis(df)
    except Exception as e:
        print(f"Sayısal değişken analizi hatası: {e}")
        correlation_matrix = None
    
    # 5. Metin değişken analizi
    try:
        text_results = text_analysis(df)
    except Exception as e:
        print(f"Metin değişken analizi hatası: {e}")
        text_results = {}
    
    # Sonuçları özetle
    print("\n" + "="*80)
    print("EDA TAMAMLANDI!")
    print("="*80)
    print("Tüm grafikler 'results/plots/' klasörüne kaydedildi.")
    print("Analiz sonuçları aşağıdaki dictionary'de:")
    
    return {
        'dataset_info': {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict()
        },
        'missing_data': missing_df,
        'target_stats': target_stats,
        'correlations': correlation_matrix,
        'text_analysis': text_results
    }
