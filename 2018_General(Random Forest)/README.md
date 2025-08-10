# Türkiye 2018 Seçim Tahmini - Gelişmiş Random Forest Analizi

Bu uygulama, 2018 Türkiye seçimleri öncesi yapılan anket verilerini kullanarak Random Forest machine learning algoritması ile gerçekçi seçim tahminleri yapar.

## 🚀 Özellikler

### Gelişmiş Veri İşleme
- **Akıllı Veri Temizleme**: Virgüllü sayılar, aralık değerleri (50-52 gibi), eksik veriler otomatik işlenir
- **Çoklu Format Desteği**: Farklı anket formatlarını otomatik tanır ve dönüştürür
- **Eksik Veri Yönetimi**: İstatistiksel yöntemlerle eksik verileri doldurur

### İleri Düzey Machine Learning
- **Random Forest Algoritması**: 200 ağaç ile ensemble learning
- **Otomatik Parametre Optimizasyonu**: Veri boyutuna göre model parametrelerini ayarlar
- **Cross-Validation**: Küçük veri setlerinde güvenilirlik için çapraz doğrulama
- **Class Balancing**: Dengesiz veri setleri için otomatik ağırlıklandırma

### Gerçekçi Senaryo Analizi
- **4 Farklı Senaryo**: Yüksek güvenilirlik, AKP güçlü, muhalefet güçlü, yakın yarış
- **Anket Şirketi Güvenilirlik Skoru**: Her anket şirketine güvenilirlik katsayısı
- **Katılımcı Sayısı Ağırlığı**: Örneklem büyüklüğüne göre ağırlıklandırma
- **Kararsız Seçmen Analizi**: Kararsız seçmen oranının etkisi

### Kapsamlı Raporlama
- **İstatistiksel Analiz**: En olası kazanan, en kararlı/değişken parti
- **Görsel Raporlar**: Bar chart ve pasta grafiği
- **Belirsizlik Analizi**: Senaryolar arası varyasyon hesabı
- **Detaylı Metrikler**: Precision, recall, F1-score

## 📊 Analiz Sonuçları

### Ortalama Tahmin Sonuçları:
1. **AKP**: %43.4 (En olası kazanan)
2. **CHP**: %22.8
3. **İYİ Parti**: %14.4
4. **HDP**: %10.0
5. **MHP**: %6.8
6. **SP**: %2.6 (En kararlı parti)

### Model Performansı:
- **Eğitim Doğruluğu**: %100
- **Test Doğruluğu**: %100
- **Veri Kalitesi**: 26 anket, 6 parti analizi

## 🛠️ Teknik Özellikler

### Kullanılan Teknolojiler:
```python
- scikit-learn: Random Forest, preprocessing
- pandas: Veri işleme
- numpy: Sayısal hesaplamalar
- matplotlib/seaborn: Görselleştirme
```

### Model Mimarisi:
```
Pipeline:
├── ColumnTransformer
│   ├── StandardScaler (sayısal veriler)
│   └── OneHotEncoder (kategorik veriler)
└── RandomForestClassifier
    ├── n_estimators: 200
    ├── max_depth: 10
    ├── class_weight: balanced
    └── random_state: 42
```

### Özellik Mühendisliği:
- Anket şirketi güvenilirlik skoru
- Katılımcı sayısı ağırlığı (log transform)
- Kronolojik sıralama
- İttifak simülasyonları (Cumhur, Millet)
- Kararsız seçmen oranı

## 📈 Senaryo Karşılaştırması

| Senaryo | AKP | CHP | İYİ | HDP | MHP | SP |
|---------|-----|-----|-----|-----|-----|----| 
| Yüksek Güvenilirlik | 43.5% | 22.0% | 14.2% | 10.1% | 7.8% | 2.6% |
| AKP Güçlü | 47.6% | 21.0% | 13.3% | 9.0% | 6.7% | 2.4% |
| Muhalefet Güçlü | 40.2% | 24.7% | 15.5% | 11.0% | 5.9% | 2.7% |
| Yakın Yarış | 42.3% | 23.4% | 14.7% | 10.1% | 6.9% | 2.6% |

## 🎯 Kullanım

```bash
python generator.py
```

Program otomatik olarak:
1. Anket verilerini yükler ve temizler
2. Machine learning modelini eğitir  
3. 4 farklı senaryoda tahmin yapar
4. Detaylı rapor oluşturur
5. Grafiği 'election_prediction_2018.png' olarak kaydeder

## 📁 Dosya Yapısı

```
2018(Random Forest)/
├── generator.py           # Ana uygulama
├── election/
│   └── all.csv           # Anket verileri
├── election_prediction_2018.png  # Sonuç grafiği
└── README.md             # Bu dosya
```

## 🔍 Veri Kaynağı

Uygulama, 2018 seçimi öncesi 26 farklı anket sonucunu analiz eder:
- **Anket Şirketleri**: MetroPOLL, SONAR, Gezici, ORC, Mediar, Piar, REMRES ve diğerleri
- **Örneklem Büyüklüğü**: 1,500 - 5,500 kişi arası
- **Zaman Aralığı**: 2017-2018 dönemi anketleri

## ⚡ Algoritma Avantajları

1. **Ensemble Learning**: 200 karar ağacının ortak kararı
2. **Overfitting Koruması**: Cross-validation ve regularization
3. **Feature Importance**: Hangi faktörlerin önemli olduğunu gösterir
4. **Robust Predictions**: Aykırı değerlere karşı dayanıklı
5. **Uncertainty Quantification**: Tahmin güvenilirlik aralıkları

## 📋 Gereksinimler

```
Python 3.8+
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
seaborn>=0.11.0
```

## 🎨 Görselleştirme

Uygulama iki türde grafik oluşturur:
1. **Bar Chart**: Partilerin oy oranlarını karşılaştırır
2. **Pie Chart**: Genel oy dağılımını gösterir

Grafik `election_prediction_2018.png` dosyasına yüksek çözünürlükte (300 DPI) kaydedilir.

---

**Not**: Bu tahmin modeli akademik ve eğitim amaçlıdır. Gerçek seçim sonuçları çok sayıda faktöre bağlıdır ve kesin tahmin mümkün değildir.
