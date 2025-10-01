import streamlit as st
import pandas as pd

st.title("📊 Painel de Rentabilidade - Consultor Belfort")

# Lê a planilha
try:
    base_belfort = pd.read_excel("BASE DE CLIENTES CONSULTOR BELFORT.xlsx")
except Exception as e:
    st.error(f"Erro ao carregar a base: {e}")
    st.stop()

# Exibe todas as colunas detectadas
st.subheader("Colunas encontradas no Excel")
st.write(base_belfort.columns.tolist())

# Verificação da coluna 'Acrônimo'
if "Acrônimo" in base_belfort.columns:
    clientes_belfort = base_belfort["Acrônimo"].dropna().unique().tolist()
    cliente = st.selectbox("Selecione o cliente:", clientes_belfort)
    st.success(f"Cliente selecionado: {cliente}")
else:
    st.error("⚠️ A base não contém a coluna 'Acrônimo'. Confira acima os nomes disponíveis.")
