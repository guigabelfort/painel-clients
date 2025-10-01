import streamlit as st
import pandas as pd
import numpy as np
import random

# -------------------------------
# Geração de base fictícia de clientes
# -------------------------------

np.random.seed(42)
clientes = [f"Cliente {i+1}" for i in range(80)]
patrimonios = np.random.randint(200000, 5000000, size=80)
rentabilidades = np.round(np.random.normal(6, 5, 80), 2)  # média 6%, desvio 5%
perfis = np.random.choice(["Conservador", "Moderado", "Arrojado"], size=80, p=[0.3, 0.5, 0.2])
instituicoes = np.random.choice(["XP", "BTG", "Avenue", "Itaú", "Nenhuma"], size=80, p=[0.25, 0.25, 0.2, 0.15, 0.15])

df = pd.DataFrame({
    "Cliente": clientes,
    "Patrimônio (R$)": patrimonios,
    "Rentabilidade YTD (%)": rentabilidades,
    "Perfil": perfis,
    "Instituição Externa": instituicoes
})

# -------------------------------
# Layout Streamlit
# -------------------------------

st.set_page_config(page_title="Painel de Clientes", layout="wide")

st.title("📊 Painel de Gestão de Clientes")

# KPIs principais
col1, col2, col3, col4 = st.columns(4)
col1.metric("Clientes sob gestão", len(df))
col2.metric("PL Total", f"R$ {df['Patrimônio (R$)'].sum():,.0f}")
col3.metric("Rentabilidade Média YTD", f"{df['Rentabilidade YTD (%)'].mean():.2f}%")
col4.metric("Clientes com instituição externa", f"{(df['Instituição Externa'] != 'Nenhuma').sum()}")

st.markdown("---")

# Filtros
col_f1, col_f2 = st.columns(2)
perfil_filter = col_f1.multiselect("Filtrar por perfil de risco:", options=df["Perfil"].unique(), default=df["Perfil"].unique())
inst_filter = col_f2.multiselect("Filtrar por instituição externa:", options=df["Instituição Externa"].unique(), default=df["Instituição Externa"].unique())

df_filtered = df[(df["Perfil"].isin(perfil_filter)) & (df["Instituição Externa"].isin(inst_filter))]

# Tabela interativa
st.subheader("📋 Lista de Clientes")
st.dataframe(df_filtered, use_container_width=True)

# Drill-down cliente
st.markdown("---")
st.subheader("🔍 Detalhamento de Cliente")

cliente = st.selectbox("Selecione um cliente:", df_filtered["Cliente"])
info = df[df["Cliente"] == cliente].iloc[0]

st.write(f"### {info['Cliente']}")
st.write(f"**Patrimônio:** R$ {info['Patrimônio (R$)']:,}")
st.write(f"**Rentabilidade YTD:** {info['Rentabilidade YTD (%)']}%")
st.write(f"**Instituição Externa:** {info['Instituição Externa']}")
st.write(f"**Perfil de Risco:** {info['Perfil']}")
