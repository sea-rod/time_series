import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

def historical_nifty_it(data):
    # st.title("Nifty IT Stock Analysis Dashboard")
    # st.header("Index Overview")
    data = data[["Adj Close_^CNXIT"]].dropna()
    st.subheader("Nifty IT Historical Trend")
    st.line_chart(data["Adj Close_^CNXIT"], height=300, use_container_width=True)


def top_performers(data):
    st.subheader("Top Performers and Laggards in 2024")
    data_2024 = data.loc["2024"]
    
    returns = (data_2024.filter(like="Adj Close_").pct_change(fill_method=None) + 1).cumprod()
    final_returns = returns.iloc[-1].sort_values(ascending=False)
    final_returns.name = final_returns.name.strftime("%Y-%m-%d")

    top_performers = final_returns.head(5)
    laggards = final_returns.tail(5)
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(data=top_performers, height=300, use_container_width=True)
        st.caption("<p style=text-align:center>Top Performers</p>", unsafe_allow_html=True)
    with col2:
        st.bar_chart(laggards, height=300, use_container_width=True)
        st.caption("<p style=text-align:center>Laggards</p>", unsafe_allow_html=True)


data = load_data()
historical_nifty_it(data)
top_performers(data)
