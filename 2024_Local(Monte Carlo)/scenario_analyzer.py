"""
Gelişmiş Senaryo Analizi ve Risk Değerlendirme Modülü
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
from advanced_election_predictor import AdvancedElectionPredictor

class ElectionScenarioAnalyzer:
    """Seçim senaryoları ve risk analizi"""
    
    def __init__(self, predictor: AdvancedElectionPredictor):
        self.predictor = predictor
        self.scenarios = {}
        
    def analyze_turnout_scenarios(self, city_name: str, turnout_variations: list = [0.6, 0.7, 0.8, 0.85]) -> dict:
        """Farklı katılım oranları için senaryo analizi"""
        
        base_stats = self.predictor.calculate_weighted_averages(city_name)
        if not base_stats:
            return {}
        
        scenario_results = {}
        
        for turnout in turnout_variations:
            # Düşük katılım genelde statükocu partileri avantajlı hale getirir
            turnout_modifier = {
                'AKP': 1.0 + (0.85 - turnout) * 0.3,  # Düşük katılımda avantajlı
                'MHP': 1.0 + (0.85 - turnout) * 0.2,
                'CHP': 1.0 - (0.85 - turnout) * 0.1,  # Yüksek katılımda avantajlı
                'İYİ': 1.0 - (0.85 - turnout) * 0.15,
                'HDP': 1.0 - (0.85 - turnout) * 0.2,
                'DEM': 1.0 - (0.85 - turnout) * 0.2,
                'YRP': 1.0,
                'ZP': 1.0
            }
            
            # Modifiye edilmiş ortalamalar
            modified_averages = {}
            for party, avg in base_stats['averages'].items():
                modifier = turnout_modifier.get(party, 1.0)
                modified_averages[party] = avg * modifier
            
            # Yeniden normalize et
            total = sum(modified_averages.values())
            if total > 0:
                modified_averages = {party: (vote/total)*100 for party, vote in modified_averages.items()}
            
            # Monte Carlo simülasyonu çalıştır
            scenario_results[f"turnout_{int(turnout*100)}"] = {
                'turnout_rate': turnout,
                'modified_averages': modified_averages,
                'winning_party': max(modified_averages.items(), key=lambda x: x[1])[0],
                'winning_percentage': max(modified_averages.values())
            }
        
        return scenario_results
    
    def analyze_undecided_allocation(self, city_name: str, undecided_scenarios: dict = None) -> dict:
        """Kararsız seçmenlerin farklı dağılım senaryoları"""
        
        if undecided_scenarios is None:
            undecided_scenarios = {
                'status_quo': {'AKP': 0.3, 'CHP': 0.25, 'İYİ': 0.15, 'MHP': 0.1, 'others': 0.2},
                'change_wave': {'AKP': 0.15, 'CHP': 0.3, 'İYİ': 0.25, 'MHP': 0.05, 'others': 0.25},
                'polarization': {'AKP': 0.4, 'CHP': 0.35, 'İYİ': 0.1, 'MHP': 0.1, 'others': 0.05},
                'fragmentation': {'AKP': 0.2, 'CHP': 0.2, 'İYİ': 0.2, 'MHP': 0.15, 'others': 0.25}
            }
        
        base_stats = self.predictor.calculate_weighted_averages(city_name)
        if not base_stats:
            return {}
        
        # Kararsız seçmen oranını %15 olarak varsay
        undecided_rate = 15.0
        
        scenario_results = {}
        
        for scenario_name, allocation in undecided_scenarios.items():
            modified_averages = base_stats['averages'].copy()
            
            # Kararsız seçmenleri dağıt
            for party in modified_averages.keys():
                if party in allocation:
                    modified_averages[party] += undecided_rate * allocation[party]
                elif party in ['YRP', 'ZP', 'DEM', 'HDP'] and 'others' in allocation:
                    modified_averages[party] += undecided_rate * allocation['others'] / 4
            
            scenario_results[scenario_name] = {
                'allocation': allocation,
                'modified_averages': modified_averages,
                'winning_party': max(modified_averages.items(), key=lambda x: x[1])[0],
                'winning_percentage': max(modified_averages.values())
            }
        
        return scenario_results
    
    def calculate_swing_scenarios(self, city_name: str, swing_percentages: list = [2, 5, 8]) -> dict:
        """Son dakika oy kaybı/kazancı senaryoları"""
        
        base_stats = self.predictor.calculate_weighted_averages(city_name)
        if not base_stats:
            return {}
        
        scenario_results = {}
        
        # Her parti için swing senaryoları
        for party in ['AKP', 'CHP', 'İYİ', 'MHP']:
            if party not in base_stats['averages']:
                continue
                
            for swing in swing_percentages:
                # Pozitif swing (parti lehine)
                scenario_name = f"{party}_plus_{swing}"
                modified_averages = base_stats['averages'].copy()
                modified_averages[party] += swing
                
                # Diğer partilerden orantılı olarak düş
                other_parties = [p for p in modified_averages.keys() if p != party and modified_averages[p] > 0]
                if other_parties:
                    total_others = sum(modified_averages[p] for p in other_parties)
                    if total_others > 0:
                        for other_party in other_parties:
                            reduction = (modified_averages[other_party] / total_others) * swing
                            modified_averages[other_party] = max(0, modified_averages[other_party] - reduction)
                
                scenario_results[scenario_name] = {
                    'party': party,
                    'swing': f"+{swing}%",
                    'modified_averages': modified_averages,
                    'winning_party': max(modified_averages.items(), key=lambda x: x[1])[0],
                    'winning_percentage': max(modified_averages.values())
                }
                
                # Negatif swing (parti aleyhine)
                if base_stats['averages'][party] > swing:
                    scenario_name = f"{party}_minus_{swing}"
                    modified_averages = base_stats['averages'].copy()
                    modified_averages[party] -= swing
                    
                    # Diğer partilere orantılı olarak ekle
                    if other_parties:
                        for other_party in other_parties:
                            if total_others > 0:
                                increase = (modified_averages[other_party] / total_others) * swing
                                modified_averages[other_party] += increase
                    
                    scenario_results[scenario_name] = {
                        'party': party,
                        'swing': f"-{swing}%",
                        'modified_averages': modified_averages,
                        'winning_party': max(modified_averages.items(), key=lambda x: x[1])[0],
                        'winning_percentage': max(modified_averages.values())
                    }
        
        return scenario_results
    
    def comprehensive_city_analysis(self, city_name: str) -> dict:
        """Bir il için kapsamlı senaryo analizi"""
        
        print(f"\n🔍 {city_name} için detaylı senaryo analizi...")
        
        analysis = {
            'city': city_name,
            'base_prediction': None,
            'turnout_scenarios': {},
            'undecided_scenarios': {},
            'swing_scenarios': {},
            'risk_assessment': {},
            'stability_score': 0
        }
        
        # Temel tahmin
        if city_name in self.predictor.prediction_results:
            analysis['base_prediction'] = self.predictor.prediction_results[city_name]
        
        # Katılım senaryoları
        analysis['turnout_scenarios'] = self.analyze_turnout_scenarios(city_name)
        
        # Kararsız seçmen senaryoları
        analysis['undecided_scenarios'] = self.analyze_undecided_allocation(city_name)
        
        # Swing senaryoları
        analysis['swing_scenarios'] = self.calculate_swing_scenarios(city_name)
        
        # Risk değerlendirmesi
        analysis['risk_assessment'] = self._assess_election_risk(analysis)
        
        return analysis
    
    def _assess_election_risk(self, analysis: dict) -> dict:
        """Seçim risk değerlendirmesi"""
        
        risk_factors = {
            'volatility': 0,  # Sonuç değişkenliği
            'competitiveness': 0,  # Yarışın çekişmeli olması
            'polling_reliability': 0,  # Anket güvenilirliği
            'scenario_sensitivity': 0  # Senaryo değişikliklerine duyarlılık
        }
        
        if not analysis['base_prediction']:
            return risk_factors
        
        base_pred = analysis['base_prediction']
        
        # Volatility - En yüksek iki partinin farkı
        win_probs = list(base_pred['win_probabilities'].values())
        if len(win_probs) >= 2:
            win_probs_sorted = sorted(win_probs, reverse=True)
            margin = win_probs_sorted[0] - win_probs_sorted[1]
            risk_factors['volatility'] = max(0, 100 - margin) / 100
        
        # Competitiveness - Çekişme düzeyi
        max_win_prob = max(win_probs) if win_probs else 0
        if max_win_prob < 60:
            risk_factors['competitiveness'] = 1.0
        elif max_win_prob < 75:
            risk_factors['competitiveness'] = 0.6
        else:
            risk_factors['competitiveness'] = 0.2
        
        # Polling reliability - Anket sayısı
        poll_count = base_pred['poll_stats']['poll_count']
        if poll_count < 3:
            risk_factors['polling_reliability'] = 1.0
        elif poll_count < 8:
            risk_factors['polling_reliability'] = 0.5
        else:
            risk_factors['polling_reliability'] = 0.2
        
        # Scenario sensitivity - Senaryolara duyarlılık
        scenario_winners = set()
        
        # Turnout senaryolarından kazananlar
        for scenario in analysis['turnout_scenarios'].values():
            scenario_winners.add(scenario['winning_party'])
        
        # Swing senaryolarından kazananlar
        for scenario in analysis['swing_scenarios'].values():
            scenario_winners.add(scenario['winning_party'])
        
        # Kararsız seçmen senaryolarından kazananlar
        for scenario in analysis['undecided_scenarios'].values():
            scenario_winners.add(scenario['winning_party'])
        
        # Farklı kazanan sayısı ne kadar fazlaysa o kadar riskli
        unique_winners = len(scenario_winners)
        risk_factors['scenario_sensitivity'] = min(1.0, unique_winners / 4)
        
        # Genel risk skoru
        overall_risk = np.mean(list(risk_factors.values()))
        risk_factors['overall_risk'] = overall_risk
        
        # Risk seviyesi kategorisi
        if overall_risk < 0.3:
            risk_factors['risk_level'] = 'Düşük'
        elif overall_risk < 0.6:
            risk_factors['risk_level'] = 'Orta'
        else:
            risk_factors['risk_level'] = 'Yüksek'
        
        return risk_factors
    
    def generate_scenario_report(self, city_analyses: dict, output_dir: str = "outputs/") -> str:
        """Senaryo analizi raporu oluşturur"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(output_dir, f"senaryo_analizi_raporu_{timestamp}.txt")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("2024 YEREL SEÇİMLERİ SENARYO ANALİZİ RAPORU\n")
            f.write("Gelişmiş Risk Değerlendirmesi ve Öngörü Analizi\n")
            f.write("=" * 80 + "\n")
            f.write(f"Oluşturulma Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            
            # Risk seviyelerine göre iller
            high_risk_cities = []
            medium_risk_cities = []
            low_risk_cities = []
            
            for city, analysis in city_analyses.items():
                risk_level = analysis['risk_assessment'].get('risk_level', 'Bilinmiyor')
                if risk_level == 'Yüksek':
                    high_risk_cities.append(city)
                elif risk_level == 'Orta':
                    medium_risk_cities.append(city)
                else:
                    low_risk_cities.append(city)
            
            f.write("RİSK DEĞERLENDİRMESİ ÖZETİ\n")
            f.write("-" * 40 + "\n")
            f.write(f"🔴 Yüksek Risk ({len(high_risk_cities)} il): {', '.join(high_risk_cities)}\n")
            f.write(f"🟡 Orta Risk ({len(medium_risk_cities)} il): {', '.join(medium_risk_cities)}\n")
            f.write(f"🟢 Düşük Risk ({len(low_risk_cities)} il): {', '.join(low_risk_cities)}\n\n")
            
            # Detaylı analizler
            f.write("DETAYLI SENARYO ANALİZLERİ\n")
            f.write("=" * 80 + "\n\n")
            
            for city, analysis in sorted(city_analyses.items()):
                f.write(f"{city.upper()}\n")
                f.write("-" * len(city) + "\n")
                
                risk = analysis['risk_assessment']
                f.write(f"Risk Seviyesi: {risk.get('risk_level', 'Bilinmiyor')} ")
                f.write(f"(Skor: {risk.get('overall_risk', 0):.2f})\n")
                
                # En kritik risk faktörü
                risk_factors = {k: v for k, v in risk.items() 
                               if k not in ['overall_risk', 'risk_level']}
                if risk_factors:
                    max_risk_factor = max(risk_factors.items(), key=lambda x: x[1])
                    f.write(f"En Kritik Faktör: {max_risk_factor[0]} ({max_risk_factor[1]:.2f})\n")
                
                # Katılım senaryoları
                if analysis['turnout_scenarios']:
                    f.write("\nKatılım Senaryoları:\n")
                    for scenario_name, scenario in analysis['turnout_scenarios'].items():
                        turnout = scenario['turnout_rate']
                        winner = scenario['winning_party']
                        percentage = scenario['winning_percentage']
                        f.write(f"  Katılım %{turnout*100:.0f}: {winner} (%{percentage:.1f})\n")
                
                # En volatil partiler
                if analysis['swing_scenarios']:
                    party_effects = {}
                    for scenario_name, scenario in analysis['swing_scenarios'].items():
                        party = scenario['party']
                        if party not in party_effects:
                            party_effects[party] = []
                        party_effects[party].append(scenario['winning_party'])
                    
                    f.write("\nSwing Analizi:\n")
                    for party, effects in party_effects.items():
                        unique_winners = len(set(effects))
                        f.write(f"  {party}: {unique_winners} farklı sonuç - ")
                        if unique_winners > 3:
                            f.write("Yüksek volatilite\n")
                        elif unique_winners > 1:
                            f.write("Orta volatilite\n")
                        else:
                            f.write("Düşük volatilite\n")
                
                f.write("\n")
        
        print(f"📋 Senaryo analizi raporu oluşturuldu: {report_file}")
        return report_file
    
    def create_scenario_visualizations(self, city_analyses: dict, output_dir: str = "outputs/graphs/"):
        """Senaryo analizi görselleştirmeleri"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Risk haritası
        plt.figure(figsize=(16, 10))
        
        cities = []
        risk_scores = []
        risk_levels = []
        
        for city, analysis in city_analyses.items():
            cities.append(city)
            risk_scores.append(analysis['risk_assessment'].get('overall_risk', 0))
            risk_levels.append(analysis['risk_assessment'].get('risk_level', 'Bilinmiyor'))
        
        # Renk kodlaması
        color_map = {'Yüksek': 'red', 'Orta': 'orange', 'Düşük': 'green', 'Bilinmiyor': 'gray'}
        colors = [color_map[level] for level in risk_levels]
        
        # Horizontal bar chart
        y_pos = np.arange(len(cities))
        plt.barh(y_pos, risk_scores, color=colors, alpha=0.7)
        plt.yticks(y_pos, cities)
        plt.xlabel('Risk Skoru (0-1)')
        plt.title('İl Bazında Seçim Risk Analizi')
        plt.grid(axis='x', alpha=0.3)
        
        # Efsane
        legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.7, label=level) 
                          for level, color in color_map.items() if level in risk_levels]
        plt.legend(handles=legend_elements, loc='lower right')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'risk_analizi_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Risk faktörleri dağılımı
        plt.figure(figsize=(12, 8))
        
        all_risk_factors = {
            'volatility': [],
            'competitiveness': [],
            'polling_reliability': [],
            'scenario_sensitivity': []
        }
        
        for analysis in city_analyses.values():
            risk = analysis['risk_assessment']
            for factor in all_risk_factors.keys():
                all_risk_factors[factor].append(risk.get(factor, 0))
        
        # Box plot
        plt.boxplot(all_risk_factors.values(), labels=all_risk_factors.keys())
        plt.ylabel('Risk Skoru')
        plt.title('Risk Faktörleri Dağılımı')
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'risk_faktorleri_{timestamp}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Senaryo analizi görselleri oluşturuldu: {output_dir}")

def main():
    """Ana çalıştırma fonksiyonu"""
    print("🎯 Gelişmiş Senaryo Analizi ve Risk Değerlendirmesi")
    print("=" * 60)
    
    # Önceki tahmin sonuçlarını yükle
    predictor = AdvancedElectionPredictor()
    predictor.load_city_data()
    
    if not predictor.city_data:
        print("❌ Veri yüklenemedi!")
        return
    
    # Basit tahminleri çalıştır (sonuçlar zaten var ise atlayabilir)
    if not predictor.prediction_results:
        print("📊 Temel tahminler hesaplanıyor...")
        predictor.predict_all_cities(n_simulations=10000)  # Hızlı analiz için az simülasyon
    
    # Senaryo analizcisini başlat
    analyzer = ElectionScenarioAnalyzer(predictor)
    
    # Kritik illeri seç (yüksek oy potansiyeli olan)
    critical_cities = ['İstanbul', 'Ankara', 'İzmir', 'Antalya', 'Bursa', 'Adana', 'Konya', 'Gaziantep', 'Şanlıurfa', 'Hatay']
    
    # Mevcut illeri filtrele
    available_critical_cities = [city for city in critical_cities if city in predictor.city_data]
    
    print(f"\n🔍 {len(available_critical_cities)} kritik il için detaylı senaryo analizi...")
    
    city_analyses = {}
    for city in available_critical_cities:
        analysis = analyzer.comprehensive_city_analysis(city)
        city_analyses[city] = analysis
    
    # Raporları oluştur
    print("\n📋 Senaryo raporları oluşturuluyor...")
    analyzer.generate_scenario_report(city_analyses)
    
    print("📊 Senaryo görselleştirmeleri oluşturuluyor...")
    analyzer.create_scenario_visualizations(city_analyses)
    
    print("\n✅ Senaryo analizi tamamlandı!")

if __name__ == "__main__":
    main()
