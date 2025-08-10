#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2024 Türkiye Yerel Seçimleri Anket Verisi Temizleme ve Analiz Aracı
Bu script anket verilerini temizler, düzenler ve analiz eder.

Özellikler:
- Wikipedia'dan çekilen ham anket verilerini temizler
- Parti sütunlarını otomatik tanımlar ve düzenler
- Gereksiz sütunları ve satırları kaldırır
- İl bazında ayrı dosyalar oluşturur
- Kapsamlı analiz raporları üretir
- Temiz bir klasör yapısı oluşturur
"""

import pandas as pd
import numpy as np
import os
import re
import shutil
from pathlib import Path
from datetime import datetime

class AnketVeriTemizleyici:
    """
    Anket verilerini temizleyen ve analiz eden ana sınıf
    """
    
    def __init__(self, girdi_klasoru="../data/raw_data", cikti_klasoru="../data/processed_data"):
        self.girdi_klasoru = Path(girdi_klasoru)
        self.cikti_klasoru = Path(cikti_klasoru)
        self.log_mesajlari = []
        
        # Parti isimleri ve alternatifleri
        self.parti_eslestirme = {
            'AKP': ['AKP', 'AK Parti', 'AK PARTİ'],
            'CHP': ['CHP'],
            'İYİ': ['İYİ', 'IYI', 'İYİ PARTİ'],
            'MHP': ['MHP'],
            'HDP': ['HDP'],
            'DEM': ['DEM', 'DEMOKRASI'],
            'YRP': ['YRP', 'YENİDEN'],
            'ZP': ['ZP', 'ZAFER'],
            'TİP': ['TİP', 'TIP', 'TURKİYE İŞÇİ'],
            'SP': ['SP', 'SAADET'],
            'BBP': ['BBP', 'BÜYÜK BİRLİK'],
            'DEVA': ['DEVA'],
            'GP': ['GP', 'GELECEK'],
            'DP': ['DP', 'DEMOKRAT'],
            'DSP': ['DSP', 'DEMOKRATİK SOL']
        }
    
    def log(self, mesaj):
        """Log mesajı ekler"""
        self.log_mesajlari.append(f"[{datetime.now().strftime('%H:%M:%S')}] {mesaj}")
        print(mesaj)
    
    def klasor_yapisini_olustur(self):
        """Temiz klasör yapısını oluşturur"""
        self.log("📁 Klasör yapısı oluşturuluyor...")
        
        # Ana çıktı klasörü
        self.cikti_klasoru.mkdir(parents=True, exist_ok=True)
        
        # Alt klasörler
        self.iller_klasoru = self.cikti_klasoru / "iller"
        self.raporlar_klasoru = self.cikti_klasoru / "raporlar"
        self.birlesik_klasoru = self.cikti_klasoru / "birlesik_veriler"
        
        for klasor in [self.iller_klasoru, self.raporlar_klasoru, self.birlesik_klasoru]:
            klasor.mkdir(parents=True, exist_ok=True)
        
        self.log(f"✓ Klasör yapısı oluşturuldu: {self.cikti_klasoru}")
    
    def sutun_isimlerini_temizle(self, columns):
        """Sütun isimlerini temizler ve düzenler"""
        temizlenmis_sutunlar = []
        
        for sutun in columns:
            sutun_str = str(sutun)
            
            # Tekrar eden kelimeleri kaldır
            if ' ' in sutun_str:
                kelimeler = sutun_str.split()
                if len(kelimeler) >= 2 and kelimeler[0] == kelimeler[1]:
                    temiz_isim = kelimeler[0]
                else:
                    temiz_isim = sutun_str
            else:
                temiz_isim = sutun_str
            
            # Özel durumlar için düzenleme
            if 'Tarih' in temiz_isim:
                temiz_isim = 'Tarih'
            elif 'Anket' in temiz_isim and 'şirket' in temiz_isim:
                temiz_isim = 'Anket_Şirketi'
            elif 'Örneklem' in temiz_isim:
                temiz_isim = 'Örneklem'
            elif 'Diğerleri' in temiz_isim:
                temiz_isim = 'Diğerleri'
            elif 'Kararsız' in temiz_isim:
                temiz_isim = 'Kararsız'
            elif 'Fark' in temiz_isim:
                temiz_isim = 'Fark'
            elif 'KaynakURL' in temiz_isim:
                temiz_isim = 'Kaynak_URL'
            elif 'Bölüm' in temiz_isim:
                temiz_isim = 'İl'
            
            temizlenmis_sutunlar.append(temiz_isim)
        
        return temizlenmis_sutunlar
    
    def parti_sutunlarini_tanimla(self, df, baslangic_sutun=5):
        """Veri içeriğine bakarak parti sütunlarını tanımlar"""
        parti_haritalama = {}
        
        if len(df.columns) > baslangic_sutun:
            # İlk satırdaki sayısal değerleri kontrol et
            ilk_satir = df.iloc[0, baslangic_sutun:]
            
            # Ana partiler (en yaygın olanlar)
            ana_partiler = ['AKP', 'CHP', 'İYİ', 'MHP', 'HDP', 'DEM', 'YRP', 'ZP']
            
            # Sayısal sütunları parti olarak kabul et
            sayisal_sutunlar = []
            for i, hucre in enumerate(ilk_satir):
                try:
                    deger = pd.to_numeric(hucre, errors='coerce')
                    if not pd.isna(deger) and deger > 0:
                        sayisal_sutunlar.append(baslangic_sutun + i)
                except:
                    pass
            
            # Maksimum 8 parti sütunu (gerçekçi sınır)
            if len(sayisal_sutunlar) > 8:
                sayisal_sutunlar = sayisal_sutunlar[:8]
            
            # Parti isimlerini ata
            for i, sutun_indeksi in enumerate(sayisal_sutunlar):
                if i < len(ana_partiler):
                    parti_haritalama[sutun_indeksi] = ana_partiler[i]
                else:
                    parti_haritalama[sutun_indeksi] = f'Parti_{i+1}'
        
        return parti_haritalama
    
    def veriyi_temizle(self, df):
        """Ana veri temizleme fonksiyonu"""
        if df.empty:
            return df
        
        temizlenmis_df = df.copy()
        
        # Gereksiz satırları kaldır
        temizlenmis_df = temizlenmis_df[~temizlenmis_df.astype(str).eq('2024').any(axis=1)]
        temizlenmis_df = temizlenmis_df.dropna(how='all')
        
        if temizlenmis_df.empty:
            return temizlenmis_df
        
        # Sütun isimlerini temizle
        yeni_sutunlar = self.sutun_isimlerini_temizle(temizlenmis_df.columns)
        
        # Parti sütunlarını tanımla
        parti_haritalama = self.parti_sutunlarini_tanimla(temizlenmis_df)
        
        # Final sütun isimlerini oluştur
        son_sutunlar = []
        for i, sutun in enumerate(yeni_sutunlar):
            if i in parti_haritalama:
                son_sutunlar.append(parti_haritalama[i])
            else:
                son_sutunlar.append(sutun)
        
        temizlenmis_df.columns = son_sutunlar
        
        # Anlamlı sütunları tut
        anlamli_sutunlar = []
        for sutun in temizlenmis_df.columns:
            if ('Unnamed' not in str(sutun) and 
                str(sutun) != 'nan' and 
                len(str(sutun).strip()) > 0):
                anlamli_sutunlar.append(sutun)
        
        if anlamli_sutunlar:
            temizlenmis_df = temizlenmis_df[anlamli_sutunlar]
        
        # Sayısal sütunları düzelt
        parti_sutunlari = list(self.parti_eslestirme.keys())
        sayisal_sutunlar = [sutun for sutun in temizlenmis_df.columns if sutun in parti_sutunlari]
        sayisal_sutunlar.extend(['Örneklem', 'Diğerleri', 'Kararsız', 'Fark'])
        
        for sutun in sayisal_sutunlar:
            if sutun in temizlenmis_df.columns:
                temizlenmis_df[sutun] = pd.to_numeric(temizlenmis_df[sutun], errors='coerce')
        
        # Boş satırları tekrar kaldır
        temizlenmis_df = temizlenmis_df.dropna(how='all')
        
        return temizlenmis_df
    
    def dosyalari_isle(self):
        """Tüm dosyaları işler"""
        self.log("📊 Dosyalar işleniyor...")
        
        islenen_dosyalar = []
        hata_sayisi = 0
        
        for dosya_yolu in self.girdi_klasoru.glob("*.csv"):
            try:
                self.log(f"İşleniyor: {dosya_yolu.name}")
                
                # CSV dosyasını oku
                df = pd.read_csv(dosya_yolu, encoding='utf-8-sig')
                
                # Veriyi temizle
                temizlenmis_df = self.veriyi_temizle(df)
                
                if not temizlenmis_df.empty:
                    # İl adını tespit et
                    il_adi = self.il_adini_cikart(dosya_yolu.name)
                    
                    # Temizlenmiş dosyayı kaydet
                    cikti_dosyasi = self.iller_klasoru / f"{il_adi}.csv"
                    temizlenmis_df.to_csv(cikti_dosyasi, index=False, encoding='utf-8-sig')
                    
                    islenen_dosyalar.append({
                        'il': il_adi,
                        'dosya': cikti_dosyasi,
                        'anket_sayisi': len(temizlenmis_df),
                        'sutun_sayisi': len(temizlenmis_df.columns),
                        'partiler': [col for col in temizlenmis_df.columns if col in self.parti_eslestirme.keys()]
                    })
                    
                    self.log(f"✓ {il_adi}: {len(temizlenmis_df)} anket, {len(temizlenmis_df.columns)} sütun")
                else:
                    self.log(f"⚠ Boş veri: {dosya_yolu.name}")
                    
            except Exception as e:
                hata_sayisi += 1
                self.log(f"✗ Hata: {dosya_yolu.name} - {str(e)}")
        
        self.log(f"📈 İşlem tamamlandı: {len(islenen_dosyalar)} başarılı, {hata_sayisi} hatalı")
        return islenen_dosyalar
    
    def il_adini_cikart(self, dosya_adi):
        """Dosya adından il adını çıkarır"""
        # Dosya uzantısını kaldır
        il_adi = dosya_adi.replace('.csv', '')
        
        # Sık kullanılan ekleri kaldır
        ekler = ['_2024_anketler', '_anketler', '_genel', '2024']
        for ek in ekler:
            il_adi = il_adi.replace(ek, '')
        
        # Başında ve sonunda boşluk varsa kaldır
        il_adi = il_adi.strip('_').strip()
        
        # İlk harfi büyük yap
        return il_adi.title()
    
    def birlesik_dosya_olustur(self, islenen_dosyalar):
        """Tüm illerin verilerini birleştiren dosya oluşturur"""
        self.log("📋 Birleşik dosya oluşturuluyor...")
        
        tum_veriler = []
        
        for dosya_bilgi in islenen_dosyalar:
            try:
                df = pd.read_csv(dosya_bilgi['dosya'], encoding='utf-8-sig')
                tum_veriler.append(df)
            except Exception as e:
                self.log(f"⚠ Birleştirme hatası: {dosya_bilgi['il']} - {str(e)}")
        
        if tum_veriler:
            birlesik_df = pd.concat(tum_veriler, ignore_index=True)
            
            # Birleşik dosyayı kaydet
            birlesik_dosya = self.birlesik_klasoru / "tum_iller_anket_verileri.csv"
            birlesik_df.to_csv(birlesik_dosya, index=False, encoding='utf-8-sig')
            
            self.log(f"✓ Birleşik dosya oluşturuldu: {len(birlesik_df)} toplam anket")
            return birlesik_df
        
        return None
    
    def ozet_raporu_olustur(self, islenen_dosyalar, birlesik_df):
        """Özet analiz raporu oluşturur"""
        self.log("📊 Özet raporu oluşturuluyor...")
        
        # İller için özet
        iller_ozeti = []
        for dosya_bilgi in islenen_dosyalar:
            iller_ozeti.append({
                'İl': dosya_bilgi['il'],
                'Anket_Sayısı': dosya_bilgi['anket_sayisi'],
                'Sütun_Sayısı': dosya_bilgi['sutun_sayisi'],
                'Parti_Sayısı': len(dosya_bilgi['partiler']),
                'Partiler': ', '.join(dosya_bilgi['partiler'])
            })
        
        # DataFrame oluştur ve sırala
        ozet_df = pd.DataFrame(iller_ozeti)
        ozet_df = ozet_df.sort_values('Anket_Sayısı', ascending=False)
        
        # Raporu kaydet
        rapor_dosyasi = self.raporlar_klasoru / "iller_ozet_raporu.csv"
        ozet_df.to_csv(rapor_dosyasi, index=False, encoding='utf-8-sig')
        
        # Detaylı analiz raporu oluştur
        self.detayli_rapor_olustur(ozet_df, birlesik_df)
        
        self.log(f"✓ Özet raporu oluşturuldu: {len(ozet_df)} il analiz edildi")
        return ozet_df
    
    def detayli_rapor_olustur(self, ozet_df, birlesik_df):
        """Detaylı analiz raporu oluşturur"""
        rapor_metni = []
        rapor_metni.append("=" * 60)
        rapor_metni.append("2024 TÜRKİYE YEREL SEÇİMLERİ ANKET VERİSİ ANALİZ RAPORU")
        rapor_metni.append("=" * 60)
        rapor_metni.append(f"Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        rapor_metni.append("")
        
        # Genel İstatistikler
        rapor_metni.append("📊 GENEL İSTATİSTİKLER")
        rapor_metni.append("-" * 30)
        rapor_metni.append(f"Toplam İl Sayısı: {len(ozet_df)}")
        rapor_metni.append(f"Toplam Anket Sayısı: {ozet_df['Anket_Sayısı'].sum()}")
        rapor_metni.append(f"Ortalama Anket/İl: {ozet_df['Anket_Sayısı'].mean():.1f}")
        rapor_metni.append("")
        
        # En Çok Anket Yapılan İller
        rapor_metni.append("🏆 EN ÇOK ANKET YAPILAN İLLER (İlk 10)")
        rapor_metni.append("-" * 40)
        for i, (_, row) in enumerate(ozet_df.head(10).iterrows(), 1):
            rapor_metni.append(f"{i:2d}. {row['İl']:15s} - {row['Anket_Sayısı']:3d} anket")
        rapor_metni.append("")
        
        # Parti Analizi
        if birlesik_df is not None:
            tum_partiler = set()
            for partiler_str in ozet_df['Partiler']:
                if pd.notna(partiler_str) and partiler_str:
                    partiler = [p.strip() for p in partiler_str.split(',')]
                    tum_partiler.update(partiler)
            
            rapor_metni.append("🎯 PARTİ ANALİZİ")
            rapor_metni.append("-" * 20)
            rapor_metni.append(f"Tespit Edilen Parti Sayısı: {len(tum_partiler)}")
            rapor_metni.append(f"Partiler: {', '.join(sorted(tum_partiler))}")
            rapor_metni.append("")
        
        # Log mesajları
        rapor_metni.append("📝 İŞLEM KAYITLARI")
        rapor_metni.append("-" * 20)
        rapor_metni.extend(self.log_mesajlari[-10:])  # Son 10 log mesajı
        
        # Raporu dosyaya yaz
        rapor_dosyasi = self.raporlar_klasoru / "detayli_analiz_raporu.txt"
        with open(rapor_dosyasi, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapor_metni))
        
        # Konsola da yazdır
        print("\n" + "\n".join(rapor_metni[:25]))  # İlk 25 satırı konsola yazdır
    
    def eski_dosyalari_temizle(self):
        """Eski temizlik dosyalarını kaldırır"""
        silinecek_klasorler = ['temiz_provinces', 'super_temiz_provinces']
        
        for klasor_adi in silinecek_klasorler:
            klasor_yolu = Path(klasor_adi)
            if klasor_yolu.exists():
                try:
                    shutil.rmtree(klasor_yolu)
                    self.log(f"🗑️ Eski klasör temizlendi: {klasor_adi}")
                except Exception as e:
                    self.log(f"⚠ Klasör silinemedi: {klasor_adi} - {str(e)}")
    
    def calistir(self):
        """Ana çalıştırma fonksiyonu"""
        print("🚀 2024 Türkiye Yerel Seçimleri Anket Verisi Temizleyici")
        print("=" * 55)
        
        # Girdi klasörü kontrolü
        if not self.girdi_klasoru.exists():
            self.log(f"❌ Girdi klasörü bulunamadı: {self.girdi_klasoru}")
            return
        
        # Eski dosyaları temizle
        self.eski_dosyalari_temizle()
        
        # Klasör yapısını oluştur
        self.klasor_yapisini_olustur()
        
        # Dosyaları işle
        islenen_dosyalar = self.dosyalari_isle()
        
        if not islenen_dosyalar:
            self.log("❌ Hiçbir dosya işlenemedi!")
            return
        
        # Birleşik dosya oluştur
        birlesik_df = self.birlesik_dosya_olustur(islenen_dosyalar)
        
        # Özet raporu oluştur
        ozet_df = self.ozet_raporu_olustur(islenen_dosyalar, birlesik_df)
        
        # Final raporu
        print(f"\n🎉 İŞLEM TAMAMLANDI!")
        print(f"📁 Temizlenmiş veriler: {self.cikti_klasoru}")
        print(f"📊 İşlenen il sayısı: {len(islenen_dosyalar)}")
        print(f"📈 Toplam anket sayısı: {sum(d['anket_sayisi'] for d in islenen_dosyalar)}")
        print(f"📋 Rapor klasörü: {self.raporlar_klasoru}")


def main():
    """Ana fonksiyon"""
    # Temizleyici oluştur ve çalıştır
    temizleyici = AnketVeriTemizleyici(
        girdi_klasoru="provinces",
        cikti_klasoru="temiz_anket_verileri"
    )
    
    temizleyici.calistir()


if __name__ == "__main__":
    main()
