import streamlit as st
import unblind.dataviz as dv
import pandas as pd

@st.cache
def get_data(url):
    return pd.read_csv(url)

s2 = get_data('https://raw.githubusercontent.com/Dataket/unblind/master/data/process_data/s2/ut_ug_m_data.csv?raw=true')

if st.checkbox('Mostrar datos completos 🤔'):
    st.write(s2)
