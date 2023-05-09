from netCDF4 import Dataset as dt
import xarray as xr
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopy.distance
import juliandate as jd
#from datetime import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, MonthLocator, YearLocator
from matplotlib.ticker import FormatStrFormatter
import math as m
from numpy.linalg import inv
import matplotlib.dates as mdates
import datetime

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")

import xtrack_functions as xf
import xtrack_plot as xp
import plot_revize as pr

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',30)
pd.set_option('display.max_rows',500000)
#-----------------------------------------------------------------------------------------------------------------------
#ANTALYA
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.007.nc"
data = xr.open_dataset(lrm_data, decode_times = False)
df = data.to_dataframe()

df2 = df.reset_index()

df3 = df2.loc[:, ["lat", "lon", "mssh", "sla", "time"]]

#df3 = df2.dropna(0)
df3 = df3[(df3.lat > 36.80000) & (df3.lat < 36.81)]

df3 = df3.dropna(0)

df3["SSH"] = df3["mssh"] + df3["sla"]
df3 = df3.drop(columns = ["mssh", "sla"])

#1950 tarihli JD BC 4713'e kaymalı
df3["BC4713"] = df3["time"] + 2433282.50000
df3["DEUS"] = [jd.to_gregorian(i) for i in df3["BC4713"]]

df3["VULT"] = [list(i) for i in df3["DEUS"]]
df3["GOD"] = [i[0:3] for i in df3["VULT"]]

df3 = df3.drop(columns = ["time", "BC4713", "DEUS", "VULT"])
"""
path = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/ISTASYONLAR/ANTALYA/antalya.xlsx"
table = df3.to_excel(path)
"""
dff = pd.read_excel("/home/furkan/deus/ALTIMETRY/processler/XTRACK/ISTASYONLAR/ANTALYA/antalya.xlsx", index_col = 0)
dff = dff.drop(columns = ["GOD"])
dff.drop([121557,121778], axis=0, inplace=True)
dff["Tarih"] = pd.to_datetime(dff["Tarih"])

#Aylık veriler
dff.set_index("Tarih", inplace = True)
dff_aylık = dff.resample("MS").mean()

#IQR
def iqr_xtrack(df):

    Q1 = df["SSH"].quantile(0.25)
    Q3 = df["SSH"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df.query('(@Q1 - 1.5 * @IQR) <= SSH <= (@Q3 + 1.5 * @IQR)')

    return filtered

filtered = iqr_xtrack(dff_aylık)

#Ufak noiseların yok edilmesi gerekmekte
filtered = filtered[filtered["SSH"] < 25.75]
filtered = filtered[filtered["SSH"] > 25.45]

#DATES INTERPOLATION
def dates_interpolation_xtrack(df):
    """
        --> Aylara göre interpolasyon yapar.
        --> Sadece tarihler için geçerlidir.

        input: df
        output: df
    """
    df.reset_index(inplace = True)

    df['Tarih'] = pd.to_datetime(df['Tarih'])

    df = (df.set_index('Tarih')
          .reindex(pd.date_range(df['Tarih'].min(), df['Tarih'].max(), freq='MS'))
          .rename_axis(['Tarih'])
          .fillna(np.nan))   #0 dı bu

    return df

filtered = dates_interpolation_xtrack(filtered)

#Plot1
def plot_xtrack(df1, title, tarih):

    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff1 = df1

    dff1.reset_index(inplace = True)

    dff1 = dff1[dff1["SSH"].notna()]

    dff1 = dff1[dff1["Tarih"] > tarih]

    # Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    ax.plot_date(dff1["Tarih"], dff1["SSH"], "#27aeef", label="XTRACK Verileri")

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=12))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()

#plot = plot_xtrack(filtered, "Antalya X-TRACK Verileri", "1980-08-01")

