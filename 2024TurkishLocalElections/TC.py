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

# Anket Sonuçları
     
  # Istanbul

akp = [31.1,35.1,38.4,29.1,32.7,28.1,34.2,31.8,36.7,27.5,30.8,35.4,31.0,31.0,38.5,29.1,33.3,34.0]
chp = [27.9,28.1,25.9,31.9,26.8,28.3,26.0,27.8,26.5,23.1,30.8,24.2,27.4,28.4,31.8,23.5,27.9,26.1]
iyi = [12.2,9.3,10.5,12.5,11.7,13.6,11.4,10.5,9.7,8.3,7.2,10.3,12.0,8.9,10.4,19.5,10.1,13.4]
dem = [11.6,9.8,9.5,10.2,10.2,9.3,9.3,10.3,10.8,9.7,11.6,9.6,10.2,10.3,11.3,10.5,10.3,10.2]   
other = [1.0,0.4,1.3,1.4,1.2,9.7,1.4,2.8,0.2,2.3,1.4,0.4,6.3,2.0,1.2,3.5,0.6,2.6]

  # Ankara
     
akp = [31.1,35.1,38.4,29.1,32.7,28.1,34.2,31.8,36.7,27.5,30.8,35.4,31.0,31.0,38.5,29.1,33.3,34.0]
chp = [27.9,28.1,25.9,31.9,26.8,28.3,26.0,27.8,26.5,23.1,30.8,24.2,27.4,28.4,31.8,23.5,27.9,26.1]
iyi = [12.2,9.3,10.5,12.5,11.7,13.6,11.4,10.5,9.7,8.3,7.2,10.3,12.0,8.9,10.4,19.5,10.1,13.4]
dem = [11.6,9.8,9.5,10.2,10.2,9.3,9.3,10.3,10.8,9.7,11.6,9.6,10.2,10.3,11.3,10.5,10.3,10.2]
other = [1.0,0.4,1.3,1.4,1.2,9.7,1.4,2.8,0.2,2.3,1.4,0.4,6.3,2.0,1.2,3.5,0.6,2.6]

  # Izmir

akp = [31.1,35.1,38.4,29.1,32.7,28.1,34.2,31.8,36.7,27.5,30.8,35.4,31.0,31.0,38.5,29.1,33.3,34.0]
chp = [27.9,28.1,25.9,31.9,26.8,28.3,26.0,27.8,26.5,23.1,30.8,24.2,27.4,28.4,31.8,23.5,27.9,26.1]
iyi = [12.2,9.3,10.5,12.5,11.7,13.6,11.4,10.5,9.7,8.3,7.2,10.3,12.0,8.9,10.4,19.5,10.1,13.4]
dem = [11.6,9.8,9.5,10.2,10.2,9.3,9.3,10.3,10.8,9.7,11.6,9.6,10.2,10.3,11.3,10.5,10.3,10.2]
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
voteCHP = chp[randrange(18)] 
voteIYI= iyi[randrange(18)] 
voteOTHER = other[randrange(18)] 

allV = voteAKP + voteCHP + voteIYI + voteOTHER

if allV == 100:
    print("Normally")
else:
    xvot = 100/allV
    voteOTHER = round((voteOTHER*xvot)/15,2)
    voteAKP = round(voteAKP*xvot + voteOTHER,2)
    voteCHP = round(voteCHP*xvot + voteOTHER,2)
    voteIYI = round(voteIYI*xvot + voteOTHER,2)

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

print("\n 13 February 2024")