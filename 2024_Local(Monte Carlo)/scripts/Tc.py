import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

def load_survey_data(city_name):
    """CSV dosyasından anket verilerini yükler"""
    file_path = f"../data/raw_data/{city_name.lower()}_2024_anketler.csv"
    # CSV dosyasını oku, ilk satırı atlayarak (comment satırını)
    df = pd.read_csv(file_path, skiprows=1)
    # Boş değerleri 0 ile doldur
    df = df.fillna(0)
    return df

def calculate_city_stats(folder_path="../data/raw_data"):
    """Tüm şehirlerin anket verilerini yükler ve istatistikleri hesaplar"""
    city_stats = {}
    
    # CSV dosyalarını bul
    csv_files = glob.glob(os.path.join(folder_path, "*_2024_anketler.csv"))
    
    for file_path in csv_files:
        # Dosya adından şehir adını al
        city_name = os.path.basename(file_path).split('_')[0].capitalize()
        
        try:
            # Anket verilerini yükle - ilk satırı atlayarak
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # İlk satır yorum satırı ise atla
            if lines[0].strip().startswith('//'):
                data = ''.join(lines[1:])
            else:
                data = ''.join(lines)
            
            # String veriden dataframe oluştur
            df = pd.read_csv(pd.io.common.StringIO(data))
            df = df.fillna(0) # Boş değerleri 0 ile doldur
            
            # Her parti için anket ortalama ve standart sapma hesapla
            ortalama_oy_oranlari = df.mean()
            oy_orani_degiskenligi = df.std()
            
            # Şehir istatistiklerini kaydet
            city_stats[city_name] = pd.DataFrame({
                'ortalama_oy': ortalama_oy_oranlari,  # Partinin beklenen oy oranı (%)
                'degiskenlik': oy_orani_degiskenligi  # Oy oranındaki belirsizlik/dalgalanma (standart sapma)
            })
            
            print(f"{city_name} verileri başarıyla yüklendi.")
        except Exception as e:
            print(f"{city_name} verileri yüklenirken hata: {str(e)}")
    
    return city_stats

def monte_carlo_secim_simulasyonu(city_stats, n_simulations=10000):
    # Tüm partilerin birleşik listesi
    all_parties = set()
    for stats in city_stats.values():
        all_parties.update(stats.index)
    all_parties = sorted(list(all_parties))

    # Parti başına simülasyon sonuçlarını tut
    results = {party: [] for party in all_parties}

    for _ in range(n_simulations):
        sim_total = {party: 0 for party in all_parties}
        
        for city, stats in city_stats.items():
            for party in stats.index:
                # Ortalama oy oranı (beklenen değer)
                ortalama = stats.loc[party, 'ortalama_oy']
                # Oy oranı değişkenliği (seçim belirsizliği)
                degiskenlik = stats.loc[party, 'degiskenlik']
                # Normal dağılımdan örnek al (muhtemel oy oranı)
                sampled_vote = np.random.normal(loc=ortalama, scale=degiskenlik)
                sampled_vote = max(0, sampled_vote)  # negatif oy olmasın
                sim_total[party] += sampled_vote
        
        # Yüzdelik normalize et (tüm partiler %100 olacak şekilde)
        total_votes = sum(sim_total.values())
        for party in sim_total:
            results[party].append(sim_total[party] / total_votes * 100)

    return pd.DataFrame(results)


def kazanan_istatistikleri(simulasyon_df):
    winners = simulasyon_df.idxmax(axis=1)
    return winners.value_counts(normalize=True) * 100  # yüzdelik

if __name__ == "__main__":
    # Şehir istatistiklerini hesapla
    city_stats = calculate_city_stats()
    
    if not city_stats:
        print("Hiç veri yüklenemedi. Lütfen CSV dosyalarının doğru konumda olduğunu kontrol edin.")
    else:
        # Her şehir için hesaplanan istatistikleri yazdır
        for city, stats in city_stats.items():
            print(f"\n{city} İstatistikleri:")
            print(stats)
        
        # Monte Carlo simülasyonunu çalıştır
        print("\nMonte Carlo simülasyonu çalıştırılıyor...")
        simulasyon_df = monte_carlo_secim_simulasyonu(city_stats, 10000)
        
        # Genel sonuçları yazdır
        print("\nGenel Sonuçlar:")
        print("Ortalama: Simülasyonlardaki ortalama oy oranı")
        print("Std: Simülasyonlardaki oy oranı değişkenliği (standart sapma)")
        print(simulasyon_df.describe().T[['mean', 'std']])
        
        # Kazanan istatistiklerini hesapla ve yazdır
        winner_stats = kazanan_istatistikleri(simulasyon_df)
        print("\nPartilerin Kazanma Olasılıkları:")
        print(winner_stats)
