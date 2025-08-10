# 🗳️ Gelişmiş Monte Carlo Seçim Tahmin Sistemi

## 2024 Türkiye Yerel Seçimleri için Kapsamlı Analiz Platformu

Bu proje, 2024 Türkiye yerel seçimleri için gelişmiş Monte Carlo simülasyon tekniklerini kullanarak kapsamlı seçim tahmin analizi yapan bir sistemdir.

## 🎯 Sistem Özellikleri

### 📊 Ana Analiz Motoru (`advanced_election_predictor.py`)
- **50,000 iterasyon/il** Monte Carlo simülasyonu
- **Çoklu belirsizlik faktörleri:**
  - Anket hatası (±3%)
  - Örnekleme yanlılığı (±2.5%)
  - Kararsız seçmen dağılımı (±8%)
  - Son dakika değişimi (±2%)
  - Katılım değişkenliği (±5%)
- **Ağırlıklı anket analizi:** Zaman, örneklem büyüklüğü ve şirket güvenilirliği
- **Beta dağılımı kullanımı:** 0-100 arası sınırlı oy oranları
- **Güven aralıkları:** %80, %90, %95 güven seviyelerinde

### 🔍 Senaryo Analizi (`scenario_analyzer.py`)
- **Katılım senaryoları:** %60, %70, %80, %85 katılım oranları
- **Kararsız seçmen dağılımı:** 4 farklı siyasi senaryo
- **Swing analizi:** ±2%, ±5%, ±8% son dakika değişimleri
- **Risk değerlendirmesi:** Volatilite, çekişme, güvenilirlik skorları

### 📈 Dashboard ve Raporlama (`dashboard.py`)
- **Yönetici özet raporları**
- **Ulusal genel bakış görselleri**
- **Çekişmeli yarış analizleri**
- **Risk haritaları**
- **Parti performans tabloları**

## 🏆 Analiz Sonuçları

### Parti Bazında Projeksiyonlar
1. **AKP**: 8 il (%15.7) - Güçlü performans
2. **HDP**: 7 il (%13.7) - Önemli varlık
3. **YRP**: 6 il (%11.8) - Yükseliş trendi
4. **DEM**: 5 il (%9.8) - Bölgesel güç
5. **CHP**: 2 il (%3.9) - Sınırlı başarı
6. **ZP**: 1 il (%2.0) - Yerel odaklar
7. **İYİ**: 1 il (%2.0) - Seçici başarı

### 📊 Kritik İstatistikler
- **Toplam analiz edilen il:** 51
- **Çekişmeli yarış:** 16 il (%31.4)
- **Güvenli sonuç:** 35 il (%68.6)
- **Yetersiz anket verisi:** 18 il
- **Yüksek belirsizlik:** 10 il

### ⚡ En Çekişmeli İller
1. **Isparta** - HDP %46.9 (fark: %0.6)
2. **Bilecik** - YRP %51.4 (fark: %2.9)
3. **Giresun** - AKP %48.0 (fark: %3.2)
4. **Niğde** - YRP %42.7 (fark: %12.1)
5. **Tekirdağ** - AKP %47.0 (fark: %12.2)

## 🔧 Teknik Özellikler

### Kullanılan Teknolojiler
- **Python 3.12+**
- **NumPy** - Numerik hesaplamalar
- **Pandas** - Veri işleme
- **Matplotlib/Seaborn** - Görselleştirme
- **SciPy** - İstatistiksel dağılımlar

### Veri Kaynakları
- Wikipedia anket verileri
- 51 il için toplamda 1,000+ anket
- Mart 2024'e kadar güncel veriler

### Kalite Kontrolleri
- ✅ Otomatik veri temizleme
- ✅ Anormal değer filtreleme
- ✅ Eksik veri tamamlama
- ✅ Normalleştirme algoritmaları
- ✅ Çapraz doğrulama

## 📁 Dosya Yapısı

