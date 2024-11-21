import streamlit as st
import numpy as np
import pandas as pd
from utils import load_data, load_model
from sklearn.preprocessing import MinMaxScaler


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

days = st.sidebar.slider("days", min_value=0, max_value=30)

data = data[[f"{ticker}"]].dropna()
scaler = MinMaxScaler(feature_range=(0, 1))
df = scaler.fit_transform(data)
x, y = feature_engineering(df)
y_pred = model.predict(x)

for i in range(days):
    yp = model.predict(df[-100:].reshape(-1, 100, 1))
    df = np.vstack((df, yp))
    y_pred = np.vstack((y_pred, yp))

y = scaler.inverse_transform(y)
y_pred = scaler.inverse_transform(y_pred)

y = np.vstack((y, np.full((days, 1), np.nan)))
new_dates = pd.date_range(data.index[-1] + pd.Timedelta(days=1), periods=days)

pred_vs_actual = pd.DataFrame(
    np.hstack((y_pred, y)),
    columns=["predicted", "actual"],
    index=data.index.append(new_dates)[100:]
)
st.line_chart(pred_vs_actual, color=("#33daff", "#ff5733"))
