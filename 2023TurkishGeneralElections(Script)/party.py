from random import randrange
import csv
from statistics import mean

# Anket tabanlı tahmin için flag (True = anket verisi, False = rastgele)
USE_POLL_PREDICTION = True

class myColors :
     
	ResetAll = "\033[0m"

	Default      = "\033[39m"
	Black        = "\033[30m"
	Red          = "\033[31m"
	Green        = "\033[32m"
	Yellow       = "\033[33m"
	Blue         = "\033[34m"
	Magenta      = "\033[35m"
	Cyan         = "\033[36m"
	LightGray    = "\033[37m"
	DarkGray     = "\033[90m"
	LightRed     = "\033[91m"
	LightGreen   = "\033[92m"
	LightYellow  = "\033[93m"
	LightBlue    = "\033[94m"
	LightMagenta = "\033[95m"
	LightCyan    = "\033[96m"
	White        = "\033[0;33m"

population = 85279553

voterPop = int(population*75.27/100)

ci = 0
mi = 0
evoi = 0
atai = 0
allV = 0
bgmsz = 0

def get_poll_averages():
    """CSV dosyasından anket ortalamalarını hesapla"""
    import os
    # Script'in bulunduğu dizini al ve CSV dosyasının tam yolunu oluştur
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'Genel_secim_anket.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            poll_data = []
            
            for row in reader:
                try:
                    # Tarih sütunu boş değilse ve geçerli veri varsa ekle
                    if row['Tarih'] and row['Tarih'].strip():
                        poll_data.append(row)
                except:
                    continue
            
            if not poll_data:
                print("❌ CSV dosyasında geçerli anket verisi bulunamadı")
                return None
            
            # Son 10 anketin ortalamasını al (daha güvenilir)
            recent_data = poll_data[:10]
            averages = {}
            
            parties = ['AKP', 'MHP', 'BBP', 'YRP', 'CHP', 'İYİ', 'YSGP', 'TİP', 'ZP', 'MP']
            
            for party in parties:
                values = []
                for poll in recent_data:
                    try:
                        value_str = poll.get(party, '').strip()
                        if value_str and value_str != '':
                            # Boş değerler yerine 0 yazılmış olabilir
                            value = float(value_str)
                            if value > 0:
                                values.append(value / 10)  # 1000'lik sistemden yüzdeye çevir
                    except (ValueError, TypeError):
                        continue
                
                if values:
                    averages[party] = mean(values)
                else:
                    averages[party] = 0
            
            print(f"✅ {len(recent_data)} anketin ortalaması hesaplandı")
            return averages
            
    except FileNotFoundError:
        print(f"❌ Anket CSV dosyası bulunamadı: {csv_path}")
        print("� Lütfen scripti doğru dizinden çalıştırdığınızdan emin olun")
        return None
    except Exception as e:
        print(f"❌ CSV dosyası okuma hatası: {e}")
        return None

if USE_POLL_PREDICTION:
    poll_avg = get_poll_averages()
    if poll_avg:
        print("📊 Anket ortalamalarına dayalı tahmin kullanılıyor...")
        voteAKP = round(poll_avg.get('AKP', 38), 2)
        voteMHP = round(poll_avg.get('MHP', 8), 2)
        voteBBP = round(poll_avg.get('BBP', 0.4), 2)
        voteYRP = round(poll_avg.get('YRP', 1.2), 2)
        voteCHP = round(poll_avg.get('CHP', 28), 2)
        voteIYI = round(poll_avg.get('İYİ', 10), 2)
        voteDEVA = 0  # CSV'de yok
        voteGP = 0    # CSV'de yok
        voteSP = 0    # CSV'de yok
        voteDP = 0    # CSV'de yok
        voteHDP = round(poll_avg.get('YSGP', 10), 2)
        voteTIP = round(poll_avg.get('TİP', 2), 2)
        voteZP = round(poll_avg.get('ZP', 1.7), 2)
        voteMP = round(poll_avg.get('MP', 1.5), 2)
        voteTDP = 0
        voteBTP = 0
        voteOTHER = round(100 - (voteAKP + voteMHP + voteBBP + voteYRP + voteCHP + voteIYI + voteHDP + voteTIP + voteZP + voteMP), 2)
    else:
        print("❌ Anket verileri yüklenemedi, rastgele değerler kullanılıyor...")
        USE_POLL_PREDICTION = False

