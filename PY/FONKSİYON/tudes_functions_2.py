import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
from numpy.linalg import inv
from matplotlib.ticker import FormatStrFormatter
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, MonthLocator, YearLocator
import sys
import datetime
pd.options.mode.chained_assignment = None  # default='warn'
np.set_printoptions(threshold=sys.maxsize)
#----------------------------------------------------------------------------------------------------------------------
def excele_yolla(df, station_name, mode):

    path = f"/home/furkan/deus/ALTIMETRY/processler/SONUÇLAR/SPEKTRAL_ANALİZ/TUDES/TUDES_EXCELLER/{station_name}_{mode}_ssh_model.xlsx"
    df.to_excel(path)
#----------------------------------------------------------------------------------------------------------------------
def dates_interpolation(df):
    """
        --> Aylara göre interpolasyon yapar.
        --> Sadece tarihler için geçerlidir.

        input: df
        output: df
    """
    df['Tarih'] = pd.to_datetime(df['Tarih'])

    df = (df.set_index('Tarih')
          .reindex(pd.date_range(df['Tarih'].min(), df['Tarih'].max(), freq='MS'))
          .rename_axis(['Tarih'])
          .fillna(np.nan)   #0 dı bu
          .reset_index())

    return df
#----------------------------------------------------------------------------------------------------------------------
def corr_ssh_plot(df, title, mss, trend):
    """
        --> Dengelenmiş SSH değerlerinin çizdirilmesi için.
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = df

    # Nan değerlerinin alınmaması
    dff = dff[dff["SSH_ilk"].notna()]
    dff = dff[dff["SSH_model"].notna()]

    # Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff["Tarih"], dff["SSH_ilk"], "#FFBF00", label="SSH Ölçü")
    ax.plot_date(dff["Tarih"], dff["SSH_model"], "#0d88e6", label="SSH Model")

    ax.axhline(y = mss, c = "red", label = "Ortalama Deniz Yüzeyi")
    plt.text(datetime.date(2018, 11, 1), 0.58, trend, fontsize=10)

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=12))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="upper left")
    plt.grid(True)
    plt.title(title)
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def iqr(df):
    """
        --> IQR hesabı yapar, outlierlar elimine edilir.
        input: df
        output: df
    """
    Q1 = df["Deniz_Seviyesi"].quantile(0.25)
    Q3 = df["Deniz_Seviyesi"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df.query('(@Q1 - 1.5 * @IQR) <= Deniz_Seviyesi <= (@Q3 + 1.5 * @IQR)')

    return filtered
#-----------------------------------------------------------------------------------------------------------------------
def tudes_oku(path):
    """
        --> TUDES verilerinin okunması sağlar.
        --> Saatlik veriler için uyguladım bunu

        input : text'in pathi
        output:
    """
    #Verinin df ile okunması
    df = pd.read_csv(path, sep = ",")

    #Bu veride gerekli olan columnları almak için
    df2 = df[["Tarih", "Deniz Seviyesi", "Deniz Seviyesi Kalite Kodu"]]
    df2.rename(columns = {"Deniz Seviyesi": "Deniz_Seviyesi", "Deniz Seviyesi Kalite Kodu": "Kalite"}, inplace = True)

    #Deniz Seviyesi Kalite Kodu 0 veya 1 olabiliyor. Eğer 0'sa kalitesiz, 1'se kaliteli veri demek.
    #Kalitesiz verileri ondan dolayı elimine etcem.
    #Kalitesiz verilerde zaten SSH verileri NaN biçiminde geliyor.
    condition = df2[df2["Kalite"] == 0].index
    df2.drop(condition, inplace = True)
    df2.drop(columns = ["Kalite"], inplace = True)  #Artık bunla işim kalmadı

    return df2
#-----------------------------------------------------------------------------------------------------------------------
def tudes_15dk_birlestir(frames):
    """
        --> 15 dk'lık verilerin okunması için fonksiyon.
        --> 15 dk'lık veriler birleştirilir bu sayede.
        --> EN sonunda günlük veriler elde edilir.

        input : list
        output: df
    """
    #Verileri birleştirip indexi sıfırladı
    result = pd.concat(frames)
    result.reset_index(inplace=True, drop=True)

    # Verilerin tarih bilgilerinin düzeltilmesi ve IQR hesabının yapılarak birleştirilmiş 15dklık verilerin elde edilmesi
    result['Tarih'] = pd.to_datetime(result['Tarih'], format='%d.%m.%Y %H:%M:%S')  # Datetime object oluşturdum
    result = iqr(result)

    #15dklık verilerden saatlik veriler elde edilmesi
    result = result.resample('H', on='Tarih', closed='right').mean().reset_index()
    result = iqr(result)

    #Günlük verilerin elde edilmesi
    result = result.groupby(pd.Grouper(freq='D', key='Tarih')).mean()
    result = iqr(result)

    result.reset_index(inplace=True)  # Index'i sıfırladım

    return result
#-----------------------------------------------------------------------------------------------------------------------
def tudes_60dk_birlestir(frames):
    """
        --> 60 dk'lık verilerin okunması için fonksiyon.
        --> 60 dk'lık veriler birleştirilir bu sayede.

        input : list
        output: df
    """

    result = pd.concat(frames)
    result.reset_index(inplace = True, drop = True)

    #Saatlik verilere IQR
    result['Tarih'] = pd.to_datetime(result['Tarih'], format='%d.%m.%Y %H:%M:%S')  # Datetime object oluşturdum
    result = iqr(result)

    # Günlük verilerin oluşturulması
    result = result.groupby(pd.Grouper(freq='D', key='Tarih')).mean()
    result = iqr(result)

    result.reset_index(inplace=True)  # Index'i sıfırladım

    return result
#-----------------------------------------------------------------------------------------------------------------------
def birlestir_1560(frames):
    """
        --> 15 ve 60dk'lık verilerin birleştirilmesi ve aylık verilerin türetilmesi için fonksiyon.

        input : list
        output: df
    """
    result = pd.concat(frames)
    result.reset_index(inplace=True, drop=True)

    # Aylık verilerin oluşturulması
    result_aylik = result.resample("MS", on="Tarih").mean()  # Tarih bilgisi yine indexte
    result_aylik = iqr(result_aylik)
    result_aylik.reset_index(inplace=True)  # Indexten aldım

    return result_aylik
#-----------------------------------------------------------------------------------------------------------------------
def harmonik_analiz_tudes(df, title, name, mode):

    l2 = df[["Deniz_Seviyesi"]]  # en sonda kullanmak için aldım, orijinal ölçüler
    # NaN olan verilerin droplanması
    df.dropna(inplace=True)

    #Ay bilgileri gelsin diye bir reset atalım indexe
    #Bunun nedeni şu an orijinal index 0. ölçüden son ölçüye giden değerler (ay biriminde)
    #Buna ihtiyacım var dengelemede
    df.reset_index(inplace = True)
    df.rename(columns = {"index" : "ay"}, inplace = True)

    # FONKSİYONEL MODEL
    # Ağırlık matrisinin oluşturulması (numpy array şeklinde)
    boyut = df.shape[0]
    P = np.diag(np.full(boyut, 1))

    # l matrisinin çekilmesi ve numpy arrayine döndürülmesi
    l = df[["Deniz_Seviyesi"]]
    l = l.to_numpy()

    # A matrisinin oluşturulması için yapılan işlemler
    ##İşlemler
    df2 = df.copy()
    df2.rename_axis("index", inplace=True)  # indexi isimlendirme
    df2.rename(columns={"ay": "delta_t"}, inplace=True)  # zaman farklarını delta_t olarak isimlendirdim

    ##Katsayıların hesapları
    df2["Ak1"] = df2.apply(lambda df: m.cos((2 * m.pi * df["delta_t"]) / 6), axis=1)
    df2["Bk1"] = df2.apply(lambda df: m.sin((2 * m.pi * df["delta_t"]) / 6), axis=1)

    df2["Ak2"] = df2.apply(lambda df: m.cos((2 * m.pi * df["delta_t"]) / 12), axis=1)
    df2["Bk2"] = df2.apply(lambda df: m.sin((2 * m.pi * df["delta_t"]) / 12), axis=1)

    df2["b0_katsayı"] = 1

    ##Şimdi A katsayı matrisi biçiminde referanslamak için yeni bir dataframee aktararak referanslandırcam
    df3 = df2.copy()
    df3.drop(columns=["Deniz_Seviyesi"], inplace=True)  # l matrisini dropluyoruz buradan
    df3 = df3[["b0_katsayı", "delta_t", "Ak1", "Bk1", "Ak2", "Bk2"]]  # orderı düzeltiyorum

    A = df3.to_numpy()  # A matrisi
    A_transpose = np.transpose(A)  # A transpose matrisi
    N = np.matmul(np.matmul(A_transpose, P), A)  # N matrisi, birimsiz
    n = np.matmul(np.matmul(A_transpose, P), l)  # n matrisi, metre biriminde
    N_ters = inv(N)  # ters N matrisi
    x = np.matmul(N_ters, n)  # x matrisi, metre biriminde

    # Düzeltme denklemlerinin hesabı
    ## v = Ax - l olarak ifade edilir. l matrisi zaten SSH ölçmeleri
    Ax = np.matmul(A, x)
    v = Ax - l  # metre biriminde

    ##Dengelemenin kontrolünün sağlanması
    l_artı_v = l + v  # ölçü + düzeltmesi

    ##Dengelemenin sağlanmasında l+v = Ax kontrolü yapılmalı. Ölçülerde virgülden sonra hata gelebileceği için
    ##milimetre mertebesinde bu kontrolü sağlayacağım.

    l_artı_v_v2 = np.round(l_artı_v, 3)
    Ax_v2 = np.round(Ax, 3)

    ##Dengelemenin kontrolü
    if np.array_equal(l_artı_v_v2, Ax_v2) == True:
        print("--------------------------------------------------------------------------")
        print("Dengeleme doğru !")
    else:
        print("Error 404 !")

    #Stokastik modelin oluşturulması
    v_transpose = np.transpose(v)   #v'nin transposesi
    PVV = np.matmul(np.matmul(v_transpose, P), v)   #metrekare biriminde bir deper döndürdü

    ##Bilinenler, bilinmeyenler ve serbestlik derecesi
    ##Aslında bu önceden belirlenmeliydi fakat ölçü sayısı zaten bilinmeyenlerden fazla gelecek kendi ölçülerimde
    bilinenler = boyut
    bilinmeyenler = 6  # 6 tane gelgit bilinmeyni var. b0, b1, Ak1, Bk1, Ak2, Bk2
    serbestlik_derecesi = bilinenler - bilinmeyenler

    varyans = PVV / serbestlik_derecesi  # metrekare
    stdv = m.sqrt(varyans)  # metre

    ##Varyans kovaryans matrisinin oluşturulması ve bilinmeyenlerin doğruluklarının hesaplanması
    varyans_kovaryans_matrisi = varyans * N_ters

    # Düzeltilmiş SSH verilerinin excele aktarılması ve plotta çizdirilmesi
    dateler = df[["Tarih"]]
    corr_ssh = pd.DataFrame(l_artı_v, columns=['Deniz_Seviyesi_Model'])
    df_mergele = dateler.join(corr_ssh)

    # Elde edilen df_merged'ün NaN boş aylarını interpole etmek
    df_mergedle2 = dates_interpolation(df_mergele)

    # Ana ölçülerile birleştirilme
    df_mergedle3 = df_mergedle2.join(l2)
    df_mergedle3.rename(columns={"Deniz_Seviyesi_Model": "SSH_model", "Deniz_Seviyesi": "SSH_ilk"}, inplace=True)
    df_mergedle3 = df_mergedle3[["Tarih", "SSH_ilk", "SSH_model"]]  # SSH_ilk dengeleme öncesi, SSH_model dengeleme sonrası SSH değerleri

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
    plot = corr_ssh_plot(df_mergedle3, f"{title} SSH Modeli", mss, plota_trend)

    # En sonunda verileri excele atalım
    excele_yolla(df_mergedle3, name, mode)















































