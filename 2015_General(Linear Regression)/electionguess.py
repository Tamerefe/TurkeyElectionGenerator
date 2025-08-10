import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
import warnings
warnings.filterwarnings('ignore')

class TurkishElectionPredictor:
    """
    Türk seçim verilerini kullanarak lineer regresyon ile parti oylarını tahmin eden kapsamlı model
    """
    
    def __init__(self):
        self.models = {}
        self.pipelines = {}
        self.data = None
        self.parties = ['AK Parti', 'CHP', 'MHP', 'HDP']
        
    def load_and_prepare_data(self):
        """Veri yükleme ve ön işleme"""
        print("📊 Veri yükleniyor ve hazırlanıyor...")
        
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        election_dir = os.path.join(script_dir, 'election')
        
        # Tüm CSV dosyalarını yükle
        files = os.listdir(election_dir)
        dataframes = []
        
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(election_dir, file)
                df = pd.read_csv(file_path)
                
                # Dosya adından dönem bilgisini çıkar
                if 'haziran-2014' in file:
                    df['Dönem'] = '2014_Haziran'
                    df['Dönem_Sayı'] = 1
                elif 'haziran-2015' in file:
                    df['Dönem'] = '2015_Haziran'
                    df['Dönem_Sayı'] = 2
                elif 'kasım-2015' in file:
                    df['Dönem'] = '2015_Kasım'
                    df['Dönem_Sayı'] = 3
                
                dataframes.append(df)
        
        # Tüm veriyi birleştir
        self.data = pd.concat(dataframes, ignore_index=True)
        
        # Veri temizleme ve dönüştürme
        self._clean_data()
        self._feature_engineering()
        
        print(f"✅ Toplam {len(self.data)} anket verisi yüklendi")
        print(f"📅 Dönemler: {self.data['Dönem'].unique()}")
        print(f"🏢 Anket şirketleri: {self.data['Anketi Yapan'].nunique()} farklı şirket")
        
    def _clean_data(self):
        """Veri temizleme işlemleri"""
        print("🧹 Veri temizleniyor...")
        
        # Eksik değerleri 0 ile doldur (parti oyları için)
        party_columns = ['AK Parti', 'CHP', 'MHP', 'HDP', 'BDP', 'SP', 'BBP', 'AP']
        for col in party_columns:
            if col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce').fillna(0)
        
        # HDP ve BDP birleştir (aynı partinin farklı dönemlerdeki isimleri)
        if 'BDP' in self.data.columns:
            self.data['HDP'] = self.data['HDP'].fillna(0) + self.data['BDP'].fillna(0)
        
        # Katılımcı sayısını numeric yap
        self.data['Katılımcı sayısı'] = pd.to_numeric(self.data['Katılımcı sayısı'], errors='coerce')
        
        # Anket şirketlerini kategorize et
        self.data['Anketi Yapan'] = self.data['Anketi Yapan'].fillna('Bilinmeyen')
        
        # Genel seçim sonuçlarını işaretle
        self.data['Gerçek_Seçim'] = self.data['Anketi Yapan'].str.contains('Genel seçimler', na=False)
        
    def _feature_engineering(self):
        """Özellik mühendisliği"""
        print("⚙️ Özellik mühendisliği yapılıyor...")
        
        # Anket şirketi güvenilirlik skoru (örnek değerler)
        company_reliability = {
            'KONDA': 0.9, 'ORC': 0.85, 'Metropoll': 0.8, 'A&G': 0.8,
            'GENAR': 0.75, 'Gezici': 0.75, 'MAK': 0.7, 'SONAR': 0.7,
            'Andy-AR': 0.65, 'ANAR': 0.65, 'KamuAR': 0.6
        }
        self.data['Şirket_Güvenilirlik'] = self.data['Anketi Yapan'].map(company_reliability).fillna(0.5)
        
        # Katılımcı sayısı kategorileri
        self.data['Katılımcı_Kategori'] = pd.cut(
            self.data['Katılımcı sayısı'].fillna(1000), 
            bins=[0, 1000, 3000, 5000, float('inf')], 
            labels=['Küçük', 'Orta', 'Büyük', 'Çok_Büyük']
        )
        
        # Tarih özelliği oluştur (basitleştirilmiş)
        self.data['Tarih_Sırası'] = range(len(self.data))
        
        # Parti toplamları ve oranları
        self.data['Toplam_Oy'] = self.data[self.parties].sum(axis=1)
        
        for party in self.parties:
            self.data[f'{party}_Oran'] = self.data[party] / self.data['Toplam_Oy'] * 100
            
    def create_model_pipeline(self, target_party):
        """Belirli bir parti için model pipeline'ı oluştur"""
        
        # Özellikler
        numeric_features = ['Katılımcı sayısı', 'Şirket_Güvenilirlik', 'Dönem_Sayı', 'Tarih_Sırası']
        categorical_features = ['Anketi Yapan', 'Dönem', 'Katılımcı_Kategori']
        
        # Diğer parti oylarını özellik olarak ekle
        other_parties = [p for p in self.parties if p != target_party]
        numeric_features.extend(other_parties)
        
        # Preprocessing pipeline
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )
        
        # Model pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ])
        
        return pipeline
        
    def train_models(self):
        """Tüm partiler için modelleri eğit"""
        print("🎯 Modeller eğitiliyor...")
        
        # Sadece anket verilerini kullan (gerçek seçim sonuçlarını hedef olarak ayır)
        train_data = self.data[~self.data['Gerçek_Seçim']].copy()
        
        results = {}
        
        for party in self.parties:
            print(f"  📈 {party} için model eğitiliyor...")
            
            # Veri hazırlama
            X = train_data.drop(columns=[party] + ['Yapılış Tarihi', 'Gerçek_Seçim'] + 
                               [col for col in train_data.columns if col.endswith('_Oran')])
            y = train_data[party]
            
            # NaN değerleri temizle
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X = X[mask]
            y = y[mask]
            
            if len(X) < 10:  # Minimum veri kontrolü
                print(f"    ⚠️ {party} için yeterli veri yok")
                continue
                
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Model eğitimi
            pipeline = self.create_model_pipeline(party)
            pipeline.fit(X_train, y_train)
            
            # Tahmin ve değerlendirme
            y_pred = pipeline.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Sonuçları kaydet
            self.pipelines[party] = pipeline
            results[party] = {
                'MSE': mse,
                'RMSE': np.sqrt(mse),
                'R2': r2,
                'Test_Size': len(X_test)
            }
            
            print(f"    ✅ {party}: R² = {r2:.3f}, RMSE = {np.sqrt(mse):.2f}")
        
        # Modelleri kaydet
        self.save_models()
            
        return results
    
    def save_models(self):
        """
        Eğitilmiş modelleri kaydet
        """
        import pickle
        from datetime import datetime
        
        if self.pipelines:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(script_dir, 'outputs', 'models')
            os.makedirs(model_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_filename = f'linear_regression_models_{timestamp}.pkl'
            model_path = os.path.join(model_dir, model_filename)
            
            # Tüm modelleri ve meta bilgileri kaydet
            model_data = {
                'pipelines': self.pipelines,
                'parties': self.parties,
                'timestamp': timestamp,
                'model_type': 'Linear Regression'
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"🤖 Modeller kaydedildi: {model_path}")
        
    def predict_election_results(self, dönem='2015_Kasım'):
        """Belirli bir dönem için seçim tahminleri yap"""
        print(f"🔮 {dönem} dönemi için tahminler yapılıyor...")
        
        # Son anket verilerini al
        recent_data = self.data[
            (self.data['Dönem'] == dönem) & 
            (~self.data['Gerçek_Seçim'])
        ].copy()
        
        if len(recent_data) == 0:
            print(f"⚠️ {dönem} için anket verisi bulunamadı")
            return None
            
        predictions = {}
        
        for party in self.parties:
            if party not in self.pipelines:
                continue
                
            # Son 5 anketin ortalamasını al
            recent_party_data = recent_data.tail(5).copy()
            
            # Tahmin için veri hazırlama
            X_pred = recent_party_data.drop(columns=[party] + ['Yapılış Tarihi', 'Gerçek_Seçim'] + 
                                           [col for col in recent_party_data.columns if col.endswith('_Oran')])
            
            # NaN değerleri temizle
            mask = ~X_pred.isnull().any(axis=1)
            X_pred = X_pred[mask]
            
            if len(X_pred) > 0:
                pred = self.pipelines[party].predict(X_pred)
                predictions[party] = np.mean(pred)
                
        return predictions
        
    def evaluate_predictions(self, dönem='2015_Kasım'):
        """Tahminleri gerçek sonuçlarla karşılaştır"""
        print(f"📊 {dönem} tahminleri değerlendiriliyor...")
        
        # Tahminleri al
        predictions = self.predict_election_results(dönem)
        
        # Gerçek sonuçları al
        actual_results = self.data[
            (self.data['Dönem'] == dönem) & 
            (self.data['Gerçek_Seçim'])
        ]
        
        if len(actual_results) == 0:
            print(f"⚠️ {dönem} için gerçek seçim sonucu bulunamadı")
            return None
            
        actual = actual_results.iloc[0]
        
        comparison = pd.DataFrame({
            'Parti': self.parties,
            'Tahmin': [predictions.get(party, 0) for party in self.parties],
            'Gerçek': [actual[party] for party in self.parties]
        })
        
        comparison['Fark'] = comparison['Gerçek'] - comparison['Tahmin']
        comparison['Mutlak_Fark'] = abs(comparison['Fark'])
        
        print("\n📋 Tahmin vs Gerçek Sonuçlar:")
        print(comparison.round(2))
        
        mae = comparison['Mutlak_Fark'].mean()
        print(f"\n📈 Ortalama Mutlak Hata (MAE): {mae:.2f} puan")
        
        return comparison
        
    def plot_trends(self):
        """Parti oylarının zaman içindeki değişimini görselleştir"""
        print("📈 Grafik çiziliyor...")
        
        try:
            # Grafik ayarları
            plt.style.use('default')  # Use default style instead of seaborn
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Türk Seçim Anketleri - Parti Oyları Trend Analizi', fontsize=16, fontweight='bold')
            
            colors = ['#FF6B35', '#004E89', '#A91D3A', '#7B2D26']
            
            for i, party in enumerate(self.parties):
                ax = axes[i//2, i%2]
                
                # Dönem bazında grupla
                for j, dönem in enumerate(self.data['Dönem'].unique()):
                    dönem_data = self.data[self.data['Dönem'] == dönem]
                    if not dönem_data.empty:
                        ax.scatter(dönem_data['Tarih_Sırası'], dönem_data[party], 
                                 label=dönem, alpha=0.6, s=30)
                        
                # Trend çizgisi
                trend_data = self.data.dropna(subset=[party])
                if len(trend_data) > 1:
                    z = np.polyfit(trend_data['Tarih_Sırası'], trend_data[party], 1)
                    p = np.poly1d(z)
                    ax.plot(trend_data['Tarih_Sırası'], p(trend_data['Tarih_Sırası']), 
                           color=colors[i], linestyle='--', linewidth=2, alpha=0.8)
                
                ax.set_title(f'{party} Oy Oranları', fontweight='bold')
                ax.set_xlabel('Zaman')
                ax.set_ylabel('Oy Oranı (%)')
                ax.legend()
                ax.grid(True, alpha=0.3)
                
            plt.tight_layout()
            
            # Çıktı klasörünü oluştur
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_dir = os.path.join(script_dir, 'outputs', 'graphs')
            os.makedirs(output_dir, exist_ok=True)
            
            # Tarih damgası ekle
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            graph_filename = f'election_trends_{timestamp}.png'
            plot_path = os.path.join(output_dir, graph_filename)
            
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            print(f"📈 Grafik kaydedildi: {plot_path}")
            
        except Exception as e:
            print(f"⚠️ Grafik çizme hatası: {e}")
            print("📊 Grafik olmadan analiz devam ediyor...")
        
    def run_analysis(self):
        """Tam analizi çalıştır"""
        print("🚀 Türk Seçim Tahmini Analizi Başlıyor...\n")
        
        # 1. Veri yükleme
        self.load_and_prepare_data()
        print("\n" + "="*50)
        
        # 2. Model eğitimi
        results = self.train_models()
        print("\n" + "="*50)
        
        # 3. Model performansları
        print("📊 Model Performansları:")
        for party, metrics in results.items():
            print(f"  {party}: R² = {metrics['R2']:.3f}, RMSE = {metrics['RMSE']:.2f}")
        print("\n" + "="*50)
        
        # 4. 2015 Kasım tahminleri
        predictions_kasim = self.predict_election_results('2015_Kasım')
        if predictions_kasim:
            print("🔮 2015 Kasım Seçimi Tahminleri:")
            for party, pred in predictions_kasim.items():
                print(f"  {party}: %{pred:.1f}")
        print("\n" + "="*50)
        
        # 5. Tahmin değerlendirmesi
        comparison = self.evaluate_predictions('2015_Kasım')
        print("\n" + "="*50)
        
        # 6. Grafikler
        self.plot_trends()
        
        # 7. Rapor kaydet
        self.save_analysis_report(results, predictions_kasim, comparison)
        
        print("\n✅ Analiz tamamlandı!")
        print("📊 Grafikler: outputs/graphs/ klasöründe")
        print("📄 Raporlar: outputs/reports/ klasöründe")
        print("🤖 Modeller: outputs/models/ klasöründe")
    
    def save_analysis_report(self, results, predictions, comparison):
        """
        Analiz raporunu dosyaya kaydet
        """
        from datetime import datetime
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        report_dir = os.path.join(script_dir, 'outputs', 'reports')
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f'linear_regression_analysis_report_{timestamp}.txt'
        report_path = os.path.join(report_dir, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("         TÜRKİYE 2015 SEÇİM TAHMİN RAPORU\n")
            f.write("              Linear Regression Analizi\n")
            f.write(f"                {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("="*60 + "\n\n")
            
            # Model performansları
            f.write("MODEL PERFORMANSLARI:\n")
            f.write("-" * 30 + "\n")
            for party, metrics in results.items():
                f.write(f"{party:15s}: R² = {metrics['R2']:6.3f}, RMSE = {metrics['RMSE']:5.2f}\n")
            
            f.write("\n2015 KASIM SEÇİM TAHMİNLERİ:\n")
            f.write("-" * 30 + "\n")
            if predictions:
                for party, pred in predictions.items():
                    f.write(f"{party:15s}: %{pred:5.1f}\n")
            
            f.write("\nTAHMİN vs GERÇEK KARŞILAŞTIRMA:\n")
            f.write("-" * 40 + "\n")
            if comparison is not None:
                for _, row in comparison.iterrows():
                    f.write(f"{row['Parti']:15s}: Tahmin=%{row['Tahmin']:5.1f}, Gerçek=%{row['Gerçek']:5.1f}, Fark={row['Fark']:+5.1f}\n")
                f.write(f"\nOrtalama Mutlak Hata: {comparison['Mutlak_Fark'].mean():.2f} puan\n")
            
            f.write(f"\nRapor oluşturma zamanı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        print(f"📄 Analiz raporu kaydedildi: {report_path}")

# Ana program
if __name__ == "__main__":
    predictor = TurkishElectionPredictor()
    predictor.run_analysis()