```
2024_Local(Monte Carlo)/
├── advanced_election_predictor.py    # Ana tahmin motoru
├── scenario_analyzer.py              # Senaryo analizi
├── dashboard.py                       # Dashboard ve raporlama
├── data/                             # Veri dosyaları
│   ├── processed_data/iller/         # İl bazında temiz veri
│   └── raw_data/                     # Ham anket verileri
└── outputs/                          # Sonuç dosyaları
    ├── data/                         # JSON sonuçlar
    ├── graphs/                       # Görsel analizler
    └── reports/                      # Metin raporları
```

## 🚀 Kullanım

### 1. Temel Analiz
```bash
python advanced_election_predictor.py
```

### 2. Senaryo Analizi
```bash
python scenario_analyzer.py
```

### 3. Dashboard Raporu
```bash
python dashboard.py
```

## 📊 Çıktı Dosyaları

### Raporlar
- **Detaylı tahmin raporu** - Her il için kapsamlı analiz
- **Senaryo analizi raporu** - Risk değerlendirmesi
- **Yönetici özet raporu** - Üst düzey bulgular

### Görseller
- **Ulusal genel bakış** - Parti dağılımı
- **Kazanma olasılıkları** - İl bazında harita
- **Risk analizi** - Belirsizlik göstergeleri
- **Çekişmeli iller tablosu** - Detaylı karşılaştırma

### Veri
- **JSON sonuçları** - Programatik erişim için
- **Güven aralıkları** - İstatistiksel kesinlik
- **Senaryo sonuçları** - Alternatif durumlar

## ⚠️ Önemli Notlar

### Metodolojik Sınırlamalar
- Anket verisi kalitesine bağımlılık
- Geçmiş seçim verilerinin sınırlı kullanımı
- Siyasi gelişmelerin öngörülememesi
- Bölgesel farklılıkların genelleştirilmesi

### Güvenilirlik Faktörleri
- **Yüksek güvenilirlik:** 10+ anket olan iller
- **Orta güvenilirlik:** 5-9 anket olan iller
- **Düşük güvenilirlik:** <5 anket olan iller

### Risk Uyarıları
- Son dakika gelişmeler sonuçları değiştirebilir
- Katılım oranı kritik faktör
- Kararsız seçmen oranı %15+ varsayılmıştır
- Yerel dinamikler tam yansıtılamayabilir

## 📈 Gelecek Geliştirmeler

### Planlanan Özellikler
- **Gerçek zamanlı veri entegrasyonu**
- **Sosyal medya sentiment analizi**
- **Ekonomik gösterge korelasyonu**
- **Mobil dashboard uygulaması**
- **API entegrasyonu**

### Metodolojik İyileştirmeler
- **Ensemble modelleri**
- **Makine öğrenmesi algoritmaları**
- **Zaman serisi analizi**
- **Bayesian güncelleme**

## 🤝 Katkıda Bulunma

Bu akademik proje açık kaynak ruhuyla geliştirilmiştir. Katkılarınız memnuniyetle karşılanır:

1. **Veri kalitesi iyileştirmeleri**
2. **Algoritma optimizasyonları**
3. **Görselleştirme geliştirmeleri**
4. **Dokümantasyon güncellemeleri**

## 📄 Lisans

Bu proje akademik amaçlarla MIT lisansı altında paylaşılmıştır.

## ⚖️ Yasal Uyarı

Bu analiz akademik araştırma amaçlıdır. Sonuçlar kesin tahmin niteliği taşımaz ve gerçek seçim sonuçları farklılık gösterebilir. Siyasi karar alma süreçlerinde yalnızca referans amaçlı kullanılmalıdır.

---

## 📞 İletişim

Proje hakkında sorularınız için GitHub Issues bölümünü kullanabilirsiniz.

**Son güncelleme:** 10 Ağustos 2025
**Versiyon:** 1.0
**Analiz kapsamı:** 51 il, 50,000 simülasyon/il
