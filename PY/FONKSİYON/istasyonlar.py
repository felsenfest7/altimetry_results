#Kütüphane
import pandas as pd

#Tüm TUDES istasyonlarının dataframe'inin oluşturulması için hazırlanan python file.
#İstasyonlar
iada = ["IADA", 41.88890424, 28.02351594]
istn = ["ISTN", 41.15984017, 29.07412648]
sile = ["SILE", 41.17636462, 29.60537553]
amsr = ["AMSR", 41.74398816, 32.39032924]
snop = ["SNOP", 42.02306816, 35.14945865]
trbz = ["TRBZ", 41.00197800, 39.74454939]
merg = ["MERG", 40.96896672, 27.96215236]
ylva = ["YLVA", 40.66197489, 29.27760959]
erdk = ["ERDK", 40.38988004, 27.84518123]
gada = ["GADA", 40.23171234, 25.89349329]
mnts = ["MNTS", 38.42960155, 26.72214568]
bdrm = ["BDRM", 37.03217553, 27.42345750]
aksa = ["AKSA", 36.84867631, 28.28226596]
antl = ["ANTL", 36.83042146, 30.60868263]
bzyz = ["BZYZ", 36.09619554, 32.94011772]
tscu = ["TSCU", 36.28146292, 33.83622766]
erdm = ["ERDM", 36.56372030, 34.25539255]
arsz = ["ARSZ", 36.41558863, 35.88519394]

#Tüm verilerin bir listeye aktarılması
liste = [iada, istn, sile, amsr, snop, trbz, merg, ylva, erdk, gada, mnts, bdrm, aksa, antl, bzyz, tscu, erdm, arsz]

#Dataframe oluşturulması
df = pd.DataFrame(liste, columns = ["Station", "Latitude", "Longitude"])

#Dataframe'in bir excel tablosuna aktarılması
tablo = df.to_excel("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/istasyonların_konumları.xlsx")

path2 = "/home/furkan/deus/gmt_calismalarim/gmt_icin2.txt"

with open(path2, 'w') as f:
    df_string = df.to_string(header=False, index=False)
    f.write(df_string)

#GMT İÇİN BOYLAM ENLEM ŞEKLİNDE YAZILMASI
def yer_degistir(liste):
    liste[1], liste[2] = liste[2], liste[1]
    return liste

iada2 = yer_degistir(iada)
istn2 = yer_degistir(istn)
sile2 = yer_degistir(sile)
amsr2 = yer_degistir(amsr)
snop2 = yer_degistir(snop)
trbz2 = yer_degistir(trbz)
merg2 = yer_degistir(merg)
ylva2 = yer_degistir(ylva)
erdk2 = yer_degistir(erdk)
gada2 = yer_degistir(gada)
mnts2 = yer_degistir(mnts)
bdrm2 = yer_degistir(bdrm)
aksa2 = yer_degistir(aksa)
antl2 = yer_degistir(antl)
bzyz2 = yer_degistir(bzyz)
tscu2 = yer_degistir(tscu)
erdm2 = yer_degistir(erdm)
arsz2 = yer_degistir(arsz)

#Tüm verilerin bir listeye aktarılması
liste2 = [iada2, istn2, sile2, amsr2, snop2, trbz2, merg2, ylva2, erdk2, gada2, mnts2, bdrm2, aksa2, antl2, bzyz2, tscu2, erdm2, arsz2]

#Dataframe oluşturulması
df2 = pd.DataFrame(liste2, columns = ["Station", "Longitude", "Latitude"])

#Dataframe'in bir excel tablosuna aktarılması
tablo2 = df2.to_excel("/home/furkan/deus/ALTIMETRY/processler/EXCELLER/istasyonların_konumları_boylam_enlem.xlsx")

#Text dosyasına atılması

path = "/home/furkan/deus/gmt_calismalarim/gmt_icin.txt"

with open(path, 'w') as f:
    df_string = df2.to_string(header=False, index=False)
    f.write(df_string)



#Bir daha
def yer_degistir2(liste):
    liste[0], liste[1] = liste[1], liste[0]
    liste[1], liste[2] = liste[2], liste[1]
    return liste

iada2 = yer_degistir2(iada)
istn2 = yer_degistir2(istn)
sile2 = yer_degistir2(sile)
amsr2 = yer_degistir2(amsr)
snop2 = yer_degistir2(snop)
trbz2 = yer_degistir2(trbz)
merg2 = yer_degistir2(merg)
ylva2 = yer_degistir2(ylva)
erdk2 = yer_degistir2(erdk)
gada2 = yer_degistir2(gada)
mnts2 = yer_degistir2(mnts)
bdrm2 = yer_degistir2(bdrm)
aksa2 = yer_degistir2(aksa)
antl2 = yer_degistir2(antl)
bzyz2 = yer_degistir2(bzyz)
tscu2 = yer_degistir2(tscu)
erdm2 = yer_degistir2(erdm)
arsz2 = yer_degistir2(arsz)

#Tüm verilerin bir listeye aktarılması
liste3 = [iada2, istn2, sile2, amsr2, snop2, trbz2, merg2, ylva2, erdk2, gada2, mnts2, bdrm2, aksa2, antl2, bzyz2, tscu2, erdm2, arsz2]

#Dataframe oluşturulması
df3 = pd.DataFrame(liste3, columns = ["Station", "Longitude", "Latitude"])

#Text dosyasına atılması

path = "/home/furkan/deus/gmt_calismalarim/gmt_icin3.txt"

with open(path, 'w') as f:
    df_string = df3.to_string(header=False, index=False)
    f.write(df_string)