if not USE_POLL_PREDICTION:
    print("🎲 Rastgele değerler kullanılıyor...")
    # Rastgele değerler (datas.py olmadığı için basit random)
    voteAKP = round(35 + randrange(10), 2)      # 35-45 arası
    voteMHP = round(6 + randrange(6), 2)        # 6-12 arası  
    voteBBP = round(0.2 + randrange(3)/10, 2)   # 0.2-0.5 arası
    voteYRP = round(0.5 + randrange(20)/10, 2)  # 0.5-2.5 arası
    voteCHP = round(25 + randrange(10), 2)      # 25-35 arası
    voteIYI = round(8 + randrange(8), 2)        # 8-16 arası
    voteDEVA = round(1 + randrange(4), 2)       # 1-5 arası
    voteGP = round(1 + randrange(3), 2)         # 1-4 arası
    voteSP = round(1 + randrange(3), 2)         # 1-4 arası
    voteDP = round(0.5 + randrange(15)/10, 2)   # 0.5-2 arası
    voteHDP = round(8 + randrange(6), 2)        # 8-14 arası
    voteTIP = round(1 + randrange(3), 2)        # 1-4 arası
    voteZP = round(1 + randrange(3), 2)         # 1-4 arası
    voteMP = round(1 + randrange(3), 2)         # 1-4 arası
    voteTDP = round(0.5 + randrange(15)/10, 2)  # 0.5-2 arası
    voteBTP = round(0.5 + randrange(15)/10, 2)  # 0.5-2 arası
    voteOTHER = round(1 + randrange(3), 2)      # 1-4 arası 

allV = voteAKP + voteMHP + voteBBP + voteYRP + voteCHP + voteIYI + voteDEVA + voteGP + voteSP + voteDP + voteHDP \
    + voteTIP + voteZP + voteMP + voteTDP + voteBTP + voteOTHER

if allV == 100:
    print("Normally")
else:
    xvot = 100/allV
    voteOTHER = round((voteOTHER*xvot)/15,2)
    voteAKP = round(voteAKP*xvot + voteOTHER,2)
    voteMHP = round(voteMHP*xvot + voteOTHER,2) 
    voteBBP = round(voteBBP*xvot + voteOTHER,2)
    voteYRP = round(voteYRP*xvot + voteOTHER,2)
    voteCHP = round(voteCHP*xvot + voteOTHER,2)
    voteIYI = round(voteIYI*xvot + voteOTHER,2)
    voteDEVA= round(voteDEVA*xvot + voteOTHER,2)
    voteGP = round(voteGP*xvot + voteOTHER,2)
    voteSP = round(voteSP*xvot + voteOTHER,2)
    voteDP = round(voteDP*xvot + voteOTHER,2)
    voteHDP = round(voteHDP*xvot + voteOTHER,2)
    voteTIP = round(voteTIP*xvot + voteOTHER,2)
    voteZP = round(voteZP*xvot + voteOTHER,2)
    voteMP = round(voteMP*xvot + voteOTHER,2)
    voteTDP = round(voteTDP*xvot + voteOTHER,2)
    voteBTP = round(voteBTP*xvot + voteOTHER,2)

ci = round(voteAKP + voteMHP + voteBBP + voteYRP,2)
mi = round(voteCHP + voteIYI + voteDEVA + voteGP + voteSP + voteDP,2)
evoi = round(voteHDP + voteTIP,2)
atai = round(voteZP,2)
bgmsz = round(voteMP + voteTDP + voteBTP,2)

print(f"\nKullanılan Oy Sayısı: {voterPop:,}\n")