def df2newdf_xtrack(df, station_date, end_date):

    """
        --> İçine atılan df'in columnlarının yalnızca bir kısmının kullanılması için oluşturulan dataframe.
        --> Ekstra bir hesap yaparak yeni bir columnda oluşturmayı hedeflemiştir.

        input: df
        output: df
    """

    df2 = df.reset_index()
    df3 = df2[["Tarih", "SSH"]].copy()

    # YYYY.MM biriminde hesaplamaya yapabilmek için yapılan hesaplamalar
    new_date = []
    for i in df3["Tarih"]:
        new_date.append(i.year + ((i.month - 0.5) / 12))

    # Elde edilen değerlerin virgülden sonra çok hanesi olduğu için formatlanması gerekmekte
    formatting = ["%.4f" % i for i in new_date]

    # Elde edilen listenin df'e eklenmesi
    df3["date"] = formatting

    # Eski cdate_t columnu burada elimine edilerek yeni elde edilen column index olarak atandı
    #df3 = df3.drop(["cdate_t"], axis=1)
    df3 = df3[df3["Tarih"] > station_date]
    df3 = df3[df3["Tarih"] < end_date]
    df3.set_index("date", inplace=True)

    # SSH columnunun isminin değiştirilmesi (ileride karşılaştırma yaparken işe yarar diye)
    df3.rename(columns={"SSH": "ssh_ales"}, inplace=True)

    # Ağırlık column'unun oluşturulması
    df3["weight"] = 1

    df3.reset_index(inplace=True)
    df3.rename_axis("ay", inplace=True)

    return df3

#nx3'lük matrisin oluşturulması
wish = df2newdf_xtrack(filtered, "1998-09-01", "2017-11-01")

