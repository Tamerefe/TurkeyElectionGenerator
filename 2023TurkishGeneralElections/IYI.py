from random import randrange

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

akp = [31.1,35.1,38.4,29.1,32.7,28.1,34.2,31.8,36.7,27.5,30.8,35.4,31.0,31.0,38.5,29.1,33.3,34.0]
mhp = [6.9,7.7,7.0,7.1,6.3,6.3,6.9,6.1,7.6,7.1,7.1,5.9,7.2,6.5,10.1,5.4,6.5,6.6]
bbp = [0,0,0.9,0,0.1,1.6,0.4,0,0,0.8,0.2,0,0,0,0,0,1.0,0]
yrp = [1.3,1.6,1.0,1.5,0.7,1.2,1.3,1.1,0.8,1.4,2.2,2,1.3,1.9,1.6,1.0,1.4,1.3]
chp = [27.9,28.1,25.9,31.9,26.8,28.3,26.0,27.8,26.5,23.1,30.8,24.2,27.4,28.4,31.8,23.5,27.9,26.1]
iyi = [12.2,9.3,10.5,12.5,11.7,13.6,11.4,10.5,9.7,8.3,7.2,10.3,12.0,8.9,10.4,19.5,10.1,13.4]
deva = [0.5,0.3,2.1,0.9,2.0,2.1,0.6,1.3,2.4,2.1,0.6,0.7,1.4,1.5,0.9,2.3,1.4,1.6]
gp = [1.2,0.3,0.8,0.2,2.5,1.0,0.6,0.5,0,1.1,2.7,1.8,0.9,1.3,0.4,2.5,1.1,1.0]
sp = [1.0,0.3,0.9,0.9,0.7,0.9,0.8,0.6,0,1.1,0.4,0.3,1.4,0,0.6,0,0.7,0.8]
dp = [0.2,0,0.5,0,0,0.4,0,0,0,0,0,0,0,0,0,0,0.4,0]
hdp_ysp = [11.6,9.8,9.5,10.2,10.2,9.3,9.3,10.3,10.8,9.7,11.6,9.6,10.2,10.3,11.3,10.5,10.3,10.2]
tip = [1.0,3.3,0.7,1.6,1.6,1.5,1.4,0.3,1.9,3.1,0,1.9,1.5,1.191,0,0.4,1.6,0.9]
zp = [0.3,0.9,0.3,1.0,0.4,1.5,1.0,1.0,0,0.5,0,0.8,1.1,1.6,1.4,2.0,1.5,1.6]
mp = [3.2,3.6,5.2,1.6,5.5,2.3,1.0,3.0,4.7,2.3,3.1,4.6,1.6,2.2,1.1,1.3,3.5,1.5]
tdp = [0,0,0,0,0,1.3,0.1,0,0,0,1.1,0,0,0.9,0.1,1.8,0.8,0.9]
btp = [0.9,0.9,0,0,0.2,1.0,1.2,0,0,0,1.8,0,0,0,0,0,1.0,0]
other = [1.0,0.4,1.3,1.4,1.2,9.7,1.4,2.8,0.2,2.3,1.4,0.4,6.3,2.0,1.2,3.5,0.6,2.6]

population = 85279553

voterPop = int(population*75.27/100)

ci = 0
mi = 0
evoi = 0
atai = 0
allV = 0
bgmsz = 0

voteAKP = akp[randrange(18)] 
voteMHP = mhp[randrange(18)] 
voteBBP = bbp[randrange(18)] 
voteYRP = yrp[randrange(18)] 
voteCHP = chp[randrange(18)] 
voteIYI= iyi[randrange(18)] 
voteDEVA = deva[randrange(18)] 
voteGP = gp[randrange(18)] 
voteSP = sp[randrange(18)] 
voteDP = dp[randrange(18)] 
voteHDP = hdp_ysp[randrange(18)] 
voteTIP = tip[randrange(18)] 
voteZP = zp[randrange(18)] 
voteMP = mp[randrange(18)] 
voteTDP = tdp[randrange(18)] 
voteBTP = btp[randrange(18)] 
voteOTHER = other[randrange(18)] 

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
