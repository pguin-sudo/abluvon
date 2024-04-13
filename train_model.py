from __future__ import division

import json

import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Conv1D, Flatten, MaxPooling1D, LSTM
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

from config import Tokens


def load_binance_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    data = data['binance']
    df = pd.DataFrame.from_dict(data)
    df.index = pd.to_datetime(data.index)

    return data


start_date = datetime.datetime(1973, 1, 1)
end_date = datetime.datetime(2011, 3, 31)


df = pd.read_csv(f"data/{Tokens.pairs}.csv")
df.index = pd.to_datetime(df["Date"])
df = df.drop("Date", axis=1)

dfm = df.resample("M").mean()

dfm = dfm[:-1]

print(dfm.head())
print(dfm.tail())
