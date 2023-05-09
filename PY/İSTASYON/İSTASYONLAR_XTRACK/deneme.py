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
import plot_revize as pr
import juliandate as jd
from datetime import datetime

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',30)
pd.set_option('display.max_rows',50000)
#-----------------------------------------------------------------------------------------------------------------------
"""
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.068.nc"
sar_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/S3A_XTRACK_DATA/ctoh.sla.ref.S3A.medsea.500.nc"

#lrm_dataset = xf.read_xtrack(lrm_data, 36.5637203, 34.25539255)
#lrm_dataset = xf.aylik(lrm_dataset)

data = xr.open_dataset(sar_data, decode_times = False)
df = data.to_dataframe()
df2 = df.reset_index()
df2 = df2.dropna(0)

jday4713 = [i + 2433282.50000 for i in df2["time"]]
df2.insert(loc = 21, column="jday4713", value = jday4713)

# Calendar date'e çevirme
cdate = [jd.to_gregorian(i) for i in df2["jday4713"]]
df2.insert(loc = 22, column= "cdate", value = cdate)

cdate_2 = []

for i in cdate:
    dt_obj = datetime(*i)
    x = dt_obj.strftime("%Y-%m-%d")
    cdate_2.append(x)
df2.insert(loc=23, column="cdate_t", value=cdate_2)

# Pandasta çalışması için şu komut girilmeli
df2["cdate_t"] = pd.to_datetime(df2["cdate_t"])

print(df2)

#plot = pr.plot_xtrack(lrm_dataset, sar_dataset, "Deneme")

"""
"""
data =  "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.068.nc"
data = xr.open_dataset(data, decode_times = False)

df = data.to_dataframe()
df2 = df.reset_index()
ist_koord = (36.5637203, 34.25539255 )

df2["distance2coast"] = df2.apply(lambda row: geopy.distance.distance((row["lat"], row["lon"]), ist_koord).km, axis=1)

#df2["distance2coast"] = df2[["distance2coast"]].min(axis=1).min()

#print(df2[(df2["lat"] < 36.5637203) & (df2["lat"] > 36.5637203 - 0.5)])

#print(df2[df2["points_numbers"] == 46])

print(df2[46500:47500])
"""
"""
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.068.nc"
lrm_dataset = read_xtrack(lrm_data, 36.5637203, 34.25539255, 0.05)
#lrm_dataset_aylik = xf.aylik(lrm_dataset)

print(lrm_dataset[["lat", "lon", "ssh", "ssh_wgs84", "mssh", "sla"]])
"""
"""
lrm_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/ctoh.sla.ref.TP+J1+J2+J3.medsea.109.nc"
lrm_dataset = xf.read_xtrack(lrm_data, 38.42960155, 26.72214568, 0.36)
lrm_dataset_aylik = xf.aylik(lrm_dataset)

print(lrm_dataset)
"""
"""
sar_data = "/home/furkan/deus/ALTIMETRY/processler/XTRACK/XTRACK_DATA/S3A_XTRACK_DATA/ctoh.sla.ref.S3A.medsea.242.nc"
sar_dataset = xf.read_xtrack(sar_data, 40.28046929973475, 26.172972952254643, 4)

print(sar_dataset)
"""














