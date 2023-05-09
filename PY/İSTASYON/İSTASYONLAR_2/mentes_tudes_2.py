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
path1 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MENTES/MENTES_60DK/MenteÅŸ_60 Dakika_13-4-1999 00-00-00_13-4-2004 00-00-00_13-11-2019 15-29-59.txt" #60dk
path2 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MENTES/MENTES_15DK/2_1_2002-2_1_2007.txt" #15dk
path3 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MENTES/MENTES_15DK/2_1_2007-2_1_2012.txt" #15dk
path4 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MENTES/MENTES_15DK/2_1_2012-2_1_2017.txt" #15dk
path5 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MENTES/MENTES_15DK/2_1_2017-13_11_2019.txt" #15dk

#Dataframelerin oluşturulması
df1 = tf.tudes_oku(path1)
df2 = tf.tudes_oku(path2)
df3 = tf.tudes_oku(path3)
df4 = tf.tudes_oku(path4)
df5 = tf.tudes_oku(path5)

#15 dakikalık verilerin birleştirilmesi
frames_15dk = [df2, df3, df4, df5]
df_15dk = tf.tudes_15dk_birlestir(frames_15dk)

#60 dakikalık verilerin birleştirilmesi
frames_60dk = [df1]
df_60dk = tf.tudes_60dk_birlestir(frames_60dk)

#İki veri grubunun birleştirilmesi ve aylık verilerin elde edilmesi
frames_merged = [df_15dk, df_60dk]
df_aylik = tf.birlestir_1560(frames_merged)

#Burada elle bir düzeltme yapacam
df_aylik = df_aylik[df_aylik["Deniz_Seviyesi"] < 0.25]
#df_aylik = df_aylik[df_aylik["Deniz_Seviyesi"] > 0]

#Aylık verilerin interpole edilmesi
df_aylik = tf.dates_interpolation(df_aylik)

#Harmonik analiz hesabı
ha = tf.harmonik_analiz_tudes(df_aylik, "Menteş", "mentes", "tudes")












































