"""
Gelişmiş Monte Carlo Seçim Tahmin Sistemi
2024 Türkiye Yerel Seçimleri için
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # GUI olmadan çalışması için
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime, timedelta
import warnings
import os
import glob
from typing import Dict, List, Tuple, Optional
import json

warnings.filterwarnings('ignore')

class AdvancedElectionPredictor:
    """Gelişmiş Monte Carlo tabanlı seçim tahmin sistemi"""
    
    def __init__(self, data_path: str = "data/processed_data/iller/"):
        self.data_path = data_path
        self.city_data = {}
        self.prediction_results = {}
        self.uncertainty_factors = {
            'poll_error': 0.03,  # Anket hatası (±3%)
            'turnout_variation': 0.05,  # Katılım değişkenliği (±5%)
            'undecided_allocation': 0.08,  # Kararsız seçmen dağılımı (±8%)
            'late_swing': 0.02,  # Son dakika değişimi (±2%)
            'sampling_bias': 0.025,  # Örnekleme yanlılığı (±2.5%)
        }
        
    def load_city_data(self) -> Dict:
        """Her il için anket verilerini yükler ve temizler"""
        csv_files = glob.glob(os.path.join(self.data_path, "*.csv"))
        
        for file_path in csv_files:
            city_name = os.path.basename(file_path).replace('.csv', '')
            
            if city_name == 'Tum_Birlesik':
                continue
                
            try:
                df = pd.read_csv(file_path, encoding='utf-8')
                
                # Veri temizleme
                df = self._clean_poll_data(df, city_name)
                
                if not df.empty:
                    self.city_data[city_name] = df
                    print(f"✓ {city_name}: {len(df)} anket verisi yüklendi")
                else:
                    print(f"⚠ {city_name}: Veri temizleme sonrası boş dataset")
                    
            except Exception as e:
                print(f"✗ {city_name}: Veri yükleme hatası - {str(e)}")
                
        print(f"\nToplam {len(self.city_data)} il verisi başarıyla yüklendi.")
        return self.city_data
    
    def _clean_poll_data(self, df: pd.DataFrame, city_name: str) -> pd.DataFrame:
        """Anket verilerini temizler ve standardize eder"""
        
        # Gerekli sütunları kontrol et
        required_columns = ['AKP', 'CHP', 'İYİ', 'MHP']
        party_columns = [col for col in required_columns if col in df.columns]
        
        if len(party_columns) < 2:
            return pd.DataFrame()
        
        # Tarih sütununu parse et
        if 'Tarih' in df.columns:
            df = self._parse_dates(df)
        
        # Parti verilerini sayısal formata çevir ve temizle
        for col in party_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)
        
        # Anormal değerleri temizle (1000'den büyük değerler /10 ile böl)
        for col in party_columns:
            df.loc[df[col] > 100, col] = df.loc[df[col] > 100, col] / 10
        
        # Satır toplamı 100'den çok farklıysa normalize et
        df_clean = df.copy()
        for idx, row in df.iterrows():
            party_total = sum([row[col] for col in party_columns if not pd.isna(row[col])])
            if party_total > 0 and (party_total < 50 or party_total > 150):
                # Normalleştir
                factor = 100 / party_total
                for col in party_columns:
                    if not pd.isna(row[col]):
                        df_clean.loc[idx, col] = row[col] * factor
        
        # Eksik parti verilerini sıfır ile doldur
        all_parties = ['AKP', 'CHP', 'İYİ', 'MHP', 'HDP', 'DEM', 'YRP', 'ZP']
        for party in all_parties:
            if party not in df_clean.columns:
                df_clean[party] = 0
            else:
                df_clean[party] = df_clean[party].fillna(0)
        
        # Son 6 ay içindeki anketleri öncelikle al
        if 'parsed_date' in df_clean.columns:
            recent_cutoff = datetime(2024, 1, 1)
            recent_data = df_clean[df_clean['parsed_date'] >= recent_cutoff]
            if len(recent_data) >= 3:
                df_clean = recent_data
        
        return df_clean
    
    def _parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Tarih sütununu parse eder"""
        df['parsed_date'] = pd.NaT
        
        for idx, date_str in df['Tarih'].items():
            if pd.isna(date_str):
                continue
                
            try:
                # Türkçe ay isimleri
                turkish_months = {
                    'Ocak': 'January', 'Şubat': 'February', 'Mart': 'March',
                    'Nisan': 'April', 'Mayıs': 'May', 'Haziran': 'June',
                    'Temmuz': 'July', 'Ağustos': 'August', 'Eylül': 'September',
                    'Ekim': 'October', 'Kasım': 'November', 'Aralık': 'December'
                }
                
                date_str = str(date_str).strip()
                
                # Türkçe ay isimlerini İngilizce'ye çevir
                for tr_month, en_month in turkish_months.items():
                    date_str = date_str.replace(tr_month, en_month)
                
                # Farklı tarih formatlarını dene
                if 'Mart' in date_str or 'March' in date_str:
                    df.loc[idx, 'parsed_date'] = datetime(2024, 3, 15)
                elif 'Şubat' in date_str or 'February' in date_str:
                    df.loc[idx, 'parsed_date'] = datetime(2024, 2, 15)
                elif '2024' in date_str:
                    df.loc[idx, 'parsed_date'] = datetime(2024, 3, 1)
                elif '2023' in date_str:
                    df.loc[idx, 'parsed_date'] = datetime(2023, 12, 1)
                else:
                    df.loc[idx, 'parsed_date'] = datetime(2024, 2, 1)
                    
            except:
                df.loc[idx, 'parsed_date'] = datetime(2024, 2, 1)
        
        return df
    
    def calculate_weighted_averages(self, city_name: str) -> Dict:
        """Ağırlıklı anket ortalamalarını hesaplar"""
        if city_name not in self.city_data:
            return {}
        
        df = self.city_data[city_name]
        parties = ['AKP', 'CHP', 'İYİ', 'MHP', 'HDP', 'DEM', 'YRP', 'ZP']
        
        # Zaman ağırlığı (yeni anketler daha yüksek ağırlık)
        if 'parsed_date' in df.columns:
            max_date = df['parsed_date'].max()
            df['time_weight'] = df['parsed_date'].apply(
                lambda x: np.exp(-((max_date - x).days / 30)) if pd.notnull(x) else 0.1
            )
        else:
            df['time_weight'] = 1.0
        
        # Örneklem büyüklüğü ağırlığı
        if 'Örneklem' in df.columns:
            df['sample_weight'] = pd.to_numeric(df['Örneklem'], errors='coerce').fillna(1000)
            df['sample_weight'] = np.sqrt(df['sample_weight']) / 100
        else:
            df['sample_weight'] = 1.0
        
        # Anket şirketi güvenilirlik ağırlığı
        company_weights = {
            'ASAL': 1.2, 'ORC': 1.1, 'AREA': 1.0, 'Areda Survey': 1.0,
            'SAROS': 1.1, 'MAK': 0.9, 'Avrasya': 0.8, 'ADA': 0.9,
            'GENAR': 1.0, 'Pollstar': 1.0, 'default': 0.9
        }
        
        if 'Anket_Şirketi' in df.columns:
            df['company_weight'] = df['Anket_Şirketi'].map(company_weights).fillna(0.9)
        else:
            df['company_weight'] = 1.0
        
        # Toplam ağırlık
        df['total_weight'] = df['time_weight'] * df['sample_weight'] * df['company_weight']
        
        # Ağırlıklı ortalama hesapla
        weighted_averages = {}
        std_deviations = {}
        
        for party in parties:
            if party in df.columns:
                party_data = df[df[party] > 0]  # Sıfır olmayan değerler
                if len(party_data) > 0:
                    weights = party_data['total_weight']
                    values = party_data[party]
                    
                    weighted_avg = np.average(values, weights=weights)
                    # Ağırlıklı standart sapma
                    weighted_var = np.average((values - weighted_avg) ** 2, weights=weights)
                    weighted_std = np.sqrt(weighted_var)
                    
                    weighted_averages[party] = weighted_avg
                    std_deviations[party] = max(weighted_std, 1.0)  # Minimum belirsizlik
                else:
                    weighted_averages[party] = 0
                    std_deviations[party] = 2.0
            else:
                weighted_averages[party] = 0
                std_deviations[party] = 2.0
        
        return {
            'averages': weighted_averages,
            'std_deviations': std_deviations,
            'poll_count': len(df),
            'last_poll_date': df['parsed_date'].max() if 'parsed_date' in df.columns else None
        }
    
    def run_monte_carlo_simulation(self, city_name: str, n_simulations: int = 50000) -> Dict:
        """Gelişmiş Monte Carlo simülasyonu çalıştırır"""
        
        stats = self.calculate_weighted_averages(city_name)
        if not stats:
            return {}
        
        averages = stats['averages']
        std_devs = stats['std_deviations']
        
        parties = list(averages.keys())
        simulations = []
        
        for _ in range(n_simulations):
            simulation = {}
            
            # Her parti için oy oranı simüle et
            for party in parties:
                base_vote = averages[party]
                uncertainty = std_devs[party]
                
                # Çoklu belirsizlik faktörlerini ekle
                total_uncertainty = np.sqrt(
                    uncertainty**2 +
                    (base_vote * self.uncertainty_factors['poll_error'])**2 +
                    (base_vote * self.uncertainty_factors['sampling_bias'])**2 +
                    (self.uncertainty_factors['undecided_allocation'] * 10)**2 +
                    (base_vote * self.uncertainty_factors['late_swing'])**2
                )
                
                # Beta dağılımı kullan (0-100 arası sınırlı)
                if base_vote > 0:
                    # Beta dağılımı parametreleri
                    mean_scaled = base_vote / 100
                    var_scaled = (total_uncertainty / 100) ** 2
                    
                    if var_scaled > 0 and mean_scaled > 0 and mean_scaled < 1:
                        alpha = mean_scaled * (mean_scaled * (1 - mean_scaled) / var_scaled - 1)
                        beta = (1 - mean_scaled) * (mean_scaled * (1 - mean_scaled) / var_scaled - 1)
                        
                        if alpha > 0 and beta > 0:
                            simulated_vote = np.random.beta(alpha, beta) * 100
                        else:
                            simulated_vote = np.random.normal(base_vote, total_uncertainty)
                    else:
                        simulated_vote = np.random.normal(base_vote, total_uncertainty)
                else:
                    simulated_vote = abs(np.random.normal(0, 2))
                
                simulation[party] = max(0, simulated_vote)
            
            # Toplam %100'e normalize et
            total = sum(simulation.values())
            if total > 0:
                simulation = {party: (vote/total)*100 for party, vote in simulation.items()}
                simulations.append(simulation)
        
        # Sonuçları analiz et
        results_df = pd.DataFrame(simulations)
        
        analysis = {
            'city': city_name,
            'simulations_count': len(simulations),
            'mean_votes': results_df.mean().to_dict(),
            'std_votes': results_df.std().to_dict(),
            'confidence_intervals': {},
            'win_probabilities': {},
            'margin_analysis': {},
            'poll_stats': stats
        }
        
        # Güven aralıkları
        for party in parties:
            if party in results_df.columns:
                analysis['confidence_intervals'][party] = {
                    '95%': [
                        results_df[party].quantile(0.025),
                        results_df[party].quantile(0.975)
                    ],
                    '90%': [
                        results_df[party].quantile(0.05),
                        results_df[party].quantile(0.95)
                    ],
                    '80%': [
                        results_df[party].quantile(0.1),
                        results_df[party].quantile(0.9)
                    ]
                }
        
        # Kazanma olasılıkları
        winners = results_df.idxmax(axis=1)
        win_counts = winners.value_counts(normalize=True) * 100
        analysis['win_probabilities'] = win_counts.to_dict()
        
        # Fark analizleri
        for party in parties:
            if party in results_df.columns:
                party_votes = results_df[party]
                other_max = results_df.drop(columns=[party]).max(axis=1)
                margins = party_votes - other_max
                
                analysis['margin_analysis'][party] = {
                    'average_margin': margins.mean(),
                    'prob_win_5plus': (margins >= 5).mean() * 100,
                    'prob_win_10plus': (margins >= 10).mean() * 100,
                    'close_race_prob': (abs(margins) <= 3).mean() * 100
                }
        
        return analysis
    
    def predict_all_cities(self, n_simulations: int = 50000) -> Dict:
        """Tüm iller için tahmin yapar"""
        print(f"\n🚀 {len(self.city_data)} il için Monte Carlo simülasyonu başlıyor...")
        print(f"Simülasyon sayısı: {n_simulations:,}")
        
        all_results = {}
        
        for i, city_name in enumerate(self.city_data.keys(), 1):
            print(f"[{i}/{len(self.city_data)}] {city_name} analiz ediliyor...")
            
            result = self.run_monte_carlo_simulation(city_name, n_simulations)
            if result:
                all_results[city_name] = result
                
                # İlk üç parti ve kazanma olasılıkları
                top_parties = sorted(
                    result['win_probabilities'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:3]
                
                print(f"  Kazanma olasılıkları: ", end="")
                for party, prob in top_parties:
                    print(f"{party}: %{prob:.1f}", end="  ")
                print()
        
        self.prediction_results = all_results
        return all_results
    
    def generate_comprehensive_report(self, output_dir: str = "outputs/") -> str:
        """Kapsamlı analiz raporu oluşturur"""
        if not self.prediction_results:
            print("❌ Önce tahminleri çalıştırın!")
            return ""
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Rapor dosyası
        report_file = os.path.join(output_dir, f"secim_tahmin_raporu_{timestamp}.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("2024 TÜRKİYE YEREL SEÇİMLERİ TAHMİN RAPORU\n")
            f.write("Gelişmiş Monte Carlo Simülasyon Analizi\n")
            f.write("=" * 80 + "\n")
            f.write(f"Oluşturulma Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Analiz Edilen İl Sayısı: {len(self.prediction_results)}\n")
            f.write(f"Toplam Simülasyon: {50000:,} (il başına)\n\n")
            
            # Genel özet
            f.write("GENEL ÖZET\n")
            f.write("-" * 40 + "\n")
            
            # Parti kazanım sayıları
            party_wins = {}
            total_cities = len(self.prediction_results)
            
            for city, result in self.prediction_results.items():
                top_party = max(result['win_probabilities'].items(), key=lambda x: x[1])
                if top_party[1] > 50:  # %50'den fazla kazanma olasılığı
                    party = top_party[0]
                    party_wins[party] = party_wins.get(party, 0) + 1
            
            f.write("Parti Bazında Kazanım Projeksiyonu:\n")
            for party, count in sorted(party_wins.items(), key=lambda x: x[1], reverse=True):
                f.write(f"  {party}: {count} il (%{count/total_cities*100:.1f})\n")
            
            uncertain_count = total_cities - sum(party_wins.values())
            f.write(f"  Belirsiz/Çekişmeli: {uncertain_count} il (%{uncertain_count/total_cities*100:.1f})\n\n")
            
            # İl bazında detaylar
            f.write("İL BAZINDA DETAYLI ANALİZ\n")
            f.write("=" * 80 + "\n\n")
            
            for city in sorted(self.prediction_results.keys()):
                result = self.prediction_results[city]
                f.write(f"{city.upper()}\n")
                f.write("-" * len(city) + "\n")
                
                # En yüksek kazanma olasılıklı üç parti
                top_parties = sorted(
                    result['win_probabilities'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:3]
                
                f.write("Kazanma Olasılıkları:\n")
                for i, (party, prob) in enumerate(top_parties, 1):
                    mean_vote = result['mean_votes'][party]
                    ci_95 = result['confidence_intervals'][party]['95%']
                    f.write(f"  {i}. {party}: %{prob:.1f} kazanma | Oy: %{mean_vote:.1f} (95% GA: %{ci_95[0]:.1f}-%{ci_95[1]:.1f})\n")
                
                # Çekişme analizi
                if len(top_parties) >= 2:
                    first_prob = top_parties[0][1]
                    second_prob = top_parties[1][1]
                    
                    if first_prob < 60:
                        f.write(f"  ⚡ ÇEKİŞMELİ YARIŞ: İlk iki parti arasında fark az!\n")
                    elif first_prob > 80:
                        f.write(f"  🏆 NET ÖNDE: {top_parties[0][0]} güçlü favoride\n")
                    else:
                        f.write(f"  📊 KARARSIZ: Sonuç belirsiz, kampanya önemli\n")
                
                # Anket güvenilirliği
                poll_count = result['poll_stats']['poll_count']
                if poll_count < 3:
                    f.write(f"  ⚠️  Az anket verisi ({poll_count} anket) - sonuçlar dikkatli yorumlanmalı\n")
                elif poll_count > 10:
                    f.write(f"  ✅ Yeterli anket verisi ({poll_count} anket) - güvenilir tahmin\n")
                
                f.write("\n")
        
        print(f"📄 Detaylı rapor oluşturuldu: {report_file}")
        return report_file
    
    def create_visualizations(self, output_dir: str = "outputs/graphs/"):
        """Görsel analizler oluşturur"""
        if not self.prediction_results:
            print("❌ Önce tahminleri çalıştırın!")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Genel kazanma olasılıkları haritası
        plt.figure(figsize=(15, 10))
        
        # Şehir isimleri ve en yüksek olasılıklı parti
        cities = []
        winning_parties = []
        win_probs = []
        
        for city, result in self.prediction_results.items():
            top_party = max(result['win_probabilities'].items(), key=lambda x: x[1])
            cities.append(city)
            winning_parties.append(top_party[0])
            win_probs.append(top_party[1])
        
        # Renk haritası
        unique_parties = list(set(winning_parties))
        colors = plt.cm.Set1(np.linspace(0, 1, len(unique_parties)))
        party_colors = dict(zip(unique_parties, colors))
        
        city_colors = [party_colors[party] for party in winning_parties]
        
        # Bar chart
        plt.barh(range(len(cities)), win_probs, color=city_colors)
        plt.yticks(range(len(cities)), cities)
        plt.xlabel('Kazanma Olasılığı (%)')
        plt.title('İl Bazında Kazanma Olasılıkları - 2024 Yerel Seçimler')
        plt.grid(axis='x', alpha=0.3)
        
        # Efsane
        legend_elements = [plt.Rectangle((0,0),1,1, facecolor=party_colors[party], label=party) 
                          for party in unique_parties]
        plt.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'kazanma_olasiliklari_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Parti bazında genel durum
        plt.figure(figsize=(12, 8))
        
        party_total_wins = {}
        for result in self.prediction_results.values():
            for party, prob in result['win_probabilities'].items():
                if prob > 50:  # %50'den fazla kazanma olasılığı
                    party_total_wins[party] = party_total_wins.get(party, 0) + 1
        
        if party_total_wins:
            parties = list(party_total_wins.keys())
            win_counts = list(party_total_wins.values())
            
            plt.pie(win_counts, labels=parties, autopct='%1.1f%%', startangle=90)
            plt.title('Parti Bazında İl Kazanım Oranları')
        
        plt.savefig(os.path.join(output_dir, f'parti_dagilimi_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Görsel analizler oluşturuldu: {output_dir}")
    
    def save_detailed_results(self, output_dir: str = "outputs/data/"):
        """Detaylı sonuçları JSON formatında kaydeder"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON serileştirme için datetime objelerini string'e çevir
        serializable_results = {}
        for city, result in self.prediction_results.items():
            serializable_result = result.copy()
            if 'poll_stats' in serializable_result and 'last_poll_date' in serializable_result['poll_stats']:
                last_date = serializable_result['poll_stats']['last_poll_date']
                if last_date and not pd.isna(last_date):
                    serializable_result['poll_stats']['last_poll_date'] = last_date.strftime('%Y-%m-%d')
                else:
                    serializable_result['poll_stats']['last_poll_date'] = None
            serializable_results[city] = serializable_result
        
        output_file = os.path.join(output_dir, f'detayli_sonuclar_{timestamp}.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Detaylı sonuçlar kaydedildi: {output_file}")

def main():
    """Ana çalıştırma fonksiyonu"""
    print("🗳️  2024 Türkiye Yerel Seçimleri - Gelişmiş Monte Carlo Tahmin Sistemi")
    print("=" * 80)
    
    # Sistemi başlat
    predictor = AdvancedElectionPredictor()
    
    # Veri yükle
    print("\n📊 Anket verileri yükleniyor...")
    city_data = predictor.load_city_data()
    
    if not city_data:
        print("❌ Hiç veri yüklenemedi! Veri dosyalarını kontrol edin.")
        return
    
    # Tahminleri çalıştır
    print("\n🎯 Monte Carlo simülasyonları başlıyor...")
    results = predictor.predict_all_cities(n_simulations=50000)
    
    if not results:
        print("❌ Tahmin hesaplanamadı!")
        return
    
    # Raporları oluştur
    print("\n📄 Raporlar oluşturuluyor...")
    report_file = predictor.generate_comprehensive_report()
    
    print("\n📊 Görsel analizler oluşturuluyor...")
    predictor.create_visualizations()
    
    print("\n💾 Detaylı sonuçlar kaydediliyor...")
    predictor.save_detailed_results()
    
    print("\n✅ Analiz tamamlandı!")
    print(f"📁 Sonuçlar 'outputs/' klasöründe")
    print(f"📄 Ana rapor: {os.path.basename(report_file)}")

if __name__ == "__main__":
    main()
