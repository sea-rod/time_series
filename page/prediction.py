import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from utils import prediction_vs_actual, load_data, load_model
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime


def feature_engineering(data, timestamp=100):
    x = []
    y = []
    for i in range(len(data) - timestamp):
        x.append(data[i : i + timestamp])
        y.append(data[i + timestamp])
    return np.array(x), np.array(y)


model = load_model()
data = load_data()

ticker = st.selectbox(
    "Select Prediction Interval",
    options=[
        col.strip("Adj") for col in data.columns if "Close" in col and "Adj" not in col
    ],
)

days = st.sidebar.slider("days",min_value=0,max_value=30)

scaler = MinMaxScaler(feature_range=(0, 1))
y_ = scaler.fit_transform(data[[f"{ticker}"]].dropna())
x, y = feature_engineering(y_)
y_pred = model.predict(x)

for i in range(days):
    yp = model.predict(y_[-100:].reshape(-1, 100, 1))
    y_ = np.vstack((y_, yp))
    y_pred = np.vstack((y_pred, yp))

# x = scaler.inverse_transform(x)
y = scaler.inverse_transform(y)
y_pred = scaler.inverse_transform(y_pred)

y = np.vstack((y, np.full((days, 1), np.nan)))
st.line_chart(np.hstack((y_pred, y)))
