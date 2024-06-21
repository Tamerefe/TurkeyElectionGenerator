from random import randrange
import datas

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

voteAKP = datas.akp[randrange(18)] 
voteMHP = datas.mhp[randrange(18)] 
voteBBP = datas.bbp[randrange(18)] 
voteYRP = datas.yrp[randrange(18)] 
voteCHP = datas.chp[randrange(18)] 
voteIYI= datas.iyi[randrange(18)] 
voteDEVA = datas.deva[randrange(18)] 
voteGP = datas.gp[randrange(18)] 
voteSP = datas.sp[randrange(18)] 
voteDP = datas.dp[randrange(18)] 
voteHDP = datas.hdp_ysp[randrange(18)] 
voteTIP = datas.tip[randrange(18)] 
voteZP = datas.zp[randrange(18)] 
voteMP = datas.mp[randrange(18)] 
voteTDP = datas.tdp[randrange(18)] 
voteBTP = datas.btp[randrange(18)] 
voteOTHER = datas.other[randrange(18)] 

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