print(f"Cumhur İttifakı: %",ci ,\
      f"\n {myColors.Yellow}AKP %{myColors.ResetAll}",voteAKP,\
      f" {myColors.LightRed}BBP %{myColors.ResetAll}",voteBBP,\
      f"\n {myColors.Red}MHP %{myColors.ResetAll}",voteMHP,\
      f"  {myColors.DarkGray}YRP %{myColors.ResetAll}",voteYRP,\
      f"\n\nMillet İttifakı: %",mi,\
      f"\n {myColors.Red}CHP %{myColors.ResetAll}",voteCHP,\
      f" {myColors.Red}SP %{myColors.ResetAll}",voteSP,\
      f"\n {myColors.LightCyan}IYI %{myColors.ResetAll}",voteIYI,\
      f" {myColors.LightRed}DP %{myColors.ResetAll}",voteDP,\
      f"\n {myColors.Blue}DEVA %{myColors.ResetAll}",voteDEVA,\
      f" {myColors.LightGreen}GP %{myColors.ResetAll}",voteGP,\
      f"\n\nEmek ve Özgürlük İttifakı: %",evoi,\
      f"\n {myColors.LightMagenta}HDP{myColors.ResetAll}-{myColors.Green}YSP %{myColors.ResetAll}",voteHDP,\
      f" {myColors.Red}TIP %{myColors.ResetAll}",voteTIP,\
      f"\n\nATA İttifakı: %",atai,\
      f"\n {myColors.Black}ZP %{myColors.ResetAll}",voteZP,\
      f"\n\nBağımsız Partiler: %",bgmsz,\
      f"\n {myColors.LightBlue}MP %{myColors.ResetAll}",voteMP,\
      f" {myColors.Magenta}TDP %{myColors.ResetAll}",voteTDP,\
      f" {myColors.LightRed}BBP %{myColors.ResetAll}",voteBBP)

allV = voteAKP + voteMHP + voteBBP + voteYRP + voteCHP + voteIYI + voteDEVA + voteGP + voteSP + voteDP + voteHDP \
    + voteTIP + voteZP + voteMP + voteTDP + voteBTP + voteOTHER

Tp = round(100 - allV,2)

# Kabaca Milletvekili Hesabı


leftVm = bgmsz

cimv = round(ci*6)
mimv = round(mi*6)
evoimv = round(evoi*6)
ataimv = round(atai*3)

leftVm = (600 - (cimv + mimv + evoimv + ataimv))

# D'Hondt sistemi simulasyonu

mvkcount = int(voterPop/100)

cio = round(ci*mvkcount)
mio = round(mi*mvkcount)
evoio = round(evoi*mvkcount)
ataio = round(atai*mvkcount)

ciz = 2
miz = 2
evoz = 2
ataz = 2

cmv = 0
mmv = 0
atamv = 0
evomv = 0



for oy in range(600-leftVm):
    fndmax = max(cio,mio,evoio,ataio)
    if fndmax == cio:
        cio = cio*(ciz-1)
        cio = cio/ciz
        ciz += 1
        cmv += 1
    elif fndmax == mio: 
        mio = mio*(miz-1)
        mio = mio/miz 
        miz += 1 
        mmv += 1
    elif fndmax == evoio:
        evoio = evoio*(evoz-1) 
        evoio = evoio/evoz
        evoz += 1
        evomv += 1
    elif fndmax == ataio: 
        ataio = ataio*(ataz-1)
        ataio = ataio/ataz
        ataz += 1
        atamv += 1

print("-"*16)

print("Cumhur İttifakı Milletvekili Sayısı:",cmv ,\
      "\nMillet İttifakı Milletvekili Sayısı:",mmv,\
      "\nEmek ve Özgürlük İttifakı Milletvekili Sayısı:",evomv,\
      "\nATA İttifakı Milletvekili Sayısı:",atamv,\
      "\nBağımsız Partilerin Milletvekili Sayısı:",leftVm)

print("\n 3 April 2023")
print(f"💡 Tahmin modu: {'📊 Anket Ortalaması' if USE_POLL_PREDICTION else '🎲 Rastgele Değerler'}")
