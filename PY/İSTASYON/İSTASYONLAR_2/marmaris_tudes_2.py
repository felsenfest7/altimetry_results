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
path1 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MARMARİS/MARMARİS_15DK/27_6_2009-27_6_2014.txt" #15dk
path2 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MARMARİS/MARMARİS_15DK/27_6_2014-27_6_2019.txt" #15dk
path3 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MARMARİS/MARMARİS_15DK/27_6_2019-13_11_2019.txt" #15dk

#Dataframelerin oluşturulması
df1 = tf.tudes_oku(path1)
df2 = tf.tudes_oku(path2)
df3 = tf.tudes_oku(path3)

#Günlük verilerin elde edilmesi
frames_15dk = [df1, df2, df3]
df_15dk = tf.tudes_15dk_birlestir(frames_15dk)

#İki veri grubunun birleştirilmesi ve aylık verilerin elde edilmesi
frames_merged = [df_15dk]
df_aylik = tf.birlestir_1560(frames_merged)

#Aylık verilerin interpole edilmesi
df_aylik = tf.dates_interpolation(df_aylik)

#Harmonik analiz hesabı
ha = tf.harmonik_analiz_tudes(df_aylik, "Marmaris", "marmaris", "tudes")





























