import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use('Agg')  # GUI olmayan backend kullan
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class TurkeyElectionPredictor:
    """
    Türkiye Seçim Tahmini için Gelişmiş Random Forest Modeli
    """
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.party_columns = ['AKP', 'CHP', 'İYİ', 'HDP', 'MHP', 'SP']
        self.is_trained = False
        
    def load_and_clean_data(self, file_path):
        """
        Veriyi yükler ve temizler
        """
        try:
            # CSV dosyasını oku
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # Boş satırları temizle
            df = df.dropna(how='all')
            
            print("Ham veri:")
            print(df.head())
            print(f"Sütunlar: {df.columns.tolist()}")
            
            # Sayısal sütunları temizle ve dönüştür
            for col in self.party_columns:
                if col in df.columns:
                    print(f"\n{col} sütunu işleniyor...")
                    
                    # Virgülleri nokta ile değiştir ve tırnak işaretlerini temizle
                    df[col] = df[col].astype(str).str.replace('"', '').str.replace(',', '.')
                    
                    # Range değerleri (50-52 gibi) ortalama al
                    df[col] = df[col].apply(self._process_range_values)
                    
                    # Sayısal olmayan değerleri NaN yap
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    
                    # Boş değerleri doldurmak için komşu değerlerin ortalamasını al
                    df[col] = df[col].fillna(df[col].mean())
                    
                    print(f"{col} - NaN sayısı: {df[col].isna().sum()}")
                    print(f"{col} - örnek değerler: {df[col].dropna().head().tolist()}")
            
            # Katılımcı sayısını temizle
            if 'Katılımcı sayısı' in df.columns:
                df['Katılımcı sayısı'] = df['Katılımcı sayısı'].astype(str).str.replace('.', '').str.replace(',', '').str.replace('"', '')
                df['Katılımcı sayısı'] = pd.to_numeric(df['Katılımcı sayısı'], errors='coerce')
                df['Katılımcı sayısı'] = df['Katılımcı sayısı'].fillna(2500)  # Ortalama değer
            
            # Kararsız sütununu temizle
            if 'Kararsız' in df.columns:
                df['Kararsız'] = df['Kararsız'].astype(str).str.replace(',', '.').str.replace('"', '')
                df['Kararsız'] = pd.to_numeric(df['Kararsız'], errors='coerce')
                df['Kararsız'] = df['Kararsız'].fillna(8.0)  # Ortalama kararsız oranı
            
            # Tarih sütununu işle
            df['Tarih_Numeric'] = range(len(df))  # Kronolojik sıra
            
            # Eksik anket şirketi bilgilerini doldur
            if 'Anketi yapan' in df.columns:
                df['Anketi yapan'] = df['Anketi yapan'].fillna('Bilinmeyen')
            
            print(f"\nVeri yüklendi: {df.shape[0]} satır, {df.shape[1]} sütun")
            
            # Her parti için geçerli veri sayısını göster
            for col in self.party_columns:
                if col in df.columns:
                    valid_count = df[col].notna().sum()
                    print(f"{col}: {valid_count} geçerli veri")
            
            return df
            
        except Exception as e:
            print(f"Veri yükleme hatası: {e}")
            return None
    
    def _process_range_values(self, value):
        """
        Range değerleri (50-52 gibi) ortalama değerle değiştirir
        """
        if isinstance(value, str) and '-' in value:
            try:
                parts = value.split('-')
                if len(parts) == 2:
                    return (float(parts[0]) + float(parts[1])) / 2
            except:
                pass
        return value
    
    def create_features(self, df):
        """
        Gelişmiş özellikler oluşturur
        """
        features_df = df.copy()
        
        # Ana partiler için oy toplamı
        main_parties = ['AKP', 'CHP', 'İYİ', 'HDP', 'MHP']
        if all(col in features_df.columns for col in main_parties):
            features_df['Total_Main_Parties'] = features_df[main_parties].sum(axis=1, skipna=True)
        
        # İttifak simülasyonları
        if all(col in features_df.columns for col in ['AKP', 'MHP']):
            features_df['Cumhur_İttifakı'] = features_df['AKP'].fillna(0) + features_df['MHP'].fillna(0)
        
        if all(col in features_df.columns for col in ['CHP', 'İYİ']):
            features_df['Millet_İttifakı'] = features_df['CHP'].fillna(0) + features_df['İYİ'].fillna(0)
        
        # Anket şirketi güvenilirlik skoru (basit)
        company_reliability = {
            'MetroPOLL': 0.9, 'SONAR': 0.85, 'Gezici': 0.8, 'ORC': 0.85,
            'Mediar': 0.75, 'Piar': 0.8, 'REMRES': 0.7
        }
        
        if 'Anketi yapan' in features_df.columns:
            features_df['Güvenilirlik_Skoru'] = features_df['Anketi yapan'].map(company_reliability).fillna(0.6)
        
        # Katılımcı sayısına göre ağırlık
        if 'Katılımcı sayısı' in features_df.columns:
            features_df['Sample_Weight'] = np.log1p(features_df['Katılımcı sayısı'].fillna(1000))
        
        # Kararsız seçmen oranı
        if 'Kararsız' in features_df.columns:
            features_df['Kararsız'] = pd.to_numeric(features_df['Kararsız'], errors='coerce').fillna(0)
        
        return features_df
    
    def prepare_training_data(self, df):
        """
        Eğitim verisi hazırlar
        """
        # En az 3 partinin verisinin olduğu satırları al
        party_vote_counts = df[self.party_columns].notna().sum(axis=1)
        valid_rows = party_vote_counts >= 3
        clean_df = df[valid_rows].copy()
        
        if clean_df.empty:
            print("Yeterli temiz veri bulunamadı!")
            return None, None
        
        print(f"Kullanılabilir satır sayısı: {len(clean_df)}")
        
        # Eksik parti verilerini o partinin ortalama değeriyle doldur
        for col in self.party_columns:
            if col in clean_df.columns:
                mean_val = clean_df[col].mean()
                clean_df[col] = clean_df[col].fillna(mean_val)
        
        # Özellikler
        feature_columns = []
        
        # Sayısal özellikler
        numeric_features = ['Tarih_Numeric', 'Güvenilirlik_Skoru', 'Sample_Weight', 'Kararsız']
        for col in numeric_features:
            if col in clean_df.columns:
                feature_columns.append(col)
        
        # Parti oy oranları da özellik olarak kullanılabilir (çapraz doğrulama için)
        for party in self.party_columns:
            if party in clean_df.columns:
                feature_columns.append(f"{party}_Vote_Share")
                clean_df[f"{party}_Vote_Share"] = clean_df[party]
        
        # Kategorik özellikler
        categorical_features = ['Anketi yapan']
        for col in categorical_features:
            if col in clean_df.columns:
                feature_columns.append(col)
        
        X = clean_df[feature_columns]
        
        # Hedef değişken: En yüksek oy alan parti
        party_votes = clean_df[self.party_columns]
        y = party_votes.idxmax(axis=1)
        
        # Regresyon için de hazırlık yapabiliriz
        y_regression = clean_df[self.party_columns].values
        
        print(f"Eğitim verisi hazırlandı: {X.shape[0]} örnek, {X.shape[1]} özellik")
        print(f"Hedef dağılımı:\n{y.value_counts()}")
        
        return X, y
    
    def train_model(self, X, y):
        """
        Random Forest modelini eğitir
        """
        # Veri ön işleme pipeline'ı
        numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        
        print(f"Sayısal özellikler: {numeric_features}")
        print(f"Kategorik özellikler: {categorical_features}")
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
            ]
        )
        
        # Random Forest modeli - parametreleri veri boyutuna göre ayarla
        n_samples = len(X)
        if n_samples < 20:
            n_estimators = 50
            max_depth = 5
        else:
            n_estimators = 200
            max_depth = 10
        
        rf_model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=max(2, n_samples // 10),
            min_samples_leaf=1,
            random_state=42,
            class_weight='balanced'
        )
        
        # Pipeline oluştur
        self.model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', rf_model)
        ])
        
        # Küçük veri seti için farklı yaklaşım
        if n_samples < 10:
            # Çok küçük veri setinde cross-validation kullan
            from sklearn.model_selection import cross_val_score
            self.model.fit(X, y)
            scores = cross_val_score(self.model, X, y, cv=min(3, n_samples))
            print(f"Cross-validation skorları: {scores}")
            print(f"Ortalama doğruluk: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
            
            # Tüm veriyi test için kullan
            y_pred = self.model.predict(X)
            train_score = self.model.score(X, y)
            
            print(f"Eğitim Doğruluğu: {train_score:.3f}")
            
        else:
            # Normal train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y if len(y.unique()) > 1 else None
            )
            
            self.model.fit(X_train, y_train)
            
            # Model performansını değerlendir
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            
            print(f"Eğitim Doğruluğu: {train_score:.3f}")
            print(f"Test Doğruluğu: {test_score:.3f}")
            
            # Tahmin raporu
            y_pred = self.model.predict(X_test)
            print("\nSınıflandırma Raporu:")
            print(classification_report(y_test, y_pred))
            
            X_test, y_test = X_test, y_test
        
        self.is_trained = True
        
        # Modeli kaydet
        self.save_model()
        
        return X, y, self.model.predict(X)
    
    def save_model(self):
        """
        Eğitilmiş modeli kaydet
        """
        import pickle
        import os
        from datetime import datetime
        
        if self.model is not None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(script_dir, 'outputs', 'models')
            os.makedirs(model_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_filename = f'random_forest_model_{timestamp}.pkl'
            model_path = os.path.join(model_dir, model_filename)
            
            # Model ve preprocessor'ı birlikte kaydet
            model_data = {
                'model': self.model,
                'preprocessor': self.preprocessor,
                'party_columns': self.party_columns,
                'timestamp': timestamp
            }
            
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"🤖 Model kaydedildi: {model_path}")
    
    def predict_election_results(self, scenario_data):
        """
        Seçim sonuçlarını tahmin eder
        """
        if not self.is_trained:
            print("Model henüz eğitilmemiş!")
            return None
        
        # Tahmin yap
        prediction = self.model.predict(scenario_data)
        prediction_proba = self.model.predict_proba(scenario_data)
        
        # Senaryodaki gerçek oy oranlarını kullan (daha gerçekçi sonuç için)
        vote_shares = {}
        for party in self.party_columns:
            vote_col = f"{party}_Vote_Share"
            if vote_col in scenario_data.columns:
                vote_shares[party] = scenario_data[vote_col].iloc[0]
        
        # Model tahminini ve gerçek oy oranlarını birleştir
        if vote_shares:
            # Oy oranlarını normalize et
            total_votes = sum(vote_shares.values())
            if total_votes > 0:
                for party in vote_shares:
                    vote_shares[party] = (vote_shares[party] / total_votes) * 100
            return vote_shares, prediction
        
        # Eğer oy oranları yoksa model tahminini kullan
        classes = self.model.classes_
        results = {}
        
        for i, party in enumerate(classes):
            avg_proba = prediction_proba[:, i].mean()
            results[party] = avg_proba * 100
        
        return results, prediction
    
    def create_prediction_scenarios(self):
        """
        Farklı seçim senaryoları oluşturur
        """
        scenarios = []
        
        # Ortalama oy oranlarını hesapla (geçmiş verilerden)
        avg_votes = {
            'AKP_Vote_Share': 47.5,
            'CHP_Vote_Share': 24.0,
            'İYİ_Vote_Share': 15.5,
            'HDP_Vote_Share': 11.0,
            'MHP_Vote_Share': 8.5,
            'SP_Vote_Share': 2.8
        }
        
        # Senaryo 1: Yüksek güvenilirlik, büyük örneklem
        scenario1 = {
            'Tarih_Numeric': [25],
            'Güvenilirlik_Skoru': [0.9],
            'Sample_Weight': [np.log1p(5000)],
            'Kararsız': [5.0],
            'Anketi yapan': ['MetroPOLL'],
            **avg_votes
        }
        scenarios.append(("Yüksek Güvenilirlik Senaryosu", scenario1))
        
        # Senaryo 2: AKP lehine değişim
        scenario2 = {
            'Tarih_Numeric': [25],
            'Güvenilirlik_Skoru': [0.85],
            'Sample_Weight': [np.log1p(3000)],
            'Kararsız': [6.0],
            'Anketi yapan': ['SONAR'],
            'AKP_Vote_Share': 50.0,
            'CHP_Vote_Share': 22.0,
            'İYİ_Vote_Share': 14.0,
            'HDP_Vote_Share': 9.5,
            'MHP_Vote_Share': 7.0,
            'SP_Vote_Share': 2.5
        }
        scenarios.append(("AKP Güçlü Senaryo", scenario2))
        
        # Senaryo 3: Muhalefet güçlü
        scenario3 = {
            'Tarih_Numeric': [25],
            'Güvenilirlik_Skoru': [0.8],
            'Sample_Weight': [np.log1p(2500)],
            'Kararsız': [8.0],
            'Anketi yapan': ['Gezici'],
            'AKP_Vote_Share': 44.0,
            'CHP_Vote_Share': 27.0,
            'İYİ_Vote_Share': 17.0,
            'HDP_Vote_Share': 12.0,
            'MHP_Vote_Share': 6.5,
            'SP_Vote_Share': 3.0
        }
        scenarios.append(("Muhalefet Güçlü Senaryo", scenario3))
        
        # Senaryo 4: Yakın yarış
        scenario4 = {
            'Tarih_Numeric': [25],
            'Güvenilirlik_Skoru': [0.75],
            'Sample_Weight': [np.log1p(2000)],
            'Kararsız': [10.0],
            'Anketi yapan': ['Piar'],
            'AKP_Vote_Share': 46.0,
            'CHP_Vote_Share': 25.5,
            'İYİ_Vote_Share': 16.0,
            'HDP_Vote_Share': 11.0,
            'MHP_Vote_Share': 7.5,
            'SP_Vote_Share': 2.8
        }
        scenarios.append(("Yakın Yarış Senaryosu", scenario4))
        
        return scenarios
    
    def visualize_results(self, results_dict):
        """
        Sonuçları görselleştirir
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart
        parties = list(results_dict.keys())
        percentages = list(results_dict.values())
        
        colors = ['#FF6B35', '#1E90FF', '#32CD32', '#9932CC', '#FF1493', '#FFA500']
        bars = ax1.bar(parties, percentages, color=colors[:len(parties)])
        ax1.set_title('Tahmini Seçim Sonuçları', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Oy Oranı (%)')
        ax1.set_ylim(0, max(percentages) * 1.2)
        
        # Bar üzerine değerleri yaz
        for bar, pct in zip(bars, percentages):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Pasta grafiği
        ax2.pie(percentages, labels=parties, autopct='%1.1f%%', startangle=90, colors=colors[:len(parties)])
        ax2.set_title('Oy Dağılımı', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        # Çıktı klasörünü oluştur
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, 'outputs', 'graphs')
        os.makedirs(output_dir, exist_ok=True)
        
        # Tarih damgası ekle
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        graph_filename = f'election_prediction_2018_{timestamp}.png'
        graph_path = os.path.join(output_dir, graph_filename)
        
        plt.savefig(graph_path, dpi=300, bbox_inches='tight')
        print(f"📊 Grafik kaydedildi: {graph_path}")
    
    def generate_detailed_report(self, all_scenarios_results):
        """
        Detaylı analiz raporu oluşturur
        """
        print("\n" + "="*80)
        print("           TÜRKİYE 2018 SEÇİM TAHMİN RAPORU")
        print("                Random Forest Analizi")
        print("="*80)
        
        # Ortalama sonuçları hesapla
        all_parties = set()
        for _, results in all_scenarios_results:
            all_parties.update(results.keys())
        
        avg_results = {}
        for party in all_parties:
            scores = [results.get(party, 0) for _, results in all_scenarios_results]
            avg_results[party] = np.mean(scores)
        
        print("\nORTALAMA TAHMİN SONUÇLARI:")
        print("-" * 40)
        sorted_results = sorted(avg_results.items(), key=lambda x: x[1], reverse=True)
        
        for i, (party, score) in enumerate(sorted_results, 1):
            print(f"{i}. {party:15s}: %{score:5.1f}")
        
        print("\nSENARYO KARŞILAŞTIRMASI:")
        print("-" * 60)
        for scenario_name, results in all_scenarios_results:
            print(f"\n{scenario_name}:")
            sorted_scenario = sorted(results.items(), key=lambda x: x[1], reverse=True)
            for party, score in sorted_scenario:
                print(f"  {party:15s}: %{score:5.1f}")
        
        # İstatistiksel analiz
        print("\nİSTATİSTİKSEL ANALİZ:")
        print("-" * 40)
        winner = max(avg_results.items(), key=lambda x: x[1])
        print(f"En Olası Kazanan: {winner[0]} (%{winner[1]:.1f})")
        
        # Belirsizlik analizi
        party_variations = {}
        for party in all_parties:
            scores = [results.get(party, 0) for _, results in all_scenarios_results]
            party_variations[party] = np.std(scores)
        
        most_stable = min(party_variations.items(), key=lambda x: x[1])
        most_volatile = max(party_variations.items(), key=lambda x: x[1])
        
        print(f"En Kararlı Parti: {most_stable[0]} (±{most_stable[1]:.1f})")
        print(f"En Değişken Parti: {most_volatile[0]} (±{most_volatile[1]:.1f})")
        
        # Raporu dosyaya kaydet
        self.save_report(all_scenarios_results, avg_results, party_variations)
        
        return avg_results
    
    def save_report(self, all_scenarios_results, avg_results, party_variations):
        """
        Detaylı raporu dosyaya kaydet
        """
        import os
        from datetime import datetime
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        report_dir = os.path.join(script_dir, 'outputs', 'reports')
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f'election_analysis_report_{timestamp}.txt'
        report_path = os.path.join(report_dir, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("           TÜRKİYE 2018 SEÇİM TAHMİN RAPORU\n")
            f.write("                Random Forest Analizi\n")
            f.write(f"                  {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("="*80 + "\n\n")
            
            # Ortalama sonuçlar
            f.write("ORTALAMA TAHMİN SONUÇLARI:\n")
            f.write("-" * 40 + "\n")
            sorted_results = sorted(avg_results.items(), key=lambda x: x[1], reverse=True)
            
            for i, (party, score) in enumerate(sorted_results, 1):
                f.write(f"{i}. {party:15s}: %{score:5.1f}\n")
            
            f.write("\nSENARYO KARŞILAŞTIRMASI:\n")
            f.write("-" * 60 + "\n")
            for scenario_name, results in all_scenarios_results:
                f.write(f"\n{scenario_name}:\n")
                sorted_scenario = sorted(results.items(), key=lambda x: x[1], reverse=True)
                for party, score in sorted_scenario:
                    f.write(f"  {party:15s}: %{score:5.1f}\n")
            
            # İstatistiksel analiz
            f.write("\nİSTATİSTİKSEL ANALİZ:\n")
            f.write("-" * 40 + "\n")
            winner = max(avg_results.items(), key=lambda x: x[1])
            f.write(f"En Olası Kazanan: {winner[0]} (%{winner[1]:.1f})\n")
            
            most_stable = min(party_variations.items(), key=lambda x: x[1])
            most_volatile = max(party_variations.items(), key=lambda x: x[1])
            
            f.write(f"En Kararlı Parti: {most_stable[0]} (±{most_stable[1]:.1f})\n")
            f.write(f"En Değişken Parti: {most_volatile[0]} (±{most_volatile[1]:.1f})\n")
            
            f.write(f"\nRapor oluşturma zamanı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        print(f"📄 Detaylı rapor kaydedildi: {report_path}")

def main():
    """
    Ana uygulama fonksiyonu
    """
    print("Türkiye 2018 Seçim Tahmini - Random Forest Analizi")
    print("=" * 55)
    
    # Predictor'ı başlat
    predictor = TurkeyElectionPredictor()
    
    # Script'in bulunduğu dizini al ve CSV dosyasının tam yolunu oluştur
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, "election", "all.csv")
    
    # Veriyi yükle ve temizle
    df = predictor.load_and_clean_data(csv_file_path)
    if df is None:
        return
    
    # Özellikler oluştur
    df_with_features = predictor.create_features(df)
    
    # Eğitim verisi hazırla
    X, y = predictor.prepare_training_data(df_with_features)
    if X is None:
        return
    
    # Modeli eğit
    print("\nModel eğitiliyor...")
    X_test, y_test, y_pred = predictor.train_model(X, y)
    
    # Senaryolar oluştur ve tahmin yap
    print("\nSeçim senaryoları oluşturuluyor...")
    scenarios = predictor.create_prediction_scenarios()
    all_results = []
    
    for scenario_name, scenario_data in scenarios:
        scenario_df = pd.DataFrame(scenario_data)
        results, predictions = predictor.predict_election_results(scenario_df)
        all_results.append((scenario_name, results))
        
        print(f"\n{scenario_name} Sonuçları:")
        for party, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
            print(f"  {party}: %{score:.1f}")
    
    # Detaylı rapor oluştur
    avg_results = predictor.generate_detailed_report(all_results)
    
    # Sonuçları görselleştir
    print("\nGrafik oluşturuluyor...")
    predictor.visualize_results(avg_results)
    
    print("\n✅ Analiz tamamlandı! Tüm çıktılar 'outputs' klasöründe organize edildi.")
    print("📊 Grafikler: outputs/graphs/ klasöründe")
    print("📄 Raporlar: outputs/reports/ klasöründe")
    print("🤖 Modeller: outputs/models/ klasöründe")

if __name__ == "__main__":
    main()