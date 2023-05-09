import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from netCDF4 import Dataset as dt
import glob
import xarray as xr
import pandas as pd
import cartopy as ca
import os
import juliandate as jd
from datetime import datetime
import math as m
from dateutil.relativedelta import relativedelta
import openpyxl
import geopy.distance
import mpu
from typing import Tuple
import verticapy as vp

#-----------------------------------------------------------------------------------------------------------------------
def merge_nc(files):
    """
        --> Bu fonksiyonun ana amacı indirilen nc dosyalarının path'inin fonksiyona girdi olarak girilmesidir.
        --> Ardından pathteki dosyalar sıralanarak ilk olarak xarray kütüphanesinin datasetine aktarılır.
        --> Ardından da hepsi dataframe olması için birer liste olur ve bunlar concat edilerek merge
    edilmiş bir dataframe elde edilir.
        --> Ardından BC 4713'e göre jday.00 değerleri düzenlenir. Bunun için yeni bir column'a bu değerler atanır.
        --> Ardından gregoryan tarihlerinin elde edilmesi için cdate adında yeni bir columnd oluşturulur ve jday
    tarihleri calendar date'e çevrilir.
        --> Fakat elde edilen "cdate" değerleri de tuple'lar içerisinde kalır. Bundan dolayı yeni bir liste
    oluşturulur ve yazılan for loopu ile "cdate_2" adı verilen ve sadece yıl-ay-gün bilgilerini içeren
    yeni bir liste elde edilir.
        --> Son olarak bu veriler dataframe'e aktarılarak sonuç ürün elde edilir.

        input: path
        output: dataframe
    """
    paths = sorted(glob.glob(files))
    datasets = [xr.open_dataset(p) for p in paths]
    dataframes = [p.to_dataframe() for p in datasets]
    dfs = pd.concat(dataframes)

    # Julian günü değişim
    # 1 Ocak 2000 12:00 UTM günü Julian günü olarak (4713 BC'e göre) 2451545.00000 gününe denk gelmekte.
    # Elimdeki julian günlerini bu date ile toplarsam aslında epok kaydırma yapmış olurum, bu sayede BC 4713'e göre tarih bulurum.
    # Ardından yeni epokları gregoryana çevirebilirim

    jday4713 = [i + 2451545 for i in dfs["jday.00"]]
    dfs.insert(loc=13, column="jday.4713", value=jday4713)

    # Calendar date'e çevirme
    cdate = [jd.to_gregorian(i) for i in dfs["jday.4713"]]
    dfs.insert(loc=14, column="cdate", value=cdate)

    # Datetime'a çevirme
    cdate_2 = []

    for i in cdate:
        dt_obj = datetime(*i)
        x = dt_obj.strftime("%Y-%m-%d")
        cdate_2.append(x)
    dfs.insert(loc=15, column="cdate_t", value=cdate_2)

    dfs["cdate_t"] = pd.to_datetime(dfs["cdate_t"])

    dfs["sla"] = (dfs["ssh.55"] - dfs["mssh.05"])  #metre biriminde

    return dfs
#-----------------------------------------------------------------------------------------------------------------------
def index_sec(df, index_num):
    """
        --> Herhangi bir dataframe'in indexsinin seçilmesi için kullanılmaktadır.

        input: df
        output: df
    """

    if index_num == 0:
        yeni_df = df.iloc[df.index == 0]
        return yeni_df

    elif index_num == 1:
        yeni_df = df.iloc[df.index == 1]
        return yeni_df

    elif index_num == 2:
        yeni_df = df.iloc[df.index == 2]
        return yeni_df

    elif index_num == 3:
        yeni_df = df.iloc[df.index == 3]
        return yeni_df

    elif index_num == 4:
        yeni_df = df.iloc[df.index == 4]
        return yeni_df

    elif index_num == 5:
        yeni_df = df.iloc[df.index == 5]
        return yeni_df

    elif index_num == 6:
        yeni_df = df.iloc[df.index == 6]
        return yeni_df

    elif index_num == 7:
        yeni_df = df.iloc[df.index == 7]
        return yeni_df

    elif index_num == 8:
        yeni_df = df.iloc[df.index == 8]
        return yeni_df

    elif index_num == 9:
        yeni_df = df.iloc[df.index == 9]
        return yeni_df

    elif index_num == 10:
        yeni_df = df.iloc[df.index == 10]
        return yeni_df

    elif index_num == 11:
        yeni_df = df.iloc[df.index == 11]
        return yeni_df

    elif index_num == 12:
        yeni_df = df.iloc[df.index == 12]
        return yeni_df

    else:
        print("ERROR")
