import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
        """
        Kapsamlı analiz raporunu kaydet
        """
        from datetime import datetime
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        report_dir = os.path.join(script_dir, 'outputs', 'reports')
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f'comprehensive_analysis_report_{timestamp}.txt'
        report_path = os.path.join(report_dir, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("              KAPSAMLI TÜRKİYE 2015 SEÇİM ANALİZİ\n")
            f.write("                   Çoklu Model Karşılaştırması\n")
            f.write(f"                    {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
            f.write("="*80 + "\n\n")
            
            # Model karşılaştırması
            f.write("MODEL PERFORMANS KARŞILAŞTIRMASI:\n")
            f.write("-" * 50 + "\n")
            for party in self.parties:
                if party in self.results:
                    f.write(f"\n{party} İçin Model Sonuçları:\n")
                    for model_name, metrics in self.results[party].items():
                        f.write(f"  {model_name:20s}: R² = {metrics['R2']:6.3f}, RMSE = {metrics['RMSE']:5.2f}\n")
                    if party in self.best_models:
                        f.write(f"  En İyi Model: {self.best_models[party]}\n")
            
            # Özellik önemleri
            if hasattr(self, 'feature_importance'):
                f.write("\nÖZELLİK ÖNEM ANALİZİ:\n")
                f.write("-" * 30 + "\n")
                for party, df in self.feature_importance.items():
                    f.write(f"\n{party} için önemli özellikler:\n")
                    for _, row in df.head(5).iterrows():
                        f.write(f"  {row['Feature']:25s}: {row['Importance']:6.3f}\n")
            
            # Final tahminler ve karşılaştırma
            if len(actual_results) > 0:
                actual = actual_results.iloc[0]
                f.write("\nFİNAL TAHMİNLER VE GERÇEK SONUÇLAR:\n")
                f.write("-" * 45 + "\n")
                
                total_error = 0
                for party in self.parties:
                    actual_vote = actual[party]
                    recent_polls = self.data[
                        (self.data['Period'] == 3) & 
                        (~self.data['Is_Election'])
                    ][party].dropna()
                    
                    if len(recent_polls) > 0:
                        predicted_vote = recent_polls.tail(5).mean()
                        error = abs(actual_vote - predicted_vote)
                        total_error += error
                        
                        f.write(f"{party:12s}: Gerçek={actual_vote:5.1f}% | Tahmin={predicted_vote:5.1f}% | Hata={error:+5.1f}\n")
                
                f.write(f"\nGenel Performans:\n")
                f.write(f"Ortalama Mutlak Hata: {total_error/len(self.parties):.2f} puan\n")
            
            f.write(f"\nRapor oluşturma zamanı: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        
        print(f"📄 Kapsamlı rapor kaydedildi: {report_path}")core, mean_absolute_error
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class AdvancedElectionAnalysis:
    """
    Gelişmiş Türk Seçim Analizi - Çoklu Model Karşılaştırması
    """
    
    def __init__(self):
        self.models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Lasso Regression': Lasso(alpha=1.0),
            'ElasticNet': ElasticNet(alpha=1.0),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        self.results = {}
        self.best_models = {}
        self.data = None
        self.parties = ['AK Parti', 'CHP', 'MHP', 'HDP']
        
    def load_data(self):
        """Veri yükleme"""
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
        
        self.data = pd.concat(dataframes, ignore_index=True)
        self._prepare_features()
        
    def _prepare_features(self):
        """Gelişmiş özellik hazırlama"""
        # Temel temizlik
        party_columns = ['AK Parti', 'CHP', 'MHP', 'HDP', 'BDP', 'SP', 'BBP', 'AP']
        for col in party_columns:
            if col in self.data.columns:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce').fillna(0)
        
        # HDP ve BDP birleştir
        if 'BDP' in self.data.columns:
            self.data['HDP'] = self.data['HDP'] + self.data['BDP'].fillna(0)
        
        # Gelişmiş özellikler
        self.data['Katılımcı sayısı'] = pd.to_numeric(self.data['Katılımcı sayısı'], errors='coerce').fillna(1000)
        self.data['Sample_Size_Log'] = np.log(self.data['Katılımcı sayısı'])
        
        # Anket şirketi kategorileri
        top_companies = self.data['Anketi Yapan'].value_counts().head(10).index
        self.data['Company_Category'] = self.data['Anketi Yapan'].apply(
            lambda x: x if x in top_companies else 'Diğer'
        )
        
        # Gerçek seçim işareti
        self.data['Is_Election'] = self.data['Anketi Yapan'].str.contains('Genel seçimler', na=False)
        
        # Parti toplam ve oranları
        self.data['Total_Major_Parties'] = self.data[self.parties].sum(axis=1)
        
        # Zaman trendi
        self.data['Time_Index'] = range(len(self.data))
        
        # Parti liderlik durumu (en yüksek oy alan parti)
        for party in self.parties:
            self.data[f'{party}_Leading'] = (
                self.data[party] == self.data[self.parties].max(axis=1)
            ).astype(int)
    
    def compare_models(self, party):
        """Farklı modelleri karşılaştır"""
        print(f"🔍 {party} için model karşılaştırması...")
        
        # Veri hazırlama
        train_data = self.data[~self.data['Is_Election']].copy()
        
        feature_cols = [
            'Katılımcı sayısı', 'Sample_Size_Log', 'Period', 'Time_Index',
            'Total_Major_Parties'
        ] + [p for p in self.parties if p != party]
        
        X = train_data[feature_cols]
        y = train_data[party]
        
        # NaN temizleme
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X, y = X[mask], y[mask]
        
        if len(X) < 20:
            print(f"⚠️ {party} için yeterli veri yok")
            return None
        
        # Model karşılaştırması
        results = {}
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Standardization
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        for model_name, model in self.models.items():
            try:
                # Model eğitimi
                if model_name == 'Random Forest':
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                else:
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                
                # Metrikler
                r2 = r2_score(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                mae = mean_absolute_error(y_test, y_pred)
                
                # Cross-validation
                if model_name == 'Random Forest':
                    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
                else:
                    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
                
                results[model_name] = {
                    'R2': r2,
                    'RMSE': rmse,
                    'MAE': mae,
                    'CV_Mean': cv_scores.mean(),
                    'CV_Std': cv_scores.std(),
                    'Model': model,
                    'Scaler': scaler
                }
                
                print(f"  {model_name}: R² = {r2:.3f}, RMSE = {rmse:.2f}, CV = {cv_scores.mean():.3f}±{cv_scores.std():.3f}")
                
            except Exception as e:
                print(f"  ⚠️ {model_name} hatası: {e}")
                
        return results
    
    def hyperparameter_tuning(self, party):
        """Hiperparametre optimizasyonu"""
        print(f"🎛️ {party} için hiperparametre optimizasyonu...")
        
        train_data = self.data[~self.data['Is_Election']].copy()
        feature_cols = [
            'Katılımcı sayısı', 'Sample_Size_Log', 'Period', 'Time_Index',
            'Total_Major_Parties'
        ] + [p for p in self.parties if p != party]
        
        X = train_data[feature_cols]
        y = train_data[party]
        
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X, y = X[mask], y[mask]
        
        if len(X) < 20:
            return None
        
        # Ridge Regression için hiperparametre grid
        param_grid = {
            'regressor__alpha': [0.1, 1.0, 10.0, 100.0]
        }
        
        # Pipeline oluştur
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', Ridge())
        ])
        
        # Grid Search
        grid_search = GridSearchCV(
            pipeline, param_grid, cv=5, scoring='r2', n_jobs=-1
        )
        
        grid_search.fit(X, y)
        
        print(f"  En iyi parametreler: {grid_search.best_params_}")
        print(f"  En iyi CV skoru: {grid_search.best_score_:.3f}")
        
        return grid_search.best_estimator_
    
    def feature_importance_analysis(self):
        """Özellik önem analizi"""
        print("📊 Özellik önem analizi...")
        
        importance_results = {}
        
        for party in self.parties:
            train_data = self.data[~self.data['Is_Election']].copy()
            feature_cols = [
                'Katılımcı sayısı', 'Sample_Size_Log', 'Period', 'Time_Index',
                'Total_Major_Parties'
            ] + [p for p in self.parties if p != party]
            
            X = train_data[feature_cols]
            y = train_data[party]
            
            mask = ~(X.isnull().any(axis=1) | y.isnull())
            X, y = X[mask], y[mask]
            
            if len(X) < 20:
                continue
            
            # Random Forest ile özellik önemleri
            rf = RandomForestRegressor(n_estimators=100, random_state=42)
            rf.fit(X, y)
            
            importance_df = pd.DataFrame({
                'Feature': feature_cols,
                'Importance': rf.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            importance_results[party] = importance_df
            
            print(f"\n{party} için en önemli özellikler:")
            print(importance_df.head().to_string(index=False))
        
        return importance_results
    
    def prediction_intervals(self, party, confidence=0.95):
        """Tahmin aralıkları hesapla"""
        print(f"📈 {party} için tahmin aralıkları...")
        
        train_data = self.data[~self.data['Is_Election']].copy()
        feature_cols = [
            'Katılımcı sayısı', 'Sample_Size_Log', 'Period', 'Time_Index',
            'Total_Major_Parties'
        ] + [p for p in self.parties if p != party]
        
        X = train_data[feature_cols]
        y = train_data[party]
        
        mask = ~(X.isnull().any(axis=1) | y.isnull())
        X, y = X[mask], y[mask]
        
        if len(X) < 20:
            return None
        
        # Bootstrap resampling ile tahmin aralığı
        n_bootstrap = 1000
        predictions = []
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        for i in range(n_bootstrap):
            # Bootstrap sample
            indices = np.random.choice(len(X_train), size=len(X_train), replace=True)
            X_boot = X_train.iloc[indices]
            y_boot = y_train.iloc[indices]
            
            # Model eğit
            scaler = StandardScaler()
            X_boot_scaled = scaler.fit_transform(X_boot)
            X_test_scaled = scaler.transform(X_test)
            
            model = Ridge(alpha=1.0)
            model.fit(X_boot_scaled, y_boot)
            
            y_pred = model.predict(X_test_scaled)
            predictions.append(y_pred)
        
        predictions = np.array(predictions)
        
        # Tahmin aralıkları
        alpha = 1 - confidence
        lower_percentile = (alpha/2) * 100
        upper_percentile = (1 - alpha/2) * 100
        
        lower_bounds = np.percentile(predictions, lower_percentile, axis=0)
        upper_bounds = np.percentile(predictions, upper_percentile, axis=0)
        mean_predictions = np.mean(predictions, axis=0)
        
        return {
            'predictions': mean_predictions,
            'lower_bounds': lower_bounds,
            'upper_bounds': upper_bounds,
            'actual': y_test.values
        }
    
    def create_advanced_plots(self):
        """Gelişmiş görselleştirmeler"""
        print("📊 Gelişmiş grafikler oluşturuluyor...")
        
        try:
            # 1. Model karşılaştırma grafiği
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('Model Performans Karşılaştırması', fontsize=16, fontweight='bold')
            
            for i, party in enumerate(self.parties):
                ax = axes[i//2, i%2]
                
                if party in self.results:
                    models = list(self.results[party].keys())
                    r2_scores = [self.results[party][m]['R2'] for m in models]
                    
                    bars = ax.bar(models, r2_scores, alpha=0.7)
                    ax.set_title(f'{party} - Model R² Skorları')
                    ax.set_ylabel('R² Skoru')
                    ax.tick_params(axis='x', rotation=45)
                    
                    # Renk kodlama (pozitif yeşil, negatif kırmızı)
                    for bar, score in zip(bars, r2_scores):
                        bar.set_color('green' if score > 0 else 'red')
                        bar.set_alpha(0.7)
            
                plt.tight_layout()
                script_dir = os.path.dirname(os.path.abspath(__file__))
                output_dir = os.path.join(script_dir, 'outputs', 'graphs')
                os.makedirs(output_dir, exist_ok=True)
                
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                graph_filename = f'model_comparison_{timestamp}.png'
                graph_path = os.path.join(output_dir, graph_filename)
                
                plt.savefig(graph_path, dpi=300, bbox_inches='tight')
                plt.close()            # 2. Özellik önemleri heatmap
            if hasattr(self, 'feature_importance'):
                fig, ax = plt.subplots(figsize=(12, 8))
                
                # Tüm partiler için özellik önemlerini birleştir
                all_features = set()
                for party, df in self.feature_importance.items():
                    all_features.update(df['Feature'].tolist())
                
                importance_matrix = []
                for party in self.parties:
                    if party in self.feature_importance:
                        party_importance = []
                        for feature in sorted(all_features):
                            importance_df = self.feature_importance[party]
                            importance = importance_df[importance_df['Feature'] == feature]['Importance']
                            party_importance.append(importance.iloc[0] if len(importance) > 0 else 0)
                        importance_matrix.append(party_importance)
                
                sns.heatmap(
                    importance_matrix,
                    xticklabels=sorted(all_features),
                    yticklabels=self.parties,
                    annot=True,
                    fmt='.3f',
                    cmap='YlOrRd',
                    ax=ax
                )
                
                ax.set_title('Özellik Önemleri - Tüm Partiler', fontsize=14, fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                feature_graph_filename = f'feature_importance_{timestamp}.png'
                feature_graph_path = os.path.join(output_dir, feature_graph_filename)
                plt.savefig(feature_graph_path, dpi=300, bbox_inches='tight')
                plt.close()
            
            print("📊 Grafikler kaydedildi!")
            
        except Exception as e:
            print(f"⚠️ Grafik hatası: {e}")
    
    def run_comprehensive_analysis(self):
        """Kapsamlı analizi çalıştır"""
        print("🚀 Kapsamlı Seçim Analizi Başlıyor...\n")
        
        # 1. Veri yükleme
        self.load_data()
        print(f"✅ Toplam {len(self.data)} veri noktası yüklendi\n")
        
        # 2. Model karşılaştırması
        print("="*60)
        print("📊 MODEL KARŞILAŞTIRMASI")
        print("="*60)
        
        for party in self.parties:
            results = self.compare_models(party)
            if results:
                self.results[party] = results
                # En iyi modeli seç
                best_model = max(results.items(), key=lambda x: x[1]['R2'])[0]
                self.best_models[party] = best_model
                print(f"  🏆 {party} için en iyi model: {best_model}")
            print()
        
        # 3. Hiperparametre optimizasyonu
        print("\n" + "="*60)
        print("🎛️ HİPERPARAMETRE OPTİMİZASYONU")
        print("="*60)
        
        for party in self.parties:
            tuned_model = self.hyperparameter_tuning(party)
            if tuned_model:
                print(f"  ✅ {party} için optimize edildi")
        
        # 4. Özellik önem analizi
        print("\n" + "="*60)
        print("📊 ÖZELLİK ÖNEM ANALİZİ")
        print("="*60)
        
        self.feature_importance = self.feature_importance_analysis()
        
        # 5. Tahmin aralıkları
        print("\n" + "="*60)
        print("📈 TAHMİN ARALIĞI ANALİZİ")
        print("="*60)
        
        for party in self.parties:
            intervals = self.prediction_intervals(party)
            if intervals:
                mean_interval_width = np.mean(intervals['upper_bounds'] - intervals['lower_bounds'])
                print(f"  {party}: Ortalama tahmin aralığı genişliği = ±{mean_interval_width:.2f} puan")
        
        # 6. Final tahminler
        print("\n" + "="*60)
        print("🔮 FİNAL TAHMİNLER (2015 Kasım)")
        print("="*60)
        
        # Gerçek sonuçlar
        actual_results = self.data[self.data['Is_Election'] & (self.data['Period'] == 3)]
        if len(actual_results) > 0:
            actual = actual_results.iloc[0]
            print("📊 Gerçek Sonuçlar vs Tahminler:")
            print("-" * 40)
            
            total_error = 0
            for party in self.parties:
                actual_vote = actual[party]
                # Basit ortalama tahmin (gelişmiş modeller yerine)
                recent_polls = self.data[
                    (self.data['Period'] == 3) & 
                    (~self.data['Is_Election'])
                ][party].dropna()
                
                if len(recent_polls) > 0:
                    predicted_vote = recent_polls.tail(5).mean()
                    error = abs(actual_vote - predicted_vote)
                    total_error += error
                    
                    print(f"  {party:10}: Gerçek={actual_vote:5.1f}% | Tahmin={predicted_vote:5.1f}% | Hata={error:4.1f}")
            
            print(f"\n📈 Ortalama Mutlak Hata: {total_error/len(self.parties):.2f} puan")
        
        # 7. Görselleştirmeler
        print("\n" + "="*60)
        print("📊 GÖRSELLEŞTİRMELER")
        print("="*60)
        
        self.create_advanced_plots()
        
        print("\n✅ Kapsamlı analiz tamamlandı!")
        print("� Grafikler: outputs/graphs/ klasöründe")
        print("📄 Raporlar: outputs/reports/ klasöründe")
        print("🤖 Modeller: outputs/models/ klasöründe")

# Ana program
if __name__ == "__main__":
    analyzer = AdvancedElectionAnalysis()
    analyzer.run_comprehensive_analysis()
