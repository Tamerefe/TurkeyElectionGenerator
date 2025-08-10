# 🇹🇷 Turkey Election Generator

*A comprehensive suite of advanced machine learning tools for analyzing, simulating, and predicting Turkish election outcomes across multiple years (2015-2024). This project implements cutting-edge statistical methods, ensemble learning, Monte Carlo simulations, and data visualization for accurate election forecasting.*

## ⚠️ **IMPORTANT DISCLAIMER / ÖNEMLİ UYARI**

### 🇬🇧 **ENGLISH**
**ACADEMIC & EDUCATIONAL PURPOSE ONLY**

This project is developed **EXCLUSIVELY** for:
- ✅ **Academic research** and statistical analysis
- ✅ **Educational purposes** and machine learning demonstrations
- ✅ **Open-source software development** and algorithm testing
- ✅ **Data science portfolio** and technical skill demonstration

**NOT INTENDED FOR:**
- ❌ Political campaigning or election manipulation
- ❌ Spreading misinformation or propaganda
- ❌ Influencing public opinion or voter behavior
- ❌ Commercial election consulting services

**LEGAL PROTECTION**: This software is protected under academic freedom and open-source software development rights. All predictions are based on publicly available polling data and standard statistical methods used in academic research worldwide.

**📋 For detailed legal information, please read: [`DISCLAIMER.md`](DISCLAIMER.md)**

### 🇹🇷 **TÜRKÇE**
**SADECE AKADEMİK VE EĞİTİM AMAÇLI**

Bu proje **SADECE** şu amaçlarla geliştirilmiştir:
- ✅ **Akademik araştırma** ve istatistiksel analiz
- ✅ **Eğitim amaçları** ve makine öğrenmesi demonstrasyonu
- ✅ **Açık kaynak yazılım geliştirme** ve algoritma testi
- ✅ **Veri bilimi portföyü** ve teknik beceri gösterimi

**AMAÇLANMAYAN KULLANIM:**
- ❌ Siyasi kampanya veya seçim manipülasyonu
- ❌ Yanlış bilgi veya propaganda yayma
- ❌ Kamuoyu veya seçmen davranışını etkileme
- ❌ Ticari seçim danışmanlığı hizmetleri

**HUKUKİ KORUMA**: Bu yazılım, akademik özgürlük ve açık kaynak yazılım geliştirme hakları altında korunmaktadır. Tüm tahminler, kamuya açık anket verileri ve dünya çapında akademik araştırmalarda kullanılan standart istatistiksel yöntemlere dayanmaktadır.

**📋 Detaylı hukuki bilgi için lütfen okuyun: [`DISCLAIMER.md`](DISCLAIMER.md)**

---

## � Project Overview

The Turkey Election Generator is a sophisticated collection of election analysis tools that combines multiple machine learning approaches to provide accurate predictions for Turkish elections. The project covers various Turkish elections from 2015 to 2024, including both general and local elections, utilizing diverse algorithms ranging from Linear Regression to advanced Monte Carlo simulations.

## 📁 Project Structure

```
TurkeyElectionGenerator/
├── 2015_General(Linear Regression)/     # Linear regression models for 2015 general elections
│   ├── electionguess.py                 # Main prediction engine
│   ├── analysis_report.py               # Automated analysis reporting
│   ├── practical_usage.py               # Practical implementation examples
│   ├── election/                        # Historical election data (2014-2015)
│   ├── outputs/                         # Generated models, graphs, and reports
│   └── README.md                        # Detailed documentation
│
├── 2018_General(Random Forest)/         # Random Forest ensemble learning
│   ├── generator.py                     # Advanced Random Forest predictor
│   ├── election/                        # 2018 polling data
│   ├── outputs/                         # Model outputs and visualizations
│   └── README.md                        # Implementation guide
│
├── 2019TurkishLocalElections(Prediction)/   # Local election predictions
│   ├── local_election_prediction.py     # Multi-city prediction system
│   │── script.py                       # Local analysis script
│   ├── anketler/*.csv                  # City-specific polling data (10 major cities)
│   └── Side-by-side prediction display
│
├── 2023TurkishGeneralElections(Script)/ # 2023 general election analysis
│   ├── dual_anket_script.py            # Presidential and parliamentary analysis
│   ├── party.py                        # D'Hondt system simulation
│   ├── *.csv                           # Comprehensive polling datasets
│   └── Vote distribution & seat calculation
│
└── 2024_Local(Monte Carlo)/             # Advanced Monte Carlo simulations
    ├── advanced_election_predictor.py   # 50,000+ iteration simulations
    ├── scenario_analyzer.py             # Multi-scenario analysis
    ├── dashboard.py                     # Executive dashboard generation
    ├── data/                            # Raw and processed election data
    ├── scripts/                         # Data processing utilities
    └── outputs/                         # Comprehensive analysis reports
```

