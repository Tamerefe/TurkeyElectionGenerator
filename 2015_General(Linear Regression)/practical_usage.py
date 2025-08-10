"""
🇹🇷 Türk Seçim Tahmin Modeli - Pratik Kullanım Örneği
Bu dosya, eğitilmiş modellerin nasıl kullanılacağını gösterir.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import os
import pickle
import warnings
warnings.filterwarnings('ignore')

class ElectionPredictor:
    """
    Eğitilmiş modelleri kullanarak yeni anket verilerinden tahmin yapan sınıf
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_names = None
        self.parties = ['AK Parti', 'CHP', 'MHP', 'HDP']
        
    def load_and_train(self):
        """Veriyi yükle ve modelleri eğit"""
        print("📚 Veriler yükleniyor ve modeller eğitiliyor...")
        
        # Veri yükleme
        script_dir = os.path.dirname(os.path.abspath(__file__))
        election_dir = os.path.join(script_dir, 'election')
        
        dataframes = []
        for file in os.listdir(election_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(election_dir, file)
                df = pd.read_csv(file_path)
                
                if 'haziran-2014' in file:
                    df['Period'] = 1
                elif 'haziran-2015' in file:
                    df['Period'] = 2
                elif 'kasım-2015' in file:
                    df['Period'] = 3
                    
                dataframes.append(df)
        
        data = pd.concat(dataframes, ignore_index=True)
        
        # Veri temizleme
        party_columns = ['AK Parti', 'CHP', 'MHP', 'HDP', 'BDP', 'SP', 'BBP', 'AP']
        for col in party_columns:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
        
        if 'BDP' in data.columns:
            data['HDP'] = data['HDP'] + data['BDP'].fillna(0)
        
        # Özellik mühendisliği
        data['Katılımcı sayısı'] = pd.to_numeric(data['Katılımcı sayısı'], errors='coerce').fillna(1000)
        data['Sample_Size_Log'] = np.log(data['Katılımcı sayısı'])
        data['Is_Election'] = data['Anketi Yapan'].str.contains('Genel seçimler', na=False)
        data['Total_Major_Parties'] = data[self.parties].sum(axis=1)
        data['Time_Index'] = range(len(data))
        
        # Saddle anket verilerini kullan (gerçek seçimler hariç)
        train_data = data[~data['Is_Election']].copy()
        
        # Her parti için model eğit
        for party in self.parties:
            print(f"  🎯 {party} modeli eğitiliyor...")
            
            # Özellikler
            feature_cols = [
                'Katılımcı sayısı', 'Sample_Size_Log', 'Period', 'Time_Index',
                'Total_Major_Parties'
            ] + [p for p in self.parties if p != party]
            
            X = train_data[feature_cols]
            y = train_data[party]
            
            # NaN temizleme
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X, y = X[mask], y[mask]
            
            if len(X) < 10:
                print(f"    ⚠️ {party} için yeterli veri yok")
                continue
            
            # Model ve scaler eğitimi
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            model = Ridge(alpha=0.1)  # Optimize edilmiş alpha değeri
            model.fit(X_scaled, y)
            
            # Kaydet
            self.models[party] = model
            self.scalers[party] = scaler
            self.feature_names = feature_cols
            
        print("✅ Tüm modeller eğitildi!")
        
    def predict_from_poll_data(self, poll_data):
        """
        Yeni anket verilerinden tahmin yap
        
        Parameters:
        poll_data (dict): Anket verileri
        Örnek: {
            'AK Parti': 45.0,
            'CHP': 25.0, 
            'MHP': 15.0,
            'HDP': 12.0,
            'Katılımcı sayısı': 2500,
            'Period': 3
        }
        """
        
        if not self.models:
            print("⚠️ Önce modelleri eğitmelisiniz: load_and_train() çağırın")
            return None
            
        predictions = {}
        
        for party in self.parties:
            if party not in self.models:
                continue
                
            # Özellik vektörü oluştur
            features = []
            
            # Temel özellikler
            features.append(poll_data.get('Katılımcı sayısı', 2000))
            features.append(np.log(poll_data.get('Katılımcı sayısı', 2000)))
            features.append(poll_data.get('Period', 3))
            features.append(poll_data.get('Time_Index', 100))  # Varsayılan değer
            
            # Diğer parti oyları toplamı
            other_parties_total = sum([poll_data.get(p, 0) for p in self.parties])
            features.append(other_parties_total)
            
            # Diğer parti oyları
            for other_party in self.parties:
                if other_party != party:
                    features.append(poll_data.get(other_party, 0))
            
            # Tahmin
            features_array = np.array(features).reshape(1, -1)
            features_scaled = self.scalers[party].transform(features_array)
            prediction = self.models[party].predict(features_scaled)[0]
            
            predictions[party] = max(0, prediction)  # Negatif değerleri sıfırla
            
        return predictions
    
    def save_models(self, filepath='election_models.pkl'):
        """Eğitilmiş modelleri kaydet"""
        model_data = {
            'models': self.models,
            'scalers': self.scalers,
            'feature_names': self.feature_names,
            'parties': self.parties
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"💾 Modeller kaydedildi: {filepath}")
    
    def load_models(self, filepath='election_models.pkl'):
        """Kaydedilmiş modelleri yükle"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.models = model_data['models']
            self.scalers = model_data['scalers']
            self.feature_names = model_data['feature_names']
            self.parties = model_data['parties']
            
            print(f"📂 Modeller yüklendi: {filepath}")
            return True
        except FileNotFoundError:
            print(f"⚠️ Model dosyası bulunamadı: {filepath}")
            return False

def demo_usage():
    """Kullanım örneği demonstrasyonu"""
    print("🚀 Türk Seçim Tahmin Modeli - Demo Kullanım")
    print("="*50)
    
    # Model oluştur ve eğit
    predictor = ElectionPredictor()
    predictor.load_and_train()
    
    print("\n" + "="*50)
    print("📊 ÖRNEKTAHMİNLER")
    print("="*50)
    
    # Örnek 1: Tipik bir anket verisi
    print("\n1️⃣ Tipik Anket Verisi:")
    sample_poll_1 = {
        'AK Parti': 44.0,
        'CHP': 26.5,
        'MHP': 14.5,
        'HDP': 11.5,
        'Katılımcı sayısı': 2500,
        'Period': 3,
        'Time_Index': 120
    }
    
    print("   Girdi:")
    for party, value in sample_poll_1.items():
        if party in predictor.parties:
            print(f"     {party}: %{value}")
    
    predictions_1 = predictor.predict_from_poll_data(sample_poll_1)
    print("   Tahmin:")
    if predictions_1:
        for party, pred in predictions_1.items():
            print(f"     {party}: %{pred:.1f}")
    
    # Örnek 2: Düşük katılımlı anket
    print("\n2️⃣ Düşük Katılımlı Anket:")
    sample_poll_2 = {
        'AK Parti': 42.0,
        'CHP': 28.0,
        'MHP': 16.0,
        'HDP': 10.0,
        'Katılımcı sayısı': 800,
        'Period': 3,
        'Time_Index': 110
    }
    
    print("   Girdi:")
    for party, value in sample_poll_2.items():
        if party in predictor.parties:
            print(f"     {party}: %{value}")
    
    predictions_2 = predictor.predict_from_poll_data(sample_poll_2)
    print("   Tahmin:")
    if predictions_2:
        for party, pred in predictions_2.items():
            print(f"     {party}: %{pred:.1f}")
    
    # Örnek 3: Yüksek katılımlı, AK Parti güçlü
    print("\n3️⃣ AK Parti Güçlü Senaryo:")
    sample_poll_3 = {
        'AK Parti': 48.0,
        'CHP': 23.0,
        'MHP': 13.0,
        'HDP': 12.0,
        'Katılımcı sayısı': 5000,
        'Period': 3,
        'Time_Index': 130
    }
    
    print("   Girdi:")
    for party, value in sample_poll_3.items():
        if party in predictor.parties:
            print(f"     {party}: %{value}")
    
    predictions_3 = predictor.predict_from_poll_data(sample_poll_3)
    print("   Tahmin:")
    if predictions_3:
        for party, pred in predictions_3.items():
            print(f"     {party}: %{pred:.1f}")
    
    # Model kaydetme örneği
    print("\n" + "="*50)
    print("💾 MODEL KAYDETME/YÜKLEME")
    print("="*50)
    
    # Modelleri kaydet
    predictor.save_models('my_election_models.pkl')
    
    # Yeni predictor oluştur ve kayıtlı modelleri yükle
    new_predictor = ElectionPredictor()
    if new_predictor.load_models('my_election_models.pkl'):
        print("✅ Modeller başarıyla yüklendi ve kullanıma hazır!")
    
    print("\n" + "="*50)
    print("📋 KULLANIM TALİMATLARI")
    print("="*50)
    
    usage_instructions = """
    🎯 Kendi tahminlerinizi yapmak için:
    
    1. ElectionPredictor() sınıfını oluşturun
    2. load_and_train() ile modelleri eğitin
    3. predict_from_poll_data() ile tahmin yapın
    
    📝 Girdi formatı:
    poll_data = {
        'AK Parti': 45.0,      # Anket sonucu (%)
        'CHP': 25.0,           # Anket sonucu (%)
        'MHP': 15.0,           # Anket sonucu (%)
        'HDP': 12.0,           # Anket sonucu (%)
        'Katılımcı sayısı': 2500,  # Anket katılımcı sayısı
        'Period': 3,           # Dönem (1-3 arası)
        'Time_Index': 120      # Zaman indeksi (isteğe bağlı)
    }
    
    ⚡ Hızlı kullanım:
    predictor = ElectionPredictor()
    predictor.load_and_train()
    results = predictor.predict_from_poll_data(poll_data)
    """
    
    print(usage_instructions)
    print("\n✅ Demo tamamlandı!")

if __name__ == "__main__":
    demo_usage()
