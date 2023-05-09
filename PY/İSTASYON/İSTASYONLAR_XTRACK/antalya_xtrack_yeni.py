from netCDF4 import Dataset as dt
import xarray as xr
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopy.distance
import juliandate as jd
from datetime import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, MonthLocator, YearLocator
from matplotlib.ticker import FormatStrFormatter
import math as m
from numpy.linalg import inv

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")

import xtrack_functions as xf
import xtrack_plot as xp

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

print(df3)



































