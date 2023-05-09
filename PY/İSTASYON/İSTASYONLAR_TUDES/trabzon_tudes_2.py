import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_PY/GENEL_DOSYALAR/TUDES")
import tudes_functions_2 as tf
#--------------------------------------------------
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',10000)
#--------------------------------------------------
#15 ve 60dklık verilerin birleştirilerek kullanılması gerekiliyor. Çünkü veriler arası zaman farklılıkları var.
#Bunları tespit ederken ben elimle txt filedan düzelttim ve ona göre verileri düzenleyerek buraya aktardım.
path1 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/TRABZON/TRABZON_15DK/14_7_2002-14_7_2007.txt" #15dk
path2 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/TRABZON/TRABZON_15DK/14_7_2007-14_7_2012.txt" #15dk
path3 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/TRABZON/TRABZON_15DK/14_7-2012-14_7_2017.txt" #15dk
path4 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/TRABZON/TRABZON_15DK/14-7-2017-13_11_2019.txt" #15dk

#Dataframelerin oluşturulması
df1 = tf.tudes_oku(path1)
df2 = tf.tudes_oku(path2)
df3 = tf.tudes_oku(path3)
df4 = tf.tudes_oku(path4)

#Günlük verilerin elde edilmesi
frames_15dk = [df1, df2, df3, df4]
df_15dk = tf.tudes_15dk_birlestir(frames_15dk)

#İki veri grubunun birleştirilmesi ve aylık verilerin elde edilmesi
frames_merged = [df_15dk]
df_aylik = tf.birlestir_1560(frames_merged)

#Burada elle bir düzeltme yapacam
#df_aylik = df_aylik[df_aylik["Deniz_Seviyesi"] < 0.55]
#df_aylik = df_aylik[df_aylik["Deniz_Seviyesi"] > 0.25]

#Aylık verilerin interpole edilmesi
df_aylik = tf.dates_interpolation(df_aylik)

#Harmonik analiz hesabı
ha = tf.harmonik_analiz_tudes(df_aylik, "Trabzon", "trabzon", "tudes")





