#-----------------------------------------------------------------------------------------------------------------------
def filter_ales_05(df):
    """
        --> Bu fonksiyonun amacı ALES verileri için verilen kısıtlamaların veriye uygulanmasıdır.
        --> 05 uzantılı columnlar için geçerlidir (jason1, jason2 vb).

        input: dataframe
        output: dataframe
    """
    df_result = df[df["distance.00"] > 3]
    df_result = df_result[df_result["swh.05"] < 11]
    df_result = df_result[df_result["stdalt.05"] < 0.20]
    df_result = df_result[df_result["sla"] < 2.5]
    return df_result
#-----------------------------------------------------------------------------------------------------------------------
def merge_df(frames):
    """
        --> Bu fonksiyonun amacı birden fazla aynı türdeki verinin (ALES, LRM)
        dataframelerinin birleştirilmesidir.
        --> Farklı veriler bir liste halinde girilmelidir.

        input: liste
        output: dataframe
    """
    result = pd.concat(frames)
    result = result.sort_values(by="cdate_t", ascending=True)
    return result
#-----------------------------------------------------------------------------------------------------------------------

def aylik(df):
    """
        --> Bu fonkisyonun amacı girdi olarak girilen bir dataframedeki değerlerin tarihlere göre
    ortalamasının alınmasıdır.
        --> Ortalamalar alınarak aylık değerler elde edilecektir.

        input: dataframe
        output: dataframe
    """

    df_aylık = df.resample("MS", on="cdate_t").mean()
    return df_aylık

def yillik(df):
    """
        --> Bu fonkisyonun amacı girdi olarak girilen bir dataframedeki değerlerin tarihlere göre
    ortalamasının alınmasıdır.
        --> Ortalamalar alınarak aylık değerler elde edilecektir.

        input: dataframe
        output: dataframe
        """

    df_yillik = df.groupby(df['cdate_t'].dt.year).mean()
    return df_yillik
#-----------------------------------------------------------------------------------------------------------------------
def ort_koord(frames, distance):

    """
        --> Ortalama koordinat hesabına yarar.
        --> Hesaba katılacak veriler liste halinde girilmeli (frames).

        input: liste
        output: point (2D)
    """

    result = pd.concat(frames)
    result = result.sort_values(by="cdate_t", ascending=True)
    result = result.loc[result['distance.00'] < distance]

    ort_lat = result["glat.00"].mean()
    ort_lon = result["glon.00"].mean()

    return ort_lat, ort_lon
#-----------------------------------------------------------------------------------------------------------------------
def agirlik_hesabi(df, enlem, boylam):
    """
        --> Ağrlık hesabını sağlayan bir fonksiyondur.
        --> İki farklı moda ait veriler ayrı ayrı sokularak hesaplamalar yapılır.
        --> Enlem ve boylam ortalama koordinatlara ait değerlerdir.

        input: df's
        output: df's
    """

    #Şimdi burada koordinatlar arasındaki mesafe hesabını yaparken her ne kadar verilerin T/P
    #elipsoidinde olduğunu bilsekte T/P ile WGS84 arasındaki farkın az olduğunu biliyoruz.
    #Bundan dolayı da aşağıda kullandığım fonksiyonun kullanılması ile mesafelerde sorun olmadan
    #hesap yapabilirim.

    ort_koordinatlar = (enlem, boylam)

    df["distance2ort"] = df.apply(lambda row: geopy.distance.distance((row["glat.00"], row["glon.00"]), ort_koordinatlar).km, axis=1)

    #Ağırlık hesabı
    ortalama_distance = df["distance2ort"].mean()
    df["weight"] = ortalama_distance / df["distance2ort"] #birimsiz

    return df
