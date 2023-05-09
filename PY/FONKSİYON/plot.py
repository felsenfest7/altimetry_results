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

#PLOTLARIN ÇİZİMİ
#-----------------------------------------------------------------------------------------------------------------------
def plot_ssh_gunluk(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.

        input: dataframe
        output: plot
    """
    #SSH GRAFİĞİ ÇİZDİRME
    #df["cdate_t"] = pd.to_datetime(df["cdate_t"]) --> RNM'YE EKLEDİM BUNU

    #Ardından normal bir fig, ax ile grafik çizdirilir
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(df["cdate_t"], df["ssh.55"], "royalblue", label="Deniz Seviyesi Yüksekliği")

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    df["EWMA7"] = df["ssh.55"].ewm(span = 7).mean()
    ax.plot_date(df["cdate_t"], df["EWMA7"], "red", label="Hareketli Ortalama")

    #Sadece year bilgileri için YearLocator kullanılmalı
    ax.xaxis.set_major_locator(YearLocator())
    #Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    #Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Günlük Deniz Seviyesi Yüksekliği (m)", fontsize=13)

    #TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ## İlk olarak datetime objectler matplotlib için çevriliyor
    x_date = df["cdate_t"]
    x_num = dates.date2num(x_date)
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(x_num, df["ssh.55"], 1)
    fit = np.poly1d(trend)
    ##Veriler tekrar datetime'a çevriliyor
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot_date(dates.num2date(x_fit), fit(x_fit), "k--", label = "Trend")

    #MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_ssh = df["ssh.55"].mean()
    ort_ssh = "%.3f" % ort_ssh
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = rmn.mean_square_gunluk(df)
    mse = "%.2f" % mse

    #Trend değerlerinin plota yazdırılması
    plt.text(datetime.date(2008, 1, 1), 19.03, f"Trend: {ort_ssh} m ± {mse} mm/yıl")

    plt.title(title)
    ax.legend(loc="best")
    plt.grid(True)
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def plot_ssh_aylik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    # Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Nan değerlerinin alınmaması
    dff = dff[dff["ssh.55"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff["cdate_t"], dff["ssh.55"], "royalblue", label="Deniz Seviyesi Yüksekliği")

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    dff["EWMA3"] = dff["ssh.55"].ewm(span=3).mean()
    ax.plot_date(dff["cdate_t"], dff["EWMA3"], "red", label="Hareketli Ortalama")

    #TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ## İlk olarak datetime objectler matplotlib için çevriliyor
    x_date = dff["cdate_t"]
    x_num = dates.date2num(x_date)
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(x_num, dff["ssh.55"], 1)
    fit = np.poly1d(trend)
    ##Veriler tekrar datetime'a çevriliyor
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot_date(dates.num2date(x_fit), fit(x_fit), "k--", label="Trend")

    # MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_ssh = dff["ssh.55"].mean()
    ort_ssh = "%.3f" % ort_ssh
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = rmn.mean_square_aylik(df)
    mse = "%.2f" % mse

    #Trend değerlerinin plota yazdırılması
    plt.text(datetime.date(2017, 12, 1), 21.53, f"Trend: {ort_ssh} m ± {mse} mm/yıl")

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
#-----------------------------------------------------------------------------------------------------------------------
def plot_ssh_yillik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin ssh plotunu çizdirmektir.
        --> Yıllık fonksiyonu ile elde edilen veriler için geçerli.
        --> Trend hesabı yapılarak ardından MSE hesabı yapılır. MSE hesabı yapılırken SLA = SSH -MSS eşitliği kullanılır.
        --> Önceki fonksiyonlarda datetime object değiştirildiği için integer olarak kullanılıyor.

            input: dataframe
            output: plot
        """

    #İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    #Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.locator_params(integer=True)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot(dff["cdate_t"], dff["ssh.55"], "royalblue", label="Deniz Seviyesi Yüksekliği")

    # Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Ortalama Yıllık Deniz Seviyesi Yüksekliği (m)", fontsize=13)

    #TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(dff["cdate_t"], dff["ssh.55"], 1)
    fit = np.poly1d(trend)
    ax.plot(dff["cdate_t"], fit(dff["cdate_t"]), "k--", label="Trend")

    #MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_ssh = dff["ssh.55"].mean()
    ort_ssh = "%.3f" % ort_ssh
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = mean_squared_error(dff["ssh.55"], dff["mssh.05"])  # Bu değer metre biriminde
    mse_cm = mse * 100  # Bu değer santimetre biriminde
    mse_cm = "%.2f" % mse_cm

    #Trend değerlerinin plota yazdırılması
    plt.text(2010, 25.6, f"Trend: {ort_ssh} m ± {mse_cm} cm")

    plt.title(title)
    plt.legend(loc = "best")
    plt.grid(True)
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def plot_sla_gunluk(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin SLA plotunu çizdirmektir.

        input: dataframe
        output: plot
    """

    #Ardından normal bir fig, ax ile grafik çizdirilir
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(df["cdate_t"], df["sla"], "royalblue", label="Deniz Seviyesi Anomalisi")

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    df["EWMA7"] = df["sla"].ewm(span = 7).mean()
    ax.plot_date(df["cdate_t"], df["EWMA7"], "red", label="Hareketli Ortalama")

    #Sadece year bilgileri için YearLocator kullanılmalı
    ax.xaxis.set_major_locator(YearLocator())
    #Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    # TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ## İlk olarak datetime objectler matplotlib için çevriliyor
    x_date = df["cdate_t"]
    x_num = dates.date2num(x_date)
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(x_num, df["sla"], 1)
    fit = np.poly1d(trend)
    ##Veriler tekrar datetime'a çevriliyor
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot_date(dates.num2date(x_fit), fit(x_fit), "k--", label="Trend")

    # MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_sla = df["sla"].mean()
    ort_sla = "%.3f" % ort_sla #m
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = rmn.mean_square_gunluk(df)
    mse = "%.2f" % mse

    # Trend değerlerinin plota yazdırılması
    plt.text(datetime.date(2008, 1, 1), -2.96, f"Trend: {ort_sla} m ± {mse} mm/yıl")

    #Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Günlük Deniz Seviyesi Anomalisi (m)", fontsize=13)

    plt.title(title)
    ax.legend(loc="best")
    plt.grid(True)
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def plot_sla_aylik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin SLA plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    # Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Nan değerlerinin alınmaması
    dff = dff[dff["sla"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff["cdate_t"], dff["sla"], "royalblue", label="Deniz Seviyesi Anomalisi")

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    dff["EWMA3"] = dff["sla"].ewm(span=3).mean()
    ax.plot_date(dff["cdate_t"], dff["EWMA3"], "red", label="Hareketli Ortalama")

    #Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval = 18))
    #Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    # TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ## İlk olarak datetime objectler matplotlib için çevriliyor
    x_date = dff["cdate_t"]
    x_num = dates.date2num(x_date)
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(x_num, dff["sla"], 1)
    fit = np.poly1d(trend)
    ##Veriler tekrar datetime'a çevriliyor
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot_date(dates.num2date(x_fit), fit(x_fit), "k--", label="Trend")

    # MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_sla = dff["sla"].mean()
    ort_sla = "%.3f" % ort_sla
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = rmn.mean_square_aylik(df)
    mse = "%.2f" % mse

    # Trend değerlerinin plota yazdırılması
    plt.text(datetime.date(2008, 1, 1), -0.96, f"Trend: {ort_sla} m ± {mse} mm/yıl")

    ax.set_xlabel("Tarih", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Anomalisi (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def plot_sla_yillik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir ALES/LRM/SAR/SARIN df'inin SLA plotunu çizdirmektir.
        --> Yıllık fonksiyonu ile elde edilen veriler için geçerli.
        --> Önceki fonksiyonlarda datetime object değiştirildiği için integer olarak kullanılıyor.

            input: dataframe
            output: plot
        """

    #İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    #Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.locator_params(integer=True)
    ax.plot(dff["cdate_t"], dff["ssh.55"], "royalblue", label="Deniz Seviyesi Anomalisi")

    # Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Ortalama Yıllık Deniz Seviyesi Anomalisi (m)", fontsize=13)

    plt.title(title)
    plt.legend(loc = "best")
    plt.grid(True)
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def sla_gunluk(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir SLA df'inin SLA plotunu çizdirmektir.

        input: dataframe
        output: plot
    """

    #Ardından normal bir fig, ax ile grafik çizdirilir
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(df["cdate_t"], df["sla.40"], "royalblue", label="Deniz Seviyesi Anomalisi")

    #MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    df["EWMA7"] = df["sla.40"].ewm(span = 7).mean()
    ax.plot_date(df["cdate_t"], df["EWMA7"], "red", label="Hareketli Ortalama")

    #Sadece year bilgileri için YearLocator kullanılmalı
    ax.xaxis.set_major_locator(YearLocator())
    #Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    # TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ## İlk olarak datetime objectler matplotlib için çevriliyor
    x_date = df["cdate_t"]
    x_num = dates.date2num(x_date)
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(x_num, df["sla.40"], 1)
    fit = np.poly1d(trend)
    ##Veriler tekrar datetime'a çevriliyor
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot_date(dates.num2date(x_fit), fit(x_fit), "k--", label="Trend")

    # MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_sla = df["sla.40"].mean()
    ort_sla = "%.3f" % ort_sla  # m
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = rmn.mean_square_gunluk_lrm(df)
    mse = "%.2f" % mse

    # Trend değerlerinin plota yazdırılması
    plt.text(datetime.date(2008, 1, 1), -0.33, f"Trend: {ort_sla} m ± {mse} mm/yıl")

    #Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Günlük Deniz Seviyesi Anomalisi (m)", fontsize=13)

    plt.title(title)
    ax.legend(loc="best")
    plt.grid(True)
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def sla_aylik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir SLA df'inin SLA plotunu çizdirmektir.
        --> Aylık fonksiyonu ile elde edilen veriler için geçerli.

            input: dataframe
            output: plot
    """
    # İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    # Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Nan değerlerinin alınmaması
    dff = dff[dff["sla.40"].notna()]

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff["cdate_t"], dff["sla.40"], "royalblue", label="Deniz Seviyesi Anomalisi")

    # MOVING AVERAGE HESABI
    ##Moving average ile daha smooth bir veri elde ediliyor, ekstren değerler ihmal ediliyor.
    dff["EWMA3"] = dff["sla.40"].ewm(span=3).mean()
    ax.plot_date(dff["cdate_t"], dff["EWMA3"], "red", label="Hareketli Ortalama")

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=18))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')

    # TREND EĞRİSİ HESAPLAMA VE ÇİZDİRME
    ## İlk olarak datetime objectler matplotlib için çevriliyor
    x_date = dff["cdate_t"]
    x_num = dates.date2num(x_date)
    ##Trend eğrisi hesaplanıyor. Birinci dereceden yapılıyor.
    trend = np.polyfit(x_num, dff["sla.40"], 1)
    fit = np.poly1d(trend)
    ##Veriler tekrar datetime'a çevriliyor
    x_fit = np.linspace(x_num.min(), x_num.max())
    ax.plot_date(dates.num2date(x_fit), fit(x_fit), "k--", label="Trend")

    # MEAN SQUARE ERROR HESABI
    ##Ortalama SSH değeri
    ort_sla = dff["sla.40"].mean()
    ort_sla = "%.3f" % ort_sla
    ##Ortalama Karesel Hata Hesabı (MSE)
    mse = rmn.mean_square_aylik_lrm(df)
    mse = "%.2f" % mse

    # Trend değerlerinin plota yazdırılması
    plt.text(datetime.date(2019, 1, 1), -0.23, f"Trend: {ort_sla} m ± {mse} mm/yıl")

    ax.set_xlabel("Tarih", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Anomalisi (m)", fontsize=13)
    ax.legend(loc="best")
    plt.grid(True)
    plt.title(title)
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def sla_yillik(df, title):
    """
        --> Bu fonksiyonun amacı girdi olarak girilen herhangi bir SLA df'inin SLA plotunu çizdirmektir.
        --> Yıllık fonksiyonu ile elde edilen veriler için geçerli.
        --> Önceki fonksiyonlarda datetime object değiştirildiği için integer olarak kullanılıyor.

            input: dataframe
            output: plot
        """

    #İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
    dfx = df.reset_index()
    #Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = dfx

    #Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.locator_params(integer=True)
    ax.plot(dff["cdate_t"], dff["sla.40"], "royalblue", label="Deniz Seviyesi Anomalisi")

    # Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
    ax.set_xlabel("Yıl", fontsize=13)
    ax.set_ylabel("Ortalama Yıllık Deniz Seviyesi Anomalisi (m)", fontsize=13)

    plt.title(title)
    plt.legend(loc = "best")
    plt.grid(True)
    plt.show()

def iki_df_sla_plot(df1, df2, title, mod):

    """
        --> İki farklı SLA df'inin plotunu çizdirmeyi sağlar.
        --> Mod seçeneği üç çeşittir: Gunluk SLA, Aylık SLA ve Yıllık SLA'dır.
        --> df1: lrm, df2: ales
    """

    if mod == "gunluk":

        # LRM ve ALES verileri ile figürün çizdirilmesi
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax.plot_date(df1["cdate_t"], df1["sla.40"], "royalblue", label="LRM/SAR/SARIN Deniz Seviyesi Anomalisi")
        ax.plot_date(df2["cdate_t"], df2["sla"], "red", label="ALES Deniz Seviyesi Anomalisi")

        # Sadece year bilgileri için YearLocator kullanılmalı
        ax.xaxis.set_major_locator(YearLocator())
        # Burada ise verinin veri tipinin formatı girilmeli
        ax.fmt_xdata = DateFormatter('% Y-% m-% d')

        # Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
        ax.set_xlabel("Yıl", fontsize=13)
        ax.set_ylabel("Günlük Deniz Seviyesi Anomalisi (m)", fontsize=13)

        ##Ortalama SLA değeri
        ort_ssh_lrm = df1["sla.40"].mean()
        ort_ssh_lrm = "%.3f" % ort_ssh_lrm

        ort_ssh_ales = df2["sla"].mean()
        ort_ssh_ales = "%.3f" % ort_ssh_ales

        ##Ortalama Karesel Hata Hesabı (MSE)
        mse_lrm = rmn.mean_square_gunluk_lrm(df1)
        mse_lrm = "%.2f" % mse_lrm

        mse_ales = rmn.mean_square_gunluk(df2)
        mse_ales = "%.2f" % mse_ales

        # Ortalama değerlerinin plota yazdırılması
        plt.text(datetime.date(2008, 6, 1), -2.56, f"LRM/SAR/SARIN Trend: {ort_ssh_lrm} m ± {mse_lrm} mm/yıl")
        plt.text(datetime.date(2008, 6, 1), -3.04, f"ALES Trend: {ort_ssh_ales} m ± {mse_ales} mm/yıl")

        plt.title(title)
        ax.legend(loc="best")
        plt.grid(True)
        plt.show()

    elif mod == "aylik":

        # İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
        dfx1 = df1.reset_index()
        dfx2 = df2.reset_index()

        # Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
        dff1 = dfx1
        dff2 = dfx2

        # Nan değerlerinin alınmaması
        dff1 = dff1[dff1["sla.40"].notna()]
        dff2 = dff2[dff2["sla"].notna()]

        # Plotun çizdirilmesi
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        ax.plot_date(dff1["cdate_t"], dff1["sla.40"], "royalblue", label="LRM/SAR/SARIN Deniz Seviyesi Anomalisi")
        ax.plot_date(dff2["cdate_t"], dff2["sla"], "red", label="ALES Deniz Seviyesi Anomalisi")

        # Year-Month bilgileri için MonthLocator kullanılmalı
        ax.xaxis.set_major_locator(MonthLocator(interval=18))
        # Burada ise verinin veri tipinin formatı girilmeli
        ax.fmt_xdata = DateFormatter('% Y-% m-% d')

        ##Ortalama SLA değeri
        ort_ssh_lrm = dff1["sla.40"].mean()
        ort_ssh_lrm = "%.3f" % ort_ssh_lrm

        ort_ssh_ales = dff2["sla"].mean()
        ort_ssh_ales = "%.3f" % ort_ssh_ales

        ##Ortalama Karesel Hata Hesabı (MSE)
        mse_lrm = rmn.mean_square_aylik_lrm(df1)
        mse_lrm = "%.2f" % mse_lrm

        mse_ales = rmn.mean_square_aylik(df2)
        mse_ales = "%.2f" % mse_ales

        ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
        ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Anomalisi (m)", fontsize=13)
        ax.legend(loc="best")
        plt.grid(True)
        plt.title(title)

        # Ortalama değerlerinin plota yazdırılması
        plt.text(datetime.date(2008, 6, 1), -0.87, f"LRM/SAR/SARIN Trend: {ort_ssh_lrm} m ± {mse_lrm} mm/yıl")
        plt.text(datetime.date(2008, 6, 1), -0.94, f"ALES Trend: {ort_ssh_ales} m ± {mse_ales} mm/yıl")

        plt.show()

    elif mod == "yillik":

        # İlk önce cdate_t değerleri indexe gittiği için ve çizilirken sorun yaşandığı için index resetlenir
        dfx1 = df1.reset_index()
        dfx2 = df2.reset_index()

        # Ardından dfx çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
        dff1 = dfx1
        dff2 = dfx2

        # Plotun çizdirilmesi
        fig, ax = plt.subplots()
        ax.locator_params(integer=True)
        ax.plot(dff1["cdate_t"], dff1["sla.40"], "royalblue", label="LRM/SAR/SARIN Deniz Seviyesi Anomalisi")
        ax.plot_date(dff2["cdate_t"], dff2["sla"], "red", label="ALES Deniz Seviyesi Anomalisi")

        # Geriye kalan bilgiler. Bu kodun bitimi ile ssh plotu çizimi biter.
        ax.set_xlabel("Yıl", fontsize=13)
        ax.set_ylabel("Ortalama Yıllık Deniz Seviyesi Anomalisi (m)", fontsize=13)

        ##Ortalama SLA değeri
        ort_ssh_lrm = df1["sla.40"].mean()
        ort_ssh_lrm = "%.3f" % ort_ssh_lrm

        ort_ssh_ales = df2["sla"].mean()
        ort_ssh_ales = "%.3f" % ort_ssh_ales

        # Ortalama değerlerinin plota yazdırılması
        plt.text(2018, 0, f"Trend: {ort_ssh_lrm} m")
        plt.text(2018, 0, f"Trend: {ort_ssh_ales} m")

        plt.title(title)
        plt.legend(loc="best")
        plt.grid(True)
        plt.show()




