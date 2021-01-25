import datetime
import os
import sys
import numpy as np
import tensorflow as tf
import pandas as pd
from pandas.io.json import json_normalize
from xlrd import open_workbook
from xlutils.copy import copy
#(r'\s+(+\.|#', np.NaN, regex = True).replace('', np.NaN)

def prediction(dataframe):

    dataframe.shape
    date_time = pd.to_datetime(dataframe.pop('Zeit'), format='%d/%m/%Y %H:%M')
    dataframe.replace('', 0, inplace=True)
    dataframe = dataframe.astype('float')
    ziel = dataframe[['Graz-DB', 'Graz-MG', 'Graz-S', 'Graz-OP', 'Graz-N', 'Graz-W', 'Lustb']].replace(0, np.NaN).T.mean().values
    luftdruck = dataframe[['Luftdruck']].replace(0, np.NaN).T.mean()
    dataframe['ziel'] = ziel
    dataframe = dataframe[['ziel']]

    #wetterDatenPath = '/home/pmf/tensorflowFlasksRuntime/wetterDaten.xlsx'
    #df_luftdruck = pd.read_excel(wetterDatenPath, sheet_name=3)[3:]
    #df_luftdruck = pd.DataFrame(df_luftdruck[['Graz-N']].replace(0, np.NaN).T.mean(), columns=['luftdruck'])
    #df_luftdruck = df_luftdruck.astype('float')
    #df_luftdruck.reset_index(inplace=True)
    #df_luftdruck = df_luftdruck[0:47]
    #print(df_luftdruck)

    #df_luftdruck.index = df_luftdruck.index -1

    dataframe['Luftdruck'] = luftdruck
    print(dataframe)

    timestamp_s = date_time.map(datetime.datetime.timestamp)
    day = 24 * 60 * 60
    year = (365.2425) * day

    dataframe['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    dataframe['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    dataframe['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    dataframe['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

    dataframe = dataframe.fillna(0)

    file1 = open("/home/pmf/tensorflowFlasksRuntime/Train_mean_std2.txt", "r")
    mean_and_sdt = file1.read().split('\n')
    len(mean_and_sdt) // 2
    train_mean = [float(x.split(' ')[-1]) for x in mean_and_sdt[:len(mean_and_sdt) // 2]]
    train_std = [float(x.split(' ')[-1]) for x in mean_and_sdt[:len(mean_and_sdt) // 2]]
    file1.close()
    example = (dataframe - train_mean) / train_std
    model = tf.keras.models.load_model('/home/pmf/tensorflowFlasksRuntime/lstm_model002')

    output = pd.DataFrame(model.predict(np.array([tf.constant(example)]))[0])

    vorhersage = output * train_std[0] + train_mean[0]
    print(
        "Der vorrausichtliche höchste Feinstaubdurchschnitsswert(PM10) für die nächsten 24 Stunden im Raum Graz beträgt ",
        vorhersage[0].max())
   # tf.keras.backend.clear_session()

#prediction(dfModel)

#sys.exit()

