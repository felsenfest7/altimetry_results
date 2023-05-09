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

def plot_xtrack_beraber(df1, df2, title):

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

def plot_xtrack(df1, title, tarih):

    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff1 = df1

    dff1.reset_index(inplace = True)

    dff1 = dff1[dff1["ssh"].notna()]

    dff1 = dff1[dff1["cdate_t"] > tarih]

    # Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    ax.plot_date(dff1["cdate_t"], dff1["ssh"], "#27aeef", label="XTRACK Verileri")

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





