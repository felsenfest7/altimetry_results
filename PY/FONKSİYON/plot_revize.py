import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib
from netCDF4 import Dataset as dt
import glob
import xarray as xr
import pandas as pd
import cartopy as ca
import os
import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, MonthLocator, YearLocator
import statsmodels
import matplotlib.dates as dates
from sklearn.metrics import mean_squared_error
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.ticker import FormatStrFormatter
import read_merge_nc as rmn
from dateutil.relativedelta import relativedelta
import math as m
import geopy.distance

#PLOTLARIN ÇİZİMİ
#-----------------------------------------------------------------------------------------------------------------------
def plot_ssh_aylik(df_lrm, df_sar, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES VERİSİNİN df'inin ssh plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff_lrm = df_lrm
    dff_sar = df_sar

    #Nan değerlerinin alınmaması
    dff_lrm = dff_lrm[dff_lrm["ssh_idw"].notna()]
    dff_sar = dff_sar[dff_sar["ssh_idw"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff_lrm["cdate_t"], dff_lrm["ssh_idw"], "#27aeef", label="ALES Envisat Verileri")
    ax.plot_date(dff_sar["cdate_t"], dff_sar["ssh_idw"], "#ea5545", label="ALES Jason Verileri")

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=6))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()

def plot_ssh_aylikv2(df_lrm, df_sar, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir GELENEKSEL VERİNİN df'inin ssh plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff_lrm = df_lrm
    dff_sar = df_sar

    #Nan değerlerinin alınmaması
    dff_lrm = dff_lrm[dff_lrm["ssh_idw"].notna()]
    dff_sar = dff_sar[dff_sar["ssh_idw"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff_lrm["cdate_t"], dff_lrm["ssh_idw"], "#87bc45", label="Altimetri LRM Verileri")
    ax.plot_date(dff_sar["cdate_t"], dff_sar["ssh_idw"], "#f46a9b", label="Altimetri SAR Verileri")

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=36))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()

def iki_df_ssh_plot(df1, df3, df4, title):
    """
            --> İki farklı SSH df'inin plotunu çizdirmeyi sağlar.
            --> df1: ales LRM, df2: ales SAR, df3: geleneksel LRM, df4: geleneksel SAR
        """

    # İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx1 = df1.reset_index()
    dfx3 = df3.reset_index()
    dfx4 = df4.reset_index()

    # Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff1 = dfx1
    dff3 = dfx3
    dff4 = dfx4

    # Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff1["cdate_t"], dff1["ssh_idw"], "#9b19f5", label="ALES")
    ax.plot_date(dff3["cdate_t"], dff3["ssh_idw"], "#e60049", label="Altimetri LRM")
    ax.plot_date(dff4["cdate_t"], dff4["ssh_idw"], "#00bfa0", label="Altimetri SAR")

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=18))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Ağırlıklandırılmış Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)

    plt.show()

def plot_ssh_aylik_yeni(df_lrm, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES VERİSİNİN df'inin ssh plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff_lrm = df_lrm

    #Nan değerlerinin alınmaması
    dff_lrm = dff_lrm[dff_lrm["ssh_idw"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff_lrm["cdate_t"], dff_lrm["ssh_idw"], "#0d88e6", label="SAR Verileri")

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

def plot_xtrack(df1, df2, title):

    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff1 = df1
    dff2 = df2

    dff1.reset_index(inplace = True)
    dff2.reset_index(inplace=True)

    dff1 = dff1[dff1["cdate_t"] > "2003-05-14"]
    dff2 = dff2[dff2["cdate_t"] > "2003-05-14"]

    # Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff1["cdate_t"], dff1["ssh"], "#27aeef", label="XTRACK LRM Verileri")
    ax.plot_date(dff2["cdate_t"], dff2["ssh"], "#0d88e6", label="XTRACK SAR Verileri")

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

def distance_plot(df, ist_enlem, ist_boylam, ort_enlem, ort_boylam, title):

    ort_koordinatlar = (ort_enlem, ort_boylam)
    ist_koordinatlar = (ist_enlem, ist_boylam)

    distancex = geopy.distance.distance(ort_koordinatlar, ist_koordinatlar).km

    fig = plt.figure()
    ax = fig.add_subplot(projection = "3d")

    ax.scatter(df["glat.00"], df["glon.00"], df["distance.00"], label = "Altimetri Verileri")
    ax.scatter(ort_enlem, ort_boylam, distancex, c = "#ff7f0e", marker = "^", label = "Ortalama Koordinat")

    ax.set_xlabel('Enlem')
    ax.set_ylabel('Boylam')
    ax.set_zlabel('Kıyıya uzaklık (km)')
    ax.set_title(f"{title} Altimetri Verilerinin Kıyıya Olan Uzaklıkları")

    plt.legend(loc="best")

    plt.show()

def corr_ssh(df, title, mss, trend):
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
    ax.plot_date(dff["cdate_t"], dff["SSH_ilk"], "#FFBF00", label="SSH Ölçü")
    ax.plot_date(dff["cdate_t"], dff["SSH_model"], "#0d88e6", label="SSH Model")

    ax.axhline(y = mss, c = "red", label = "MSS")
    plt.text(datetime.date(2016, 1, 1), 37.685, trend, fontsize=10)

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

def excele_yolla(df, station_name, mode):

    path = f"/home/furkan/deus/ALTIMETRY/processler/SONUÇLAR/SPEKTRAL_ANALİZ/ALES/ALES_EXCELLER/{station_name}_{mode}_ssh_model.xlsx"
    df.to_excel(path)




