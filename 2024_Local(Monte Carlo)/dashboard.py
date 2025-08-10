"""
Kapsamlı Seçim Analizi Dashboard ve Özet Rapor Sistemi
2024 Türkiye Yerel Seçimleri için
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class ElectionDashboard:
    """Seçim sonuçları için kapsamlı dashboard ve rapor sistemi"""
    
    def __init__(self, outputs_dir: str = "outputs/"):
        self.outputs_dir = outputs_dir
        self.results = {}
        self.scenarios = {}
        
    def load_analysis_results(self):
        """Tüm analiz sonuçlarını yükler"""
        
        # Ana tahmin sonuçlarını yükle
        data_files = list(Path(self.outputs_dir + "data/").glob("detayli_sonuclar_*.json"))
        if data_files:
            latest_results = max(data_files, key=os.path.getctime)
            with open(latest_results, 'r', encoding='utf-8') as f:
                self.results = json.load(f)
            print(f"✓ Ana sonuçlar yüklendi: {latest_results.name}")
        
        # Senaryo sonuçlarını yükle (varsa)
        scenario_files = list(Path(self.outputs_dir).glob("senaryo_analizi_raporu_*.txt"))
        if scenario_files:
            latest_scenario = max(scenario_files, key=os.path.getctime)
            print(f"✓ Senaryo analizi bulundu: {latest_scenario.name}")
    
    def create_executive_summary(self) -> dict:
        """Üst düzey yönetici özeti oluşturur"""
        
        if not self.results:
            return {}
        
        summary = {
            'total_cities': len(self.results),
            'analysis_date': datetime.now().strftime('%d/%m/%Y'),
            'party_performance': {},
            'competitive_races': [],
            'safe_seats': [],
            'key_insights': [],
            'risk_alerts': []
        }
        
        # Parti performansı
        party_wins = {}
        competitive_cities = []
        safe_cities = []
        
        for city, result in self.results.items():
            # En yüksek kazanma olasılığı
            top_party = max(result['win_probabilities'].items(), key=lambda x: x[1])
            party = top_party[0]
            probability = top_party[1]
            
            # Parti kazanımları
            if probability > 60:  # Güçlü favoriler
                party_wins[party] = party_wins.get(party, 0) + 1
                safe_cities.append({
                    'city': city,
                    'party': party,
                    'probability': probability
                })
            elif probability > 40:  # Çekişmeli
                competitive_cities.append({
                    'city': city,
                    'leading_party': party,
                    'probability': probability,
                    'margin': probability - sorted(result['win_probabilities'].values(), reverse=True)[1]
                })
        
        summary['party_performance'] = party_wins
        summary['competitive_races'] = sorted(competitive_cities, key=lambda x: x['margin'])[:10]
        summary['safe_seats'] = safe_cities
        
        # Ana bulgular
        total_cities = len(self.results)
        competitive_count = len(competitive_cities)
        
        summary['key_insights'] = [
            f"Toplam {total_cities} il analiz edildi",
            f"{competitive_count} il çekişmeli yarış gösteriyor (%{competitive_count/total_cities*100:.1f})",
            f"En güçlü parti: {max(party_wins.items(), key=lambda x: x[1])[0] if party_wins else 'Belirlenmedi'} ({max(party_wins.values()) if party_wins else 0} il)",
            f"En çekişmeli şehir: {competitive_cities[0]['city'] if competitive_cities else 'Yok'}"
        ]
        
        # Risk uyarıları
        high_risk_cities = []
        low_poll_cities = []
        
        for city, result in self.results.items():
            poll_count = result['poll_stats']['poll_count']
            top_prob = max(result['win_probabilities'].values())
            
            if poll_count < 5:
                low_poll_cities.append(city)
            
            if top_prob < 45:
                high_risk_cities.append(city)
        
        summary['risk_alerts'] = [
            f"{len(low_poll_cities)} ilde yetersiz anket verisi",
            f"{len(high_risk_cities)} ilde yüksek belirsizlik",
            "Son dakika gelişmeleri sonuçları değiştirebilir"
        ]
        
        return summary
    
    def create_national_overview(self, output_dir: str = "outputs/graphs/"):
        """Ulusal genel bakış görselleri"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Parti bazında il dağılımı (pasta grafiği)
        plt.figure(figsize=(12, 8))
        
        party_wins = {}
        for city, result in self.results.items():
            top_party = max(result['win_probabilities'].items(), key=lambda x: x[1])
            if top_party[1] > 50:  # %50'den fazla kazanma olasılığı
                party = top_party[0]
                party_wins[party] = party_wins.get(party, 0) + 1
        
        if party_wins:
            # Belirsiz iller
            total_analyzed = len(self.results)
            certain_wins = sum(party_wins.values())
            uncertain = total_analyzed - certain_wins
            
            if uncertain > 0:
                party_wins['Belirsiz/Çekişmeli'] = uncertain
            
            # Pasta grafiği
            colors = plt.cm.Set3(np.linspace(0, 1, len(party_wins)))
            wedges, texts, autotexts = plt.pie(party_wins.values(), labels=party_wins.keys(), 
                                              autopct='%1.1f%%', colors=colors, startangle=90)
            
            plt.title('2024 Yerel Seçimler - Parti Bazında İl Dağılımı Projeksiyonu', fontsize=14, pad=20)
            
            # İstatistikleri ekle
            plt.figtext(0.02, 0.02, f'Toplam {total_analyzed} il analiz edildi', fontsize=10)
            plt.figtext(0.02, 0.05, f'Kesin sonuç: {certain_wins} il (%{certain_wins/total_analyzed*100:.1f})', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'ulusal_genel_bakis_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Kazanma olasılıkları histogram
        plt.figure(figsize=(14, 8))
        
        all_probabilities = []
        party_colors = {}
        color_map = plt.cm.Set1(np.linspace(0, 1, 8))
        
        for i, party in enumerate(['AKP', 'CHP', 'İYİ', 'MHP', 'HDP', 'DEM', 'YRP', 'ZP']):
            party_colors[party] = color_map[i]
        
        for city, result in self.results.items():
            top_party = max(result['win_probabilities'].items(), key=lambda x: x[1])
            all_probabilities.append(top_party[1])
        
        plt.hist(all_probabilities, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        plt.xlabel('En Yüksek Kazanma Olasılığı (%)')
        plt.ylabel('İl Sayısı')
        plt.title('İllerdeki Kazanma Olasılıkları Dağılımı')
        plt.grid(axis='y', alpha=0.3)
        
        # Kritik eşik çizgileri
        plt.axvline(x=50, color='red', linestyle='--', alpha=0.7, label='Çekişmeli Eşik (%50)')
        plt.axvline(x=70, color='green', linestyle='--', alpha=0.7, label='Güvenli Eşik (%70)')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'olasilik_dagilimi_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. İl bazında detaylı tablo (top 20 most competitive)
        fig, ax = plt.subplots(figsize=(16, 10))
        ax.axis('tight')
        ax.axis('off')
        
        # En çekişmeli 20 şehir
        competitive_data = []
        for city, result in self.results.items():
            probs = sorted(result['win_probabilities'].values(), reverse=True)
            if len(probs) >= 2:
                margin = probs[0] - probs[1]
                top_party = max(result['win_probabilities'].items(), key=lambda x: x[1])
                competitive_data.append({
                    'city': city,
                    'leading_party': top_party[0],
                    'probability': top_party[1],
                    'margin': margin
                })
        
        competitive_data.sort(key=lambda x: x['margin'])
        top_competitive = competitive_data[:20]
        
        table_data = []
        for item in top_competitive:
            table_data.append([
                item['city'],
                item['leading_party'],
                f"{item['probability']:.1f}%",
                f"{item['margin']:.1f}%"
            ])
        
        table = ax.table(cellText=table_data,
                        colLabels=['İl', 'Önde Olan Parti', 'Kazanma Olasılığı', 'Fark'],
                        cellLoc='center',
                        loc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)
        
        # Başlık çizgileri renklendir
        for i in range(len(table_data[0])):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        plt.title('En Çekişmeli 20 İl - Detaylı Analiz', fontsize=16, pad=20)
        plt.savefig(os.path.join(output_dir, f'cekismeli_iller_tablosu_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Ulusal genel bakış görselleri oluşturuldu: {output_dir}")
    
    def generate_executive_report(self, output_dir: str = "outputs/reports/") -> str:
        """Üst düzey yönetici raporu oluşturur"""
        
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(output_dir, f"yonetici_ozet_raporu_{timestamp}.txt")
        
        summary = self.create_executive_summary()
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("🗳️  " + "=" * 70 + "\n")
            f.write("2024 TÜRKİYE YEREL SEÇİMLERİ\n")
            f.write("YÖNETİCİ ÖZET RAPORU\n")
            f.write("Gelişmiş Monte Carlo Analizi Sonuçları\n")
            f.write("=" * 76 + "\n\n")
            
            f.write(f"📅 Rapor Tarihi: {summary.get('analysis_date', 'Bilinmiyor')}\n")
            f.write(f"📊 Analiz Kapsamı: {summary.get('total_cities', 0)} İl\n")
            f.write(f"🔬 Metodoloji: Monte Carlo Simülasyonu (50,000 iterasyon/il)\n\n")
            
            # Anahtar Bulgular
            f.write("🔍 ANAHTAR BULGULAR\n")
            f.write("-" * 40 + "\n")
            for insight in summary.get('key_insights', []):
                f.write(f"• {insight}\n")
            f.write("\n")
            
            # Parti Performansı
            f.write("🏆 PARTİ PERFORMANS TABLOSU\n")
            f.write("-" * 40 + "\n")
            party_performance = summary.get('party_performance', {})
            if party_performance:
                sorted_parties = sorted(party_performance.items(), key=lambda x: x[1], reverse=True)
                for i, (party, count) in enumerate(sorted_parties, 1):
                    percentage = count / summary.get('total_cities', 1) * 100
                    f.write(f"{i:2d}. {party:>8s}: {count:2d} il (%{percentage:4.1f})\n")
            f.write("\n")
            
            # En Çekişmeli Yarışlar
            f.write("⚡ EN ÇEKİŞMELİ 10 YARIŞ\n")
            f.write("-" * 40 + "\n")
            competitive_races = summary.get('competitive_races', [])[:10]
            if competitive_races:
                f.write(f"{'İl':<15} {'Öndeki Parti':<10} {'Olasılık':<10} {'Fark':<8}\n")
                f.write("-" * 43 + "\n")
                for race in competitive_races:
                    city = race['city'][:14]  # İl adını kısalt
                    party = race['leading_party'][:9]
                    prob = f"{race['probability']:.1f}%"
                    margin = f"{race['margin']:.1f}%"
                    f.write(f"{city:<15} {party:<10} {prob:<10} {margin:<8}\n")
            f.write("\n")
            
            # Risk Değerlendirmesi
            f.write("⚠️  RİSK DEĞERLENDİRMESİ\n")
            f.write("-" * 40 + "\n")
            for alert in summary.get('risk_alerts', []):
                f.write(f"🔴 {alert}\n")
            f.write("\n")
            
            # Stratejik Öneriler
            f.write("💡 STRATEJİK ÖNERİLER\n")
            f.write("-" * 40 + "\n")
            f.write("1. Çekişmeli şehirlerde yoğun saha çalışması yapılmalı\n")
            f.write("2. Yetersiz anket verisi olan illerde ek araştırma gerekli\n")
            f.write("3. Son 2 hafta kritik - günlük izleme önerilir\n")
            f.write("4. Katılım oranı stratejileri gözden geçirilmeli\n")
            f.write("5. Kararsız seçmen profili detaylı analiz edilmeli\n\n")
            
            # Metodoloji Notu
            f.write("📋 METODOLOJİ NOTU\n")
            f.write("-" * 40 + "\n")
            f.write("Bu analiz, mevcut anket verilerini kullanarak Monte Carlo\n")
            f.write("simülasyon tekniği ile gerçekleştirilmiştir. Sonuçlar:\n")
            f.write("• Anket hatası, örnekleme yanlılığı ve belirsizlik faktörleri\n")
            f.write("• Kararsız seçmen dağılımı senaryoları\n")
            f.write("• Katılım oranı değişkenleri\n")
            f.write("• Son dakika oy değişimi olasılıkları\n")
            f.write("parametreleri ile hesaplanmıştır.\n\n")
            
            f.write("⚖️  Yasal Uyarı: Bu analiz akademik amaçlıdır ve kesin\n")
            f.write("sonuç garantisi vermez. Gerçek seçim sonuçları farklılık\n")
            f.write("gösterebilir.\n")
        
        print(f"📋 Yönetici özet raporu oluşturuldu: {report_file}")
        return report_file
    
    def create_comparison_analysis(self, output_dir: str = "outputs/graphs/"):
        """2019 seçimleri ile karşılaştırma analizi"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 2019 sonuçları vs 2024 tahminleri karşılaştırması
        plt.figure(figsize=(16, 10))
        
        # Her parti için beklenen değişim
        party_changes = {
            'AKP': {'2019_estimate': 35, '2024_prediction': 0, 'cities_won': 0},
            'CHP': {'2019_estimate': 30, '2024_prediction': 0, 'cities_won': 0},
            'İYİ': {'2019_estimate': 8, '2024_prediction': 0, 'cities_won': 0},
            'MHP': {'2019_estimate': 15, '2024_prediction': 0, 'cities_won': 0},
            'HDP/DEM': {'2019_estimate': 12, '2024_prediction': 0, 'cities_won': 0}
        }
        
        # 2024 tahminlerini hesapla
        total_cities = len(self.results)
        for city, result in self.results.items():
            top_party = max(result['win_probabilities'].items(), key=lambda x: x[1])
            if top_party[1] > 50:
                if top_party[0] in party_changes:
                    party_changes[top_party[0]]['cities_won'] += 1
                elif top_party[0] in ['HDP', 'DEM']:
                    party_changes['HDP/DEM']['cities_won'] += 1
        
        # Karşılaştırma grafiği
        parties = list(party_changes.keys())
        prediction_2024 = [party_changes[party]['cities_won'] for party in parties]
        
        x = np.arange(len(parties))
        width = 0.35
        
        plt.bar(x, prediction_2024, width, label='2024 Tahmin', alpha=0.8)
        plt.xlabel('Partiler')
        plt.ylabel('Kazanılan İl Sayısı')
        plt.title('2024 Yerel Seçimler - Parti Bazında İl Kazanım Projeksiyonu')
        plt.xticks(x, parties, rotation=45)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        # Değerleri grafiğin üstüne ekle
        for i, v in enumerate(prediction_2024):
            plt.text(i, v + 0.5, str(v), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'parti_karsilastirma_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Karşılaştırma analizi oluşturuldu: {output_dir}")

def main():
    """Ana dashboard çalıştırma fonksiyonu"""
    print("📊 2024 Yerel Seçimler - Kapsamlı Dashboard ve Rapor Sistemi")
    print("=" * 70)
    
    # Dashboard'u başlat
    dashboard = ElectionDashboard()
    
    # Sonuçları yükle
    print("\n📁 Analiz sonuçları yükleniyor...")
    dashboard.load_analysis_results()
    
    if not dashboard.results:
        print("❌ Analiz sonuçları bulunamadı! Önce ana analizleri çalıştırın.")
        return
    
    # Üst düzey özeti oluştur
    print("\n📋 Yönetici özet raporu oluşturuluyor...")
    dashboard.generate_executive_report()
    
    # Ulusal genel bakış görselleri
    print("\n📊 Ulusal genel bakış görselleri oluşturuluyor...")
    dashboard.create_national_overview()
    
    # Karşılaştırma analizi
    print("\n📈 Karşılaştırma analizi oluşturuluyor...")
    dashboard.create_comparison_analysis()
    
    # Özet istatistikler
    summary = dashboard.create_executive_summary()
    
    print("\n" + "=" * 70)
    print("🎯 ANALİZ ÖZETİ")
    print("=" * 70)
    print(f"📊 Toplam analiz edilen il: {summary.get('total_cities', 0)}")
    print(f"⚡ Çekişmeli yarış sayısı: {len(summary.get('competitive_races', []))}")
    
    party_performance = summary.get('party_performance', {})
    if party_performance:
        print(f"🏆 En başarılı parti: {max(party_performance.items(), key=lambda x: x[1])[0]} ({max(party_performance.values())} il)")
    
    print("\n✅ Tüm raporlar ve görseller oluşturuldu!")
    print("📁 Sonuçlar 'outputs/' klasörlerinde bulunabilir.")

if __name__ == "__main__":
    main()