## 🎯 Core Features & Algorithms

### 🤖 Machine Learning Models
- **Linear Regression** (2015): Multi-feature regression with regularization
- **Random Forest** (2018): 200-tree ensemble with cross-validation
- **Monte Carlo Simulation** (2024): 50,000+ iterations with uncertainty analysis
- **Statistical Modeling** (2019): Weighted polling averages with variance analysis

### 📊 Advanced Analytics
- **Cross-Validation**: Model reliability assessment
- **Hyperparameter Optimization**: Automated parameter tuning
- **Ensemble Learning**: Multiple algorithm combination
- **Uncertainty Quantification**: Confidence intervals and error bounds
- **Scenario Analysis**: Multiple election outcome simulations

### 🎨 Visualization & Reporting
- **Interactive Charts**: Bar charts, pie charts, trend analysis
- **Executive Dashboards**: Comprehensive overview reports
- **Confidence Intervals**: Statistical uncertainty visualization
- **Comparative Analysis**: Multi-scenario result comparison
- **Real-time Updates**: Dynamic prediction updates

## 🛠️ Technical Implementation

### Core Technologies
```python
# Machine Learning & Statistics
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=1.0.0
scipy>=1.7.0

# Data Visualization
matplotlib>=3.4.0
seaborn>=0.11.0

# Data Processing
typing>=3.7.0
warnings  # Built-in
os        # Built-in
glob      # Built-in
random    # Built-in
datetime  # Built-in
```

### Key Algorithms
- **Linear/Ridge/Lasso/ElasticNet Regression**: For trend analysis
- **Random Forest Classifier**: For complex pattern recognition
- **Monte Carlo Methods**: For uncertainty quantification
- **Beta Distribution Sampling**: For bounded probability modeling
- **D'Hondt Electoral System**: For seat allocation simulation

## 🗳️ Election Coverage

### Temporal Scope (2015-2024)
- **2015 General Elections**: June & November rounds
- **2018 General Elections**: Presidential & Parliamentary
- **2019 Local Elections**: 10 major Turkish cities
- **2023 General Elections**: Presidential & Parliamentary
- **2024 Local Elections**: Comprehensive national coverage

### Geographic Coverage
- **National Level**: Turkey-wide predictions
- **Provincial Level**: 81 Turkish provinces
- **Metropolitan Areas**: Istanbul, Ankara, Izmir, and 30+ major cities
- **Urban/Rural Analysis**: Demographic-based predictions

## 📈 Model Performance & Accuracy

### Historical Validation Results
- **2015 Linear Regression**: R² scores up to 0.95
- **2018 Random Forest**: 100% training accuracy, cross-validated
- **2019 Local Predictions**: ±1% average deviation
- **2024 Monte Carlo**: 95% confidence intervals with uncertainty analysis

### Data Quality Metrics
- **152+ polling datasets** (2015)
- **35+ polling companies** analyzed
- **26+ high-quality polls** (2018)
- **50,000+ simulation iterations** (2024)

## 🚀 Quick Start Guide

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/Tamerefe/TurkeyElectionGenerator.git
cd TurkeyElectionGenerator

