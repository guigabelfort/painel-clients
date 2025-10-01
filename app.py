import os
import streamlit as st
import pandas as pd

st.title("📊 Painel de Rentabilidade - Consultor Belfort")

# Lista todos os arquivos disponíveis
st.write("📂 Arquivos encontrados no repositório:", os.listdir("."))

# Carrega o Excel se existir
file_name = "BASE DE CLIENTES CONSULTOR BELFORT.xlsx"
if file_name in os.listdir("."):
    base_belfort = pd.read_excel(file_name)
    st.success("Arquivo carregado com sucesso!")
    st.write("Colunas disponíveis:", base_belfort.columns.tolist())
else:
    st.error(f"⚠️ Arquivo '{file_name}' não encontrado no repositório.")
