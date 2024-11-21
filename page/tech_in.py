import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data


def bollinger_band(data,stock_column):
    # Bollinger Bands
    if stock_column in data.columns:
        st.subheader(f"Bollinger Bands for {selected_stock}")
        df = data[[stock_column]].dropna()
        df["20 Day MA"] = df[stock_column].rolling(window=20).mean()
        df["Upper Band"] = df["20 Day MA"] + (
            df[stock_column].rolling(window=20).std() * 2
        )
        df["Lower Band"] = df["20 Day MA"] - (
            df[stock_column].rolling(window=20).std() * 2
        )
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df.index, df[stock_column], label="Close Price", color="blue")
        ax.plot(df["20 Day MA"], label="20 Day MA", color="orange")
        ax.fill_between(
            df.index, df["Upper Band"], df["Lower Band"], color="gray", alpha=0.2
        )
        ax.legend(loc="upper left")
        st.pyplot(fig)
        return df


def RSI_graph(df, stock_column):
    st.subheader(f"RSI for {selected_stock}")
    if stock_column in data.columns:
        delta = df[stock_column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        st.line_chart(df["RSI"], height=300, use_container_width=True)
        st.caption("RSI: Overbought > 70, Oversold < 30")


data = load_data()

st.header("Technical Indicators")

selected_stock = st.selectbox(
    "Select a Stock for Technical Analysis",
    [col.split("_")[-1] for col in data.columns if "Adj Close_" in col],
)
stock_column = f"Adj Close_{selected_stock}"

df = bollinger_band(data, stock_column)
RSI_graph(df,stock_column)
