import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# st.set_page_config(layout="wide")


pages = {
    "Menu": [
        st.Page("page/overview.py", title="Overview"),
        st.Page("page/stock_performance.py", title="Stock Performance"),
        st.Page("page/tech_in.py", title="Tech Indicator"),
        st.Page("page/prediction.py", title="Prediction"),
    ]
}


pg = st.navigation(pages)
pg.run()
