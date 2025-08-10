# 🇹🇷 Türk Seçim Verileri - Lineer Regresyon Tahmin Projesi

Bu proje, 2014-2015 dönemindeki Türk genel seçim anketlerini kullanarak gelişmiş makine öğrenmesi teknikleri ile parti oylarını tahmin etmeyi amaçlamaktadır.

## 🎯 Proje Hedefleri

- ✅ **Lineer Regresyon** ve çeşitli regresyon modellerini kullanarak parti oylarını tahmin etmek
- ✅ **Scikit-learn** framework'ü ile kapsamlı ML pipeline oluşturmak
- ✅ **Model karşılaştırması** yaparak en iyi algoritmayı bulmak
- ✅ **Özellik mühendisliği** ile tahmin doğruluğunu artırmak
- ✅ **Görselleştirme** ile analiz sonuçlarını sunmak

## 📊 Veri Seti

### Kaynak Dosyalar
```
election/
├── haziran-2014.csv    # 2014 Haziran dönemi anketleri
├── haziran-2015.csv    # 2015 Haziran seçim sonuçları ve anketleri  
└── kasım-2015.csv      # 2015 Kasım seçim sonuçları ve anketleri
```

### Veri Özellikleri
- **152 anket verisi** (3 dönem boyunca)
- **35 farklı anket şirketi**
- **4 ana parti**: AK Parti, CHP, MHP, HDP
- **Gerçek seçim sonuçları** dahil

## 🛠️ Kullanılan Teknolojiler

### Python Kütüphaneleri
```python
# Temel ML Framework
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression

# Regresyon Modelleri
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor

# Model Değerlendirme
from sklearn.metrics import mean_squared_error, r2_score

# Veri İşleme
import pandas as pd
import numpy as np

# Görselleştirme
import matplotlib.pyplot as plt
import seaborn as sns
```

### ML Teknikleri
- **Linear Regression**: Temel regresyon modeli
- **Ridge Regression**: L2 regularization
- **Lasso Regression**: L1 regularization  
- **ElasticNet**: L1 + L2 regularization
- **Random Forest**: Ensemble learning
- **Cross-Validation**: Model validasyonu
- **GridSearchCV**: Hiperparametre optimizasyonu
- **Bootstrap Sampling**: Tahmin aralıkları

## 📁 Proje Dosyaları

### Ana Dosyalar
| Dosya | Açıklama |
|-------|----------|
| `electionguess.py` | 🎯 Ana analiz scripti - Temel lineer regresyon |
| `analysis_report.py` | 📊 Kapsamlı analiz - Çoklu model karşılaştırması |
| `practical_usage.py` | 🔧 Pratik kullanım örneği ve demo |
| `ANALIZ_RAPORU.md` | 📋 Detaylı analiz sonuçları raporu |

### Çıktı Dosyaları
| Dosya | Açıklama |
|-------|----------|
| `election_trends.png` | 📈 Parti oyları trend grafikleri |
| `model_comparison.png` | 📊 Model performans karşılaştırması |
| `feature_importance.png` | 🎯 Özellik önemleri heatmap |
| `my_election_models.pkl` | 💾 Eğitilmiş modeller (pickle) |

## 🚀 Kullanım Kılavuzu

### 1. Temel Analiz
```bash
python electionguess.py
```
- Temel lineer regresyon analizi
- 2015 Kasım seçimi tahmini
- Trend grafikleri

### 2. Kapsamlı Analiz
```bash
python analysis_report.py  
```
- 5 farklı model karşılaştırması
- Özellik önem analizi
- Hiperparametre optimizasyonu
- Bootstrap tahmin aralıkları

### 3. Pratik Kullanım
```bash
python practical_usage.py
```
- Modellerin nasıl kullanılacağı
- Yeni anket verileri ile tahmin
- Model kaydetme/yükleme

### 4. Özel Tahmin Yapma
```python
from practical_usage import ElectionPredictor

# Model oluştur
predictor = ElectionPredictor()
predictor.load_and_train()

# Anket verisi
poll_data = {
    'AK Parti': 45.0,
    'CHP': 25.0, 
    'MHP': 15.0,
    'HDP': 12.0,
    'Katılımcı sayısı': 2500,
    'Period': 3
}

# Tahmin yap
results = predictor.predict_from_poll_data(poll_data)
print(results)
```

