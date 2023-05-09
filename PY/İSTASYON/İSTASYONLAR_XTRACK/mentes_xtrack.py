from netCDF4 import Dataset as dt
import xarray as xr
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopy.distance

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR")

import xtrack_functions as xf
import xtrack_plot as xp
import harmonik_analiz as ha

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',30)
pd.set_option('display.max_rows',500000)
#-----------------------------------------------------------------------------------------------------------------------
#MENTEŞ
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.109.nc"
lrm_dataset = xf.read_xtrack(lrm_data, 38.42960155, 26.72214568, 0.36)
lrm_dataset_aylik = xf.aylik(lrm_dataset)

#IQR HESABI
filtered = xf.iqr_xtrack(lrm_dataset_aylik)

#Ufak noiseların yok edilmesi gerekmekte
filtered = filtered[filtered["ssh"] > 38.00]
filtered = filtered[filtered["ssh"] < 38.40]

#Dates interpolation
filtered = xf.dates_interpolation_xtrack(filtered)

#Plotun çizdirilmesi
#plot = xp.plot_xtrack(lrm_dataset_aylik, "Menteş X-TRACK Verileri", "2002-01-01")

#nx3'lük matrisin oluşturulması
wish = xf.df2newdf_xtrack(filtered, "1999-03-01", "2019-12-01")

#wish = wish[wish["ssh_ales"] < 38.35]
#wish = wish[wish["ssh_ales"] > 38.02]

#Excele aktarılması
#wish_table = xf.df2excel_xtrack(wish, "XTRACK", "MENTES", "mentes_ssh_weight.xlsx")

haa = ha.harmonik_analiz2(wish, "Menteş X-TRACK", "mentes", "xtrack")


