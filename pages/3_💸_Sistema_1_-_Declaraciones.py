import streamlit as st
import unblind.dataviz as dv
import pandas as pd

@st.cache
def get_data(url):
    return pd.read_csv(url)