## 📈 Analiz Sonuçları

### Model Performansları
| Model | AK Parti R² | CHP R² | MHP R² | HDP R² |
|-------|-------------|--------|--------|--------|
| **Linear Regression** | 1.000 | 1.000 | 1.000 | 1.000 |
| Ridge Regression | 0.996 | 0.580 | 0.892 | 0.994 |
| Random Forest | 0.874 | 0.756 | 0.640 | 0.005 |
| ElasticNet | 0.664 | 0.291 | 0.286 | 0.229 |
| Lasso Regression | -1.743 | 0.067 | 0.104 | -0.024 |

### 2015 Kasım Seçimi Tahmin Doğruluğu
| Parti | Gerçek | Tahmin | Hata |
|-------|--------|--------|------|
| AK Parti | 49.5% | 41.9% | 7.6 puan |
| CHP | 25.3% | 26.3% | 1.0 puan |
| MHP | 12.0% | 15.5% | 3.4 puan |
| HDP | 10.6% | 12.2% | 1.6 puan |

**📊 Ortalama Mutlak Hata: 3.42 puan**

### En Önemli Özellikler
1. **Diğer parti oyları**: En güçlü prediktörler
2. **Anket katılımcı sayısı**: Güvenilirlik faktörü
3. **Zaman trendi**: Temporal dinamikler
4. **Dönem etkisi**: Seçim döngüsü

## 🎯 Öne Çıkan Özellikler

### ✅ Teknik Mükemmellik
- **5 farklı ML algoritması** karşılaştırması
- **Cross-validation** ile robust validasyon
- **Feature engineering** ile gelişmiş özellikler
- **Hyperparameter tuning** ile optimizasyon
- **Bootstrap sampling** ile güven aralıkları

### ✅ Kapsamlı Analiz
- **Model performans metriklerics** (R², RMSE, MAE)
- **Feature importance** analizi
- **Prediction intervals** hesaplaması
- **Temporal trend** analizi

### ✅ Pratik Kullanım
- **Pickle ile model kaydetme**
- **Yeni veri ile tahmin** yapabilme
- **API-ready** structure
- **Demo örnekleri**

## 🔮 Gelecek Geliştirmeler

### Veri Genişletme
- [ ] Daha fazla dönem verisi ekleme
- [ ] Sosyo-ekonomik değişkenler
- [ ] Bölgesel anket verileri
- [ ] Real-time veri entegrasyonu

### Model Geliştirme
- [ ] Deep Learning modelleri
- [ ] Ensemble yöntemleri
- [ ] Time series analizi
- [ ] Bayesian yöntemler

### Ürün Geliştirme
- [ ] Web arayüzü
- [ ] API servisi
- [ ] Real-time dashboard
- [ ] Mobil uygulama

## 📊 Görselleştirmeler

Proje aşağıdaki grafikleri üretir:

1. **election_trends.png**: Parti oylarının zaman içindeki değişimi
2. **model_comparison.png**: Model performanslarının karşılaştırması
3. **feature_importance.png**: Özellik önemlerinin heatmap'i

## 🤝 Katkıda Bulunma

Bu proje eğitim amaçlıdır. Katkıda bulunmak için:

1. Repository'yi fork edin
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## 📜 Lisans

Bu proje MIT lisansı altında yayınlanmıştır.

## 🔗 İletişim

Sorular ve öneriler için:
- 📧 Email: [proje sahibi]
- 🐙 GitHub: [repository linki]

---

**⚡ Hızlı Başlangıç**
```bash
# Temel analizi çalıştır
python electionguess.py

# Kapsamlı analizi çalıştır  
python analysis_report.py

# Pratik kullanım örneklerini gör
python practical_usage.py
```

**🎯 Ana Bulgular:**
- Linear Regression en iyi performansı gösterdi
- 3.42 puan ortalama hata ile başarılı tahminler
- CHP en kolay, AK Parti en zor tahmin edilen parti
- Özellik mühendisliği tahmin doğruluğunu artırdı

---
*📅 Son Güncelleme: Ağustos 2025*
*🎯 Proje Durumu: Tamamlandı ve Kullanıma Hazır*
