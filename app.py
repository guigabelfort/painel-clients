import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Painel de Rentabilidade", layout="wide")

st.title("📊 Painel de Rentabilidade - Consultor Belfort")

# ===============================
# 1. Checar arquivos disponíveis
# ===============================
st.subheader("Arquivos encontrados no repositório:")
st.write(os.listdir("."))  # Mostra todos os arquivos que o Streamlit enxerga

# Nome EXATO do arquivo (atenção: há dois espaços no nome original)
file_name = "BASE DE CLIENTES  CONSULTOR  BELFORT.xlsx"

# ===============================
# 2. Carregar base de clientes Belfort
# ===============================
try:
    base_belfort = pd.read_excel(file_name)
    st.success(f"✅ Arquivo '{file_name}' carregado com sucesso!")

    # Mostrar colunas disponíveis
    st.subheader("Colunas detectadas na planilha:")
    st.write(base_belfort.columns.tolist())

    # ===============================
    # 3. Verificar coluna de Acrônimo
    # ===============================
    if "Acrônimo" in base_belfort.columns:
        clientes = base_belfort["Acrônimo"].dropna().unique().tolist()
        cliente_sel = st.selectbox("Selecione um cliente:", clientes)
        st.info(f"🔎 Cliente selecionado: **{cliente_sel}**")

        # Aqui futuramente vamos puxar a rentabilidade real do cliente (via Comdinheiro/API)
        st.metric(label="Rentabilidade YTD", value="⏳ Em construção")

    else:
        st.error("⚠️ A planilha não contém a coluna 'Acrônimo'. Verifique os nomes listados acima.")

except Exception as e:
    st.error(f"Erro ao carregar a base: {e}")
