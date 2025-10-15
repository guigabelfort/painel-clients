from etl import carrega_base, merge_bases
import pandas as pd

# Ex.: cache para acelerar no Streamlit (se usar Streamlit)
try:
    import streamlit as st
    @st.cache_data
    def load_data():
        df1 = carrega_base("BASE DE CLIENTES CONSULTOR BELFORT.xlsx")
        df2 = carrega_base("BASE-CADASTRAL-CLIENTES.xlsx")
        df, _ = merge_bases(df1, df2)
        return df
    df = load_data()
except ImportError:
    # fallback se não estiver usando Streamlit
    df1 = carrega_base("BASE DE CLIENTES CONSULTOR BELFORT.xlsx")
    df2 = carrega_base("BASE-CADASTRAL-CLIENTES.xlsx")
    df, _ = merge_bases(df1, df2)