#-----------------------------------------------------------------------------------------------------------------------
def idw(df):

    """
        --> IDW hesabı yapmayı sağlar.
        --> IDW hesabı yapılacak dataframe girilmeli.

        input: df
        output: series
    """

    #Veri tarihine göre düzenlenir
    df['month_year'] = df['cdate_t'].dt.to_period('M')

    #Diğer düzeltmeler
    dx = df[["cdate_t", "glat.00", "glon.00", "distance.00", "ssh.55", "mssh.05", "weight", "month_year"]].copy()
    dx.reset_index(inplace = True)
    dx.drop(["time"], axis = 1, inplace = True)
    dx.set_index("month_year", inplace = True)

    #IDW ve diğer değerlerin hesabı
    dx["ssh_idw"] = dx.groupby("month_year").apply(lambda df: (df["ssh.55"] * df["weight"]).sum() / df["weight"].sum())
    dx["ssh.55"] = dx.groupby("month_year").apply(lambda df: df["ssh.55"].mean())
    dx["mssh.05"] = dx.groupby("month_year").apply(lambda df: df["mssh.05"].mean())
    dx["glat.00"] = dx.groupby("month_year").apply(lambda df: df["glat.00"].mean())
    dx["glon.00"] = dx.groupby("month_year").apply(lambda df: df["glon.00"].mean())
    dx["cdate_t"] = dx.groupby("month_year").apply(lambda df: df["cdate_t"].mean())
    dx["distance.00"] = dx.groupby("month_year").apply(lambda df: df["distance.00"].mean())

    dx.reset_index(inplace = True)
    dx.drop_duplicates(subset = "month_year", keep = "first", inplace= True)
    dx.reset_index(inplace=True)
    dx.drop(["index"], axis=1, inplace=True)
    dx.drop(["month_year"], axis=1, inplace=True)
    dx["cdate_t"] = dx["cdate_t"].to_numpy().astype('datetime64[M]')

    return dx
#-----------------------------------------------------------------------------------------------------------------------
def dates_interpolation(df):
    """
        --> Aylara göre interpolasyon yapar.
        --> Sadece tarihler için geçerlidir.

        input: df
        output: df
    """
    df['cdate_t'] = pd.to_datetime(df['cdate_t'])

    df = (df.set_index('cdate_t')
          .reindex(pd.date_range(df['cdate_t'].min(), df['cdate_t'].max(), freq='MS'))
          .rename_axis(['cdate_t'])
          .fillna(np.nan)   #0 dı bu
          .reset_index())

    return df
#-----------------------------------------------------------------------------------------------------------------------
def df2excel(df, mode, station_name, station_name_mode):

    """
        --> Herhangi bir dataframe'in excele çevrilmesini sağlar.
        --> Mod ve station name bilgileri verinin pathi için gereklidir.

        input: df
        output: excel table
    """

    path = f"/home/furkan/deus/ALTIMETRY/processler/{mode}/{station_name}/{station_name_mode}.xlsx"
    table = df.to_excel(path)
    return table
#-----------------------------------------------------------------------------------------------------------------------
def ales_sla_filter(df):
    """
        --> SLA'lara göre noiselu verileri elimine etmek için
    :param df:
    :return:
        """
    df_result = df[df["sla"] < 0.6]
    df_result = df_result[df_result["sla"] > -0.6]
    return df_result
#-----------------------------------------------------------------------------------------------------------------------

