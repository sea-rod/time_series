import streamlit as st
import pandas as pd
from datetime import datetime
from utils import candle_stick_graph,load_data


def graph_1(data):
    st.header("Stock Performance")
    selected_stock = st.selectbox(
        "Select a Stock",
        [col.split("_")[-1] for col in data.columns if "Adj Close_" in col],
    )
    # Line chart for selected stock
    stock_column = f"Adj Close_{selected_stock}"
    if stock_column in data.columns:
        data[stock_column].name = stock_column.strip(r".NS")
        st.line_chart(data[stock_column], height=300, use_container_width=True)


#############################################################################3


def graph_2(data):
    col_1, col_2 = st.columns(2)
    with col_1:
        ticker = st.selectbox("Select Prediction Interval", 
                              options=[col.strip("Close_") for col in data.columns if "Close" in col and "Adj" not in col])
    with col_2:
        period = st.selectbox(
            "Select Prediction Interval", options=["month", "day", "year"]
        )

    with col_1:
        date = st.date_input(
            "Enter begin date", datetime.strptime("06-11-2019", "%d-%m-%Y")
        )

    fig = candle_stick_graph(data, period, date,ticker)
    st.plotly_chart(fig)

data = load_data()
graph_1(data)
graph_2(data)
