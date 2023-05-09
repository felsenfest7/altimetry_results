import pandas as pd
import numpy as np
import math as m
from numpy.linalg import inv

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")
import altimetry_functions as af
import plot_revize as pr

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
    bilinmeyenler = 6   #6 tane gelgit bilinmeyni var. b0, b1, Ak1, Bk1, Ak2, Bk2
    serbestlik_derecesi = bilinenler - bilinmeyenler

    varyans = PVV / serbestlik_derecesi  #metrekare
    stdv = m.sqrt(varyans)  #metre

    ##Varyans kovaryans matrisinin oluşturulması ve bilinmeyenlerin doğruluklarının hesaplanması
    varyans_kovaryans_matrisi = varyans * N_ters

    #Düzeltilmiş SSH verilerinin excele aktarılması ve plotta çizdirilmesi
    dateler = df[["cdate_t"]]
    corr_ssh = pd.DataFrame(l_artı_v, columns=['SSH'])

    dateler.reset_index(inplace = True)
    dateler.drop(columns=["ay"], inplace=True)

    df_merged = dateler.join(corr_ssh)  #Date ve CORR SSH değerlerinin tek dfte bulunduğu durum

    #Elde edilen df_merged'ün NaN boş aylarını interpole etmek
    df_merged = af.dates_interpolation(df_merged)

    #Ana ölçülerile birleştirilme
    df_merged = df_merged.join(l2)
    df_merged.rename(columns = {"SSH" : "SSH_model", "ssh_ales" : "SSH_ilk"}, inplace = True)
    df_merged = df_merged[["cdate_t", "SSH_ilk", "SSH_model"]] #SSH_ilk dengeleme öncesi, SSH_model dengeleme sonrası SSH değerleri

    # Değerlerin elde edilmesi (x ve Ell matrisinden)
    mss = x[0]                                      # Mean Sea Surface (m) biriminde ama array halinde
    mss = mss[0]                                    # Burada ise float halinde
    mss = mss.round(3)                              # metre
    mss_hata = varyans_kovaryans_matrisi[0][0]      # hata (m2 biriminde)
    mss_hata = m.sqrt(mss_hata) * 100               # cm biriminde mss hatası
    mss_hata = round(mss_hata, 1)                   # Yuvarlama işlemi (cm)

    trend = x[1]                                    # metre/ay biriminde
    trend = trend[0]                                # Burada ise float halinde
    trend = trend * 1000 * 12                       # yılda mm bazında değişim
    trend = trend.round(2)                          # mm/yıl
    trend_hata = varyans_kovaryans_matrisi[1][1]    # hata m2 biriminde
    trend_hata = m.sqrt(trend_hata) * 1000 * 12     # mm biriminde trend hatası
    trend_hata = round(trend_hata, 1)               # yuvarlama işlemi (mm)

    A1 = x[2]                                       # metre biriminde
    A1 = A1[0]                                      # Burada ise float halinde
    A1 = A1 * 100                                   # cm  biriminde
    A1 = abs(round(A1, 4))                          # Yuvarlama işlemi, sanırım abs değeri alınmalı !!!!!!!
    A1_hata = varyans_kovaryans_matrisi[2][2]       # Hata m2 biriminde
    A1_hata = m.sqrt(A1_hata)                       # m biriminde
    A1_hata = round(A1_hata * 100, 1)               #cm biriminde yuvarlanmış değer

    B1 = x[3]                                       # metre biriminde
    B1 = B1[0]                                      # Burada ise float halinde
    B1 = B1 * 100                                   # cm  biriminde
    B1 = abs(round(B1, 4))                          # Yuvarlama işlemi, sanırım abs değeri alınmalı !!!!!!!
    B1_hata = varyans_kovaryans_matrisi[3][3]       # Hata m2 biriminde
    B1_hata = m.sqrt(B1_hata)                       # m biriminde
    B1_hata = round(B1_hata * 100, 1)               # cm biriminde yuvarlanmış değer

    semi_annual_genlik = round(m.sqrt(A1**2 + B1**2), 2)      # cm biriminde
    semi_annual_faz = round(m.atan(B1 / A1), 2)

    A2 = x[4]                                       # metre biriminde
    A2 = A2[0]                                      # Burada ise float halinde
    A2 = A2 * 100                                   # cm  biriminde
    A2 = abs(round(A2, 4))                          # Yuvarlama işlemi, sanırım abs değeri alınmalı !!!!!!!
    A2_hata = varyans_kovaryans_matrisi[4][4]       # Hata m2 biriminde
    A2_hata = m.sqrt(A2_hata)                       # m biriminde
    A2_hata = round(A2_hata * 100, 1)               # cm biriminde yuvarlanmış değer

    B2 = x[5]                                       # metre biriminde
    B2 = B2[0]                                      # Burada ise float halinde
    B2 = B2 * 100                                   # cm  biriminde
    B2 = abs(round(B2, 4))                          # Yuvarlama işlemi, sanırım abs değeri alınmalı !!!!!!!
    B2_hata = varyans_kovaryans_matrisi[5][5]       # Hata m2 biriminde
    B2_hata = m.sqrt(B2_hata)                       # m biriminde
    B2_hata = round(B2_hata * 100, 1)               # cm biriminde yuvarlanmış değer

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

    #Plotun çizdirilmesi
    plot = pr.corr_ssh(df_merged, f"{title} SSH Modeli", mss, plota_trend)

    #En sonunda verileri excele atalım
    pr.excele_yolla(df_merged, name, mode)

