def iqr(df):

    Q1 = df["ssh_idw"].quantile(0.25)
    Q3 = df["ssh_idw"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df.query('(@Q1 - 1.5 * @IQR) <= ssh_idw <= (@Q3 + 1.5 * @IQR)')

    return filtered
#-----------------------------------------------------------------------------------------------------------------------
def df2newdf(df):

    """
        --> İçine atılan df'in columnlarının yalnızca bir kısmının kullanılması için oluşturulan dataframe.
        --> Ekstra bir hesap yaparak yeni bir columnda oluşturmayı hedeflemiştir.

        input: df
        output: df
    """
    #Bazı ihtiyaç duyulmayan columnların droplanması
    df2 = df.drop(["glat.00", "glon.00", "distance.00", "mssh.05", "weight", "ssh.55"], axis = 1)

    #YYYY.MM biriminde hesaplamaya yapabilmek için yapılan hesaplamalar
    new_date = []
    for i in df2["cdate_t"]:
        new_date.append(i.year + ((i.month - 0.5)/12))

    #Elde edilen değerlerin virgülden sonra çok hanesi olduğu için formatlanması gerekmekte
    formatting = ["%.4f" % i for i in new_date]

    #Elde edilen listenin df'e eklenmesi
    df2["date"] = formatting

    #Eski cdate_t columnu burada elimine edilerek yeni elde edilen column index olarak atandı
    #df2 = df2.drop(["cdate_t"], axis = 1)
    df2.set_index("date", inplace = True)

    #SSH columnunun isminin değiştirilmesi (ileride karşılaştırma yaparken işe yarar diye)
    df2.rename(columns = {"ssh_idw" : "ssh_ales"}, inplace = True)

    #Ağırlık column'unun oluşturulması
    df2["weight"] = 1

    df2.reset_index(inplace = True)
    df2.rename_axis("ay", inplace = True)

    return df2
#-----------------------------------------------------------------------------------------------------------------------
def df2excel3(df, mode, station_name, station_name_mode):

    """
        --> Herhangi bir dataframe'in excele çevrilmesini sağlar.
        --> Mod ve station name bilgileri verinin pathi için gereklidir.

        input: df
        output: excel table
    """

    path = f"/home/furkan/deus/ALTIMETRY/processler/{mode}/{station_name}/{station_name_mode}.xlsx"
    table = df.to_excel(path)
    return table
#-----------------------------------------------------------------------------------------------------------------------
def df2newdf_gel(df):

    """
        --> İçine atılan df'in columnlarının yalnızca bir kısmının kullanılması için oluşturulan dataframe.
        --> Ekstra bir hesap yaparak yeni bir columnda oluşturmayı hedeflemiştir.
        --> SENTINEL 3A SAR VERİLERİ İÇİN OLUŞTURULDU

        input: df
        output: df
    """
    #Bazı ihtiyaç duyulmayan columnların droplanması
    df2 = df.drop(["glat.00", "glon.00", "ssh.40", "weight"], axis = 1)

    #YYYY.MM biriminde hesaplamaya yapabilmek için yapılan hesaplamalar
    new_date = []
    for i in df2["cdate_t"]:
        new_date.append(i.year + ((i.month - 0.5)/12))

    #Elde edilen değerlerin virgülden sonra çok hanesi olduğu için formatlanması gerekmekte
    formatting = ["%.4f" % i for i in new_date]

    #Elde edilen listenin df'e eklenmesi
    df2["date"] = formatting

    #Eski cdate_t columnu burada elimine edilerek yeni elde edilen column index olarak atandı
    #df2 = df2.drop(["cdate_t"], axis = 1)
    df2.set_index("date", inplace = True)

    #SSH columnunun isminin değiştirilmesi (ileride karşılaştırma yaparken işe yarar diye)
    df2.rename(columns = {"ssh_idw" : "ssh_ales"}, inplace = True)

    #Ağırlık column'unun oluşturulması
    df2["weight"] = 1

    df2.reset_index(inplace=True)
    df2.rename_axis("ay", inplace=True)

    return df2