def corr_ssh_plot(df, title, mss, trend):
    """
        --> Dengelenmiş SSH değerlerinin çizdirilmesi için.
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = df

    # Nan değerlerinin alınmaması
    dff = dff[dff["SSH_ilk"].notna()]
    dff = dff[dff["SSH_model"].notna()]

    dff.reset_index(inplace = True)
    # Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff["Tarih"], dff["SSH_ilk"], "#FFBF00", label="SSH Ölçü")
    ax.plot_date(dff["Tarih"], dff["SSH_model"], "#0d88e6", label="SSH Model")

    ax.axhline(y = mss, c = "red", label = "MSS")
    plt.text(datetime.date(2016, 2, 1), 25.74, trend, fontsize=10)

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=12))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_xlabel("Tarih (Yıl)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="upper left")
    plt.grid(True)
    plt.title(title)
    plt.show()

def harmonik_analiz2(df, title, name, mode):

    l2 = df[["ssh_ales"]]  # en sonda kullanmak için aldım

    #NaN olan verilerin droplanması
    df.dropna(inplace = True)

    # FONKSİYONEL MODEL
    # Ağırlık matrisinin oluşturulması (numpy array şeklinde)
    boyut = df.shape[0]
    P = np.diag(np.full(boyut, 1))

    # l matrisinin çekilmesi ve numpy arrayine döndürülmesi
    l = df[["ssh_ales"]]
    l = l.to_numpy()

    #A matrisinin oluşturulması için yapılan işlemler
    ##İşlemler
    df2 = df.copy()
    df2.drop(columns = ["date", "weight"], inplace = True)  #gereksiz columnlar droplandı
    df2.reset_index(inplace = True)     #index sıfırlandı
    df2.rename_axis("index", inplace = True)    #indexi isimlendirme
    df2.rename(columns={"ay": "delta_t"}, inplace=True)     #zaman farklarını delta_t olarak isimlendirdim

    ##Katsayıların hesapları
    df2["Ak1"] = df2.apply(lambda df: m.cos((2 * m.pi * df["delta_t"])/6), axis=1)
    df2["Bk1"] = df2.apply(lambda df: m.sin((2 * m.pi * df["delta_t"])/6), axis=1)

    df2["Ak2"] = df2.apply(lambda df: m.cos((2 * m.pi * df["delta_t"])/12), axis=1)
    df2["Bk2"] = df2.apply(lambda df: m.sin((2 * m.pi * df["delta_t"])/12), axis=1)

    df2["b0_katsayı"] = 1

    ##l matrisini de çekmek lazım
    l = df2[["ssh_ales"]]

    ##Şimdi A katsayı matrisi biçiminde referanslamak için yeni bir dataframee aktararak referanslandırcam
    df3 = df2.copy()
    df3.drop(columns = ["ssh_ales"], inplace = True)    #l matrisini dropluyoruz buradan
    df3 = df3[["b0_katsayı", "delta_t", "Ak1", "Bk1", "Ak2", "Bk2"]]    #orderı düzeltiyorum

    A = df3.to_numpy()  #A matrisi
    l = l.to_numpy()    #l matrisi
    A_transpose = np.transpose(A)   #A transpose matrisi
    N = np.matmul(np.matmul(A_transpose, P), A)     #N matrisi, birimsiz
    n = np.matmul(np.matmul(A_transpose, P), l)     #n matrisi, metre biriminde
    N_ters = inv(N)     #ters N matrisi
    x = np.matmul(N_ters, n)    #x matrisi, metre biriminde

    #Düzeltme denklemlerinin hesabı
    ## v = Ax - l olarak ifade edilir. l matrisi zaten SSH ölçmeleri
    Ax = np.matmul(A, x)
    v = Ax - l  #metre biriminde

    ##Dengelemenin kontrolünün sağlanması
    l_artı_v = l + v    #ölçü + düzeltmesi

    ##Dengelemenin sağlanmasında l+v = Ax kontrolü yapılmalı. Ölçülerde virgülden sonra hata gelebileceği için
    ##milimetre mertebesinde bu kontrolü sağlayacağım.

    l_artı_v_v2 = np.round(l_artı_v, 3)
    Ax_v2 = np.round(Ax, 3)

    ##Dengelemenin kontrolü
    if np.array_equal(l_artı_v_v2, Ax_v2) == True:
        print("Dengeleme doğru !")
    else:
        print("Error 404 !")

    #Stokastik modelin oluşturulması
    v_transpose = np.transpose(v)   #v'nin transposesi
    PVV = np.matmul(np.matmul(v_transpose, P), v)   #metrekare biriminde bir deper döndürdü

    ##Bilinenler, bilinmeyenler ve serbestlik derecesi
    ##Aslında bu önceden belirlenmeliydi fakat ölçü sayısı zaten bilinmeyenlerden fazla gelecek kendi ölçülerimde
    bilinenler = boyut
    bilinmeyenler = 6   #6 tane gelgit bilinmeyni var. b0, b1, Ak1, Bk1, Ak2, Bk2
    serbestlik_derecesi = bilinenler - bilinmeyenler

    varyans = PVV / serbestlik_derecesi  #metrekare
    stdv = m.sqrt(varyans)  #metre

    ##Varyans kovaryans matrisinin oluşturulması ve bilinmeyenlerin doğruluklarının hesaplanması
    varyans_kovaryans_matrisi = varyans * N_ters

    #Düzeltilmiş SSH verilerinin excele aktarılması ve plotta çizdirilmesi
    dateler = df[["Tarih"]]
    corr_ssh = pd.DataFrame(l_artı_v, columns=['SSH'])

    dateler.reset_index(inplace = True)
    dateler.drop(columns=["ay"], inplace=True)

    df_merged = dateler.join(corr_ssh)  #Date ve CORR SSH değerlerinin tek dfte bulunduğu durum

    # Elde edilen df_merged'ün NaN boş aylarını interpole etmek
    df_merged = dates_interpolation_xtrack(df_merged)
    df_merged.drop(columns=["index"], inplace=True)
    df_merged.reset_index(inplace = True)

    # Ana ölçülerile birleştirilme
    df_merged = df_merged.join(l2)

    df_merged.rename(columns={"SSH": "SSH_model", "ssh_ales": "SSH_ilk"}, inplace=True)
    df_merged = df_merged[["Tarih", "SSH_ilk", "SSH_model"]]  # SSH_ilk dengeleme öncesi, SSH_model dengeleme sonrası SSH değerleri

    # Değerlerin elde edilmesi (x ve Ell matrisinden)
    mss = x[0]  # Mean Sea Surface (m) biriminde ama array halinde
    mss = mss[0]  # Burada ise float halinde
    mss = mss.round(3)  # metre
    mss_hata = varyans_kovaryans_matrisi[0][0]  # hata (m2 biriminde)
    mss_hata = m.sqrt(mss_hata) * 100  # cm biriminde mss hatası
    mss_hata = round(mss_hata, 1)  # Yuvarlama işlemi (cm)

    trend = x[1]  # metre/ay biriminde
    trend = trend[0]  # Burada ise float halinde
    trend = trend * 1000 * 12  # yılda mm bazında değişim
    trend = trend.round(1)  # mm/yıl
    trend_hata = varyans_kovaryans_matrisi[1][1]  # hata m2 biriminde
    trend_hata = m.sqrt(trend_hata) * 1000 * 12  # mm biriminde trend hatası
    trend_hata = round(trend_hata, 1)  # yuvarlama işlemi (mm)

    A1 = x[2]  # metre biriminde
    A1 = A1[0]  # Burada ise float halinde
    A1 = A1 * 100  # cm  biriminde
    A1 = abs(round(A1, 4))  # Yuvarlama işlemi, sanırım abs değeri alınmalı !!!!!!!
    A1_hata = varyans_kovaryans_matrisi[2][2]  # Hata m2 biriminde
    A1_hata = m.sqrt(A1_hata)  # m biriminde
    A1_hata = round(A1_hata * 100, 1)  # cm biriminde yuvarlanmış değer

    B1 = x[3]  # metre biriminde
    B1 = B1[0]  # Burada ise float halinde
    B1 = B1 * 100  # cm  biriminde
    B1 = abs(round(B1, 4))  # Yuvarlama işlemi, sanırım abs değeri alınmalı !!!!!!!
    B1_hata = varyans_kovaryans_matrisi[3][3]  # Hata m2 biriminde
    B1_hata = m.sqrt(B1_hata)  # m biriminde
    B1_hata = round(B1_hata * 100, 1)  # cm biriminde yuvarlanmış değer

    semi_annual_genlik = round(m.sqrt(A1 ** 2 + B1 ** 2), 2)  # cm biriminde
    semi_annual_faz = round(m.atan(B1 / A1), 2)

    A2 = x[4]  # metre biriminde
    A2 = A2[0]  # Burada ise float halinde
    A2 = A2 * 100  # cm  biriminde
    A2 = abs(round(A2, 4))  # Yuvarlama işlemi, sanırım abs değeri alınmalı !!!!!!!
    A2_hata = varyans_kovaryans_matrisi[4][4]  # Hata m2 biriminde
    A2_hata = m.sqrt(A2_hata)  # m biriminde
    A2_hata = round(A2_hata * 100, 1)  # cm biriminde yuvarlanmış değer

    B2 = x[5]  # metre biriminde
    B2 = B2[0]  # Burada ise float halinde
    B2 = B2 * 100  # cm  biriminde
    B2 = abs(round(B2, 4))  # Yuvarlama işlemi, sanırım abs değeri alınmalı !!!!!!!
    B2_hata = varyans_kovaryans_matrisi[5][5]  # Hata m2 biriminde
    B2_hata = m.sqrt(B2_hata)  # m biriminde
    B2_hata = round(B2_hata * 100, 1)  # cm biriminde yuvarlanmış değer

    annual_genlik = round(m.sqrt(A2 ** 2 + B2 ** 2), 2)  # cm biriminde
    annual_faz = round(m.atan(B2 / A2), 2)

    print("--------------------------------------------------------------------------")
    print(f"MSS ve hatası: {mss} m ± {mss_hata} cm")
    print(f"Trend ve hatası: {trend} ± {trend_hata} mm/yıl")
    print(f"Ak1 ve hatası: {A1} ± {A1_hata} cm")
    print(f"Bk1 ve hatası: {B1} ± {B1_hata} cm")
    print(f"Ak2 ve hatası: {A2} ± {A2_hata} cm")
    print(f"Bk2 ve hatası: {B2} ± {B2_hata} cm")
    print(f"Semi-annual Genlik ve Faz: {semi_annual_genlik} cm - {semi_annual_faz}")
    print(f"Annual Genlik ve Faz: {annual_genlik} cm - {annual_faz}")
    print("--------------------------------------------------------------------------")

    plota_trend = f"Trend: {trend} ± {trend_hata} mm/yıl"

    # Plotun çizdirilmesi
    plot = corr_ssh_plot(df_merged, f"{title} SSH Modeli", mss, plota_trend)

    # En sonunda verileri excele atalım
    pr.excele_yolla(df_merged, name, mode)



haa = harmonik_analiz2(wish, "Antalya X-TRACK", "antalya", "xtrack")








