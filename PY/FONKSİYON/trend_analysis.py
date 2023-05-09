#Kütüphaneler
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse
from statsmodels.tsa.seasonal import seasonal_decompose

#Fonksiyonlar

##Multiplicative time series analysis
def additive(df):
    """
        --> Additive yöntemi ile trend analizinin yapılmasını sağlar.
        --> Value = Base Level + Trend + Seasonality + Error

        input: df
        output: plot
    """
    #NaN değerlerin çıkarılması
    df.sla.dropna()
    dff = df[df["sla"]]
    print(dff)

    #Additive yönteminin hesabı
    #add = seasonal_decompose(dfx["sla"], model = "additive", period = 10)

    #Grafiklerin çizdirilmesi
    #plt.figure(figsize = (12,6))
    #add.plot().suptitle("Additive Decomposotion for Antalya", fontsize = 16)
    #plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    #plt.show()

