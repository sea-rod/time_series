import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    print("heelo")
    return pd.read_csv("stocks_data.csv",parse_dates=['Date'],index_col='Date')

@st.cache_resource
def load_model():
    return tf.keras.models.load_model("model.keras")


plt.style.use(["dark_background"])

def prediction_vs_actual(y_pred, data):


    fig, ax = plt.subplots(figsize=(6, 2))
    # fig.figure(figsize=(12,6))
    ax.set_title("Predicted v/s Actual")
    ax.patch.set_alpha(0)
    fig.patch.set_alpha(0)
    look_back = 100
    trainPredictPlot = np.empty_like(data)
    trainPredictPlot[:, :] = np.nan
    # trainPredictPlot[look_back:, :] = y_pred

    # plot baseline and predictions
    ax.plot(data, color="blue",label="Actual")
    ax.plot(y_pred, color="red",label="Predicted")
    return fig

def candle_stick_graph(df, month,date,ticker):
    date = pd.Timestamp(date).tz_localize(df.index.tz)
    df_filtered = df[date:]
    dic = {"year": "Ye", "month": "ME", "day": "D"}
    df = df_filtered.resample(dic[month]).mean()
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                    open=df[f"Open_{ticker}"],
                high=df[f"High_{ticker}"],
                low=df[f"Low_{ticker}"],
                close=df[f"Close_{ticker}"],
                increasing_line_color="green",
                decreasing_line_color="red",
            )
        ]
    )
    # fig.update_layout(yaxis_range=[0,30000])
    return fig
