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
pd.set_option('display.max_rows',30000)
#-----------------------------------------------------------------------------------------------------------------------
#GOKCEADA
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.170.nc"
lrm_dataset = xf.read_xtrack(lrm_data, 40.28046929973475, 26.172972952254643, 0.05)
lrm_dataset_aylik = xf.aylik(lrm_dataset)

#IQR HESABI
filtered = xf.iqr_xtrack(lrm_dataset_aylik)

#Ufak noiseların yok edilmesi gerekmekte
#filtered = filtered[filtered["ssh"] > 39.60]
#filtered = filtered[filtered["ssh"] < 39.90]

#Dates interpolation
filtered = xf.dates_interpolation_xtrack(filtered)

#Plotun çizdirilmesi
#plot = xp.plot_xtrack(filtered, "Gökçeada X-TRACK Verileri", "2008-01-01")

#nx3'lük matrisin oluşturulması
wish = xf.df2newdf_xtrack(filtered, "2009-05-01", "2019-12-01")

#Excele aktarılması
#wish_table = xf.df2excel_xtrack(wish, "XTRACK", "GOKCEADA", "gokceada_ssh_weight")

haa = ha.harmonik_analiz2(wish, "Gökçeada X-TRACK", "gokceada", "xtrack")


