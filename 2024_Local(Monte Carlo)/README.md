# 2024 Türkiye Yerel Seçimleri Anket Verisi Temizleyici

Bu proje, 2024 Türkiye yerel seçimleri için yapılan anket verilerini Wikipedia'dan çekerek temizleyen ve analiz eden bir araçtır.

## 📁 Klasör Yapısı

```
2024_Local(Monte Carlo)/
├── scripts/                       # Python scriptleri
│   ├── anket_veri_düzenleyici.py  # Ana temizlik scripti
│   ├── wikipedia_anket_scriper.py # Wikipedia'dan veri çekme scripti
│   └── Tc.py                      # Monte Carlo simülasyon scripti
├── data/                          # Veri dosyaları
│   ├── raw_data/                  # Ham anket verileri
│   └── processed_data/            # Temizlenmiş veriler
│       ├── iller/                 # İl bazında temizlenmiş veriler
│       ├── birlesik_veriler/      # Tüm illerin birleşik verisi
│       └── raporlar/              # Analiz raporları
└── README.md                      # Bu dosya
```

## 🚀 Kullanım

### 1. Veri Temizleme
```bash
python scripts/anket_veri_düzenleyici.py
```

Bu script:
- `data/raw_data/` klasöründeki ham verileri okur
- Gereksiz sütunları ve satırları temizler
- Parti sütunlarını otomatik tanımlar
- Temizlenmiş verileri düzenli klasörlere kaydeder
- Kapsamlı analiz raporları oluşturur

### 2. Wikipedia'dan Veri Çekme (İsteğe bağlı)
```bash
python scripts/wikipedia_anket_scriper.py
```

### 3. Monte Carlo Simülasyonu
```bash
python scripts/Tc.py
```

## 📊 Çıktı Dosyaları

### İller Klasörü (`data/processed_data/iller/`)
- Her il için ayrı CSV dosyası
- Standart sütun yapısı: İl, Kaynak_URL, Tarih, Anket_Şirketi, Örneklem, AKP, CHP, İYİ, MHP, HDP, DEM, YRP, ZP
- Temizlenmiş ve sayısal formatta parti verileri

### Birleşik Veriler (`data/processed_data/birlesik_veriler/`)
- `tum_iller_anket_verileri.csv`: Tüm illerin birleşik verisi
- Toplu analiz ve makine öğrenmesi için uygun format

### Raporlar (`data/processed_data/raporlar/`)
- Detaylı analiz raporları
- İstatistiksel özetler
- Parti trendleri ve karşılaştırmalar

## 🔧 Özellikler

- **Otomatik Veri Temizleme**: Ham anket verilerini otomatik olarak temizler
- **Standardizasyon**: Tüm veri formatlarını standart hale getirir
- **Monte Carlo Simülasyonu**: Seçim sonuçlarını olasılıksal olarak tahmin eder
- **Kapsamlı Raporlama**: Detaylı analiz ve görselleştirme
- **Modüler Yapı**: Her script bağımsız çalışabilir

## 📋 Gereksinimler

```bash
pip install pandas numpy matplotlib requests beautifulsoup4 lxml
```

## 🎯 Kullanım Adımları

1. Wikipedia'dan veri çekme (isteğe bağlı):
   ```bash
   cd scripts
   python wikipedia_anket_scriper.py
   ```

2. Verileri temizleme ve düzenleme:
   ```bash
   cd scripts
   python anket_veri_düzenleyici.py
   ```

3. Monte Carlo simülasyonu çalıştırma:
   ```bash
   cd scripts
   python Tc.py
   ```

## � Teknik Özellikler

### Veri Temizleme
- Çok seviyeli sütun başlıklarını düzleştirme
- Gereksiz sütunları otomatik kaldırma
- Parti sütunlarını akıllı tanıma
- Sayısal verileri optimize etme
- Boş ve tekrar eden satırları temizleme

### Analiz Yetenekleri
- İl bazında detaylı istatistikler
- Parti trendleri analizi
- Monte Carlo simülasyonu ile tahmin
- Görselleştirme ve raporlama

## 📄 Lisans

Bu proje MIT lisansı altında yayınlanmıştır.
- İl bazında anket sayısı analizi
- Parti dağılım analizi
- İşlem kayıtları ve hata raporları
- CSV ve TXT formatında çıktılar

## 📋 Veri Formatı

### Giriş Formatı (Ham Veri)
```csv
Bölüm,KaynakURL,Tarih Tarih,Anket şirketi Anket şirketi,Örneklem Örneklem,CHP Unnamed: 3_level_1,AKP Unnamed: 4_level_1,...
```

### Çıkış Formatı (Temizlenmiş Veri)
```csv
İl,Kaynak_URL,Tarih,Anket_Şirketi,Örneklem,AKP,CHP,İYİ,MHP,HDP,DEM,YRP,ZP
Ankara,https://...,29 Mart,BETİMAR,3.06,612.0,289.0,14.0,39.0,24.0,14.0,8,323
```

## 🛠️ Gereksinimler

```python
pandas >= 1.0.0
numpy >= 1.18.0
pathlib (Python 3.4+ ile birlikte gelir)
```

## 📝 Notlar

- Script otomatik olarak eski temizlik dosyalarını kaldırır
- Hata durumlarında log mesajları oluşturur
- Büyük dosyaları işlerken bellek kullanımını optimize eder
- UTF-8 encoding ile Türkçe karakterleri destekler

## 🔄 Güncelleme Geçmişi

- **v1.0**: İlk sürüm - Temel veri temizleme
- **v2.0**: Gelişmiş parti tanıma algoritması
- **v3.0**: Birleşik script ve temiz klasör yapısı (Mevcut)

---

**Geliştiren**: Anket Veri Temizleyici v3.0  
**Son Güncelleme**: Ağustos 2025