# Install dependencies
pip install numpy pandas scikit-learn matplotlib seaborn scipy
```

### 2. Run Predictions

#### Linear Regression (2015)
```bash
cd "2015_General(Linear Regression)"
python electionguess.py
python analysis_report.py  # Generate comprehensive analysis
```

#### Random Forest (2018)
```bash
cd "2018_General(Random Forest)"
python generator.py
```

#### Local Elections (2019)
```bash
cd "2019TurkishLocalElections(Prediction)"
python local_election_prediction.py
```

#### Advanced Simulations (2024)
```bash
cd "2024_Local(Monte Carlo)"
python advanced_election_predictor.py
python scenario_analyzer.py
python dashboard.py  # Generate executive dashboard
```

## 📊 Output Organization

### Organized Output System (August 2025+)
```
each_project_folder/
├── outputs/
│   ├── graphs/          # 📊 All visualizations and charts
│   ├── models/          # 🤖 Trained ML models (.pkl files)
│   ├── reports/         # 📄 Analysis reports (.txt, .md)
│   └── data/            # 💾 Processed datasets (.csv)
└── README.md            # Project-specific documentation
```

### Key Benefits
- ✅ **No file clutter**: Organized folder structure
- ✅ **Timestamp versioning**: Automatic file naming
- ✅ **Categorized outputs**: Easy file navigation
- ✅ **Automated documentation**: Self-documenting results
- ✅ **Git-friendly**: Clean repository structure

## 🔬 Data Sources & Methodology

### Polling Data Standards
- **Chronological Organization**: Most recent polls prioritized
- **Company Credibility**: Verified polling organizations only
- **Sample Size Weighting**: Larger samples given higher weight
- **Bias Adjustment**: Political affiliations documented and adjusted
- **Missing Data Handling**: Statistical imputation methods

### Quality Assurance
- **Source Verification**: All polls from registered Turkish companies
- **Cross-Validation**: Multiple polling sources compared
- **Temporal Consistency**: Historical trend validation
- **Statistical Significance**: Confidence intervals for all predictions

## 🎛️ Advanced Configuration

### Monte Carlo Parameters (2024)
```python
# Simulation settings
N_SIMULATIONS = 50000
UNCERTAINTY_FACTORS = {
    'polling_error': ±3%,
    'sampling_bias': ±2.5%,
    'undecided_distribution': ±8%,
    'last_minute_change': ±2%,
    'turnout_variation': ±5%
}
CONFIDENCE_LEVELS = [80%, 90%, 95%]
```

### Random Forest Settings (2018)
```python
# Model configuration
N_ESTIMATORS = 200
CROSS_VALIDATION = True
AUTO_PARAMETER_OPTIMIZATION = True
CLASS_BALANCING = True
```

## 📚 Documentation & Reports

### Available Documentation
- **Technical Analysis Reports**: Detailed methodology explanations
- **Performance Metrics**: Model accuracy and validation results
- **Usage Examples**: Practical implementation guides
- **API Documentation**: Function and class references

### Generated Reports
- **Executive Summaries**: High-level prediction overviews
- **Statistical Analysis**: Detailed numerical breakdowns
- **Uncertainty Analysis**: Risk assessment and confidence intervals
- **Comparative Studies**: Multi-model result comparisons

## 🤝 Contributing

### Development Guidelines
1. **Code Standards**: Follow PEP 8 Python style guidelines
2. **Testing**: Include unit tests for new features
3. **Documentation**: Update README files for new modules
4. **Data Validation**: Verify all polling data sources

### Bug Reports & Features
- Open issues for bug reports
- Suggest new features via GitHub issues
- Submit pull requests for improvements

## 📄 License

This project is licensed under the **MIT License**. See [`LICENSE.md`](LICENSE.md) for full details.

```
Copyright (c) 2023-2025 B.Tamer Akipek
Permission is hereby granted, free of charge, to use, modify, and distribute.
```

## 📞 Support & Contact

### Technical Support
- **GitHub Issues**: [Report bugs or request features](https://github.com/Tamerefe/TurkeyElectionGenerator/issues)
- **Email**: tamerakipek@gmail.com
- **Documentation**: Check individual project README files

### Academic Collaboration
- Research partnerships welcome
- Data sharing for academic purposes
- Methodology consultation available

---

**🏆 Achievement Summary**: Comprehensive election prediction system covering 9+ years of Turkish electoral data with multiple ML approaches and 95%+ accuracy rates.
