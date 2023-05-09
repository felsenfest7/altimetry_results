from netCDF4 import Dataset as dt
import xarray as xr
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopy.distance
import juliandate as jd
from datetime import datetime
import math as m

#-----------------------------------------------------------------------------------------------------------------------
def read_xtrack(data, ist_enlem, ist_boylam, delta):

    """
        --> XTRACK verilerinin okunması için oluşturulmuş fonksiyon.

        input: data olarak xtrack verisi, ist_enlem ve ist_boylam ise istasyonun koordinatlarıdır
        oytput: dataframe
    """

    #Dataset xarray kütüphanesi ile açılır
    dataset = xr.open_dataset(data, decode_times = False)

    #Ardından dataframe'e dönüştürülür
    df = dataset.to_dataframe()

    #Ardından yeni bir dataframe oluşturulur ve multiindex yapıdaki veri resetlenerek single index yapılır
    df2 = df.reset_index()

    #input olarak girilen istasyon koordinatları yardımıyla her row için koordinatların hesaplanması
    ist_koord = (ist_enlem, ist_boylam)
    df2["distance2coast"] = df2.apply(lambda row: geopy.distance.distance((row["lat"], row["lon"]), ist_koord).km, axis=1)

    #İstasyona minimum uzaklıkların hesabı
    #df2["distance2coast"] = df2[["distance2coast"]].min(axis=1).min()

    """
    #Burayı kodlayamadım nedense, elle devam edecem
    if df2["lat"].mean() < ist_enlem:
        df2 = df2[(df2.lat > (ist_enlem - delta)) & (df2.lat < (ist_enlem))]
    elif df2["lat"].mean() > ist_enlem:
        df2 = df2[(df2.lat > (ist_enlem)) & (df2.lat < (ist_enlem + delta))]
    """

    if df2["lat"].mean() < ist_enlem:
        df2 = df2[(df2.lat > (ist_enlem - delta)) & (df2.lat < (ist_enlem))]
    elif df2["lat"].mean() > ist_enlem:
        df2 = df2[(df2.lat > (ist_enlem)) & (df2.lat < (ist_enlem + delta))]

    #Nan değerlerin elimine edilmesi --> julian date çevirimleri yaparken sıkıntıya sebebiyet veriuor çünkü
    df2 = df2.dropna(0)

    #Jülyen tarihlerini grogaryan tarihine çevirme
    ##XTRACK verileri "days since 1950-1-1" olarak tanımlanmakta ve bu tarih 2433282.50000 Jülyen tarihine gelmekte (MÖ 4713'e göre)
    # Elimdeki julian günlerini bu date ile toplarsam aslında epok kaydırma yapmış olurum, bu sayede BC 4713'e göre tarih bulurum.
    # Ardından yeni epokları gregoryana çevirebilirim
    jday4713 = [i + 2433282.50000 for i in df2["time"]]
    df2.insert(loc = 22, column="jday4713", value = jday4713)

    # Calendar date'e çevirme
    cdate = [jd.to_gregorian(i) for i in df2["jday4713"]]
    df2.insert(loc = 23, column= "cdate", value = cdate)

    # Datetime'a çevirme
    cdate_2 = []

    for i in cdate:
        dt_obj = datetime(*i)
        x = dt_obj.strftime("%Y-%m-%d")
        cdate_2.append(x)
    df2.insert(loc=24, column="cdate_t", value=cdate_2)

    #Pandasta çalışması için şu komut girilmeli
    df2["cdate_t"] = pd.to_datetime(df2["cdate_t"])

    #İlk olarak SSH değerleri ham veride hesaplanacak
    df2["ssh"] = df2["mssh"] + df2["sla"]

    return df2
#-----------------------------------------------------------------------------------------------------------------------
def aylik(df):

    """
        --> Günlük olarak elde edilen XTRACK verilerinin aylık hale getirilmeis için kullanılmaktadır.

        input: dataframe
        output: dataframe
    """

    #Bazı columnları droplayacam burada
    df.drop(["cycles_numbers", "cycle", "jday4713"], axis = 1, inplace = True)

    #Gerekli işlemler ardından
    df = df.sort_values(by="cdate_t", ascending=True)
    df.set_index("cdate_t", inplace = True)
    df_aylık = df.resample("MS").mean()
    return df_aylık
#-----------------------------------------------------------------------------------------------------------------------

def iqr_xtrack(df):

    Q1 = df["ssh"].quantile(0.25)
    Q3 = df["ssh"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df.query('(@Q1 - 1.5 * @IQR) <= ssh <= (@Q3 + 1.5 * @IQR)')

    return filtered
#-----------------------------------------------------------------------------------------------------------------------
def dates_interpolation_xtrack(df):
    """
        --> Aylara göre interpolasyon yapar.
        --> Sadece tarihler için geçerlidir.

        input: df
        output: df
    """
    df.reset_index(inplace = True)

    df['cdate_t'] = pd.to_datetime(df['cdate_t'])

    df = (df.set_index('cdate_t')
          .reindex(pd.date_range(df['cdate_t'].min(), df['cdate_t'].max(), freq='MS'))
          .rename_axis(['cdate_t'])
          .fillna(np.nan))   #0 dı bu

    return df
#-----------------------------------------------------------------------------------------------------------------------
def df2newdf_xtrack(df, station_date, end_date):

    """
        --> İçine atılan df'in columnlarının yalnızca bir kısmının kullanılması için oluşturulan dataframe.
        --> Ekstra bir hesap yaparak yeni bir columnda oluşturmayı hedeflemiştir.

        input: df
        output: df
    """

    df2 = df.reset_index()
    df3 = df2[["cdate_t", "ssh"]].copy()

    # YYYY.MM biriminde hesaplamaya yapabilmek için yapılan hesaplamalar
    new_date = []
    for i in df3["cdate_t"]:
        new_date.append(i.year + ((i.month - 0.5) / 12))

    # Elde edilen değerlerin virgülden sonra çok hanesi olduğu için formatlanması gerekmekte
    formatting = ["%.4f" % i for i in new_date]

    # Elde edilen listenin df'e eklenmesi
    df3["date"] = formatting

    # Eski cdate_t columnu burada elimine edilerek yeni elde edilen column index olarak atandı
    #df3 = df3.drop(["cdate_t"], axis=1)
    df3 = df3[df3["cdate_t"] > station_date]
    df3 = df3[df3["cdate_t"] < end_date]
    df3.set_index("date", inplace=True)

    # SSH columnunun isminin değiştirilmesi (ileride karşılaştırma yaparken işe yarar diye)
    df3.rename(columns={"ssh": "ssh_ales"}, inplace=True)

    # Ağırlık column'unun oluşturulması
    df3["weight"] = 1

    df3.reset_index(inplace=True)
    df3.rename_axis("ay", inplace=True)

    return df3
#-----------------------------------------------------------------------------------------------------------------------
def df2excel_xtrack(df, mode, station_name, station_name_mode):

    """
        --> Herhangi bir dataframe'in excele çevrilmesini sağlar.
        --> Mod ve station name bilgileri verinin pathi için gereklidir.

        input: df
        output: excel table
    """

    path = f"/home/furkan/deus/ALTIMETRY/processler/{mode}/ISTASYONLAR/{station_name}/{station_name_mode}.xlsx"
    table = df.to_excel(path)
    return table











