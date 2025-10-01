import streamlit as st
import pandas as pd
from datetime import datetime

# =============================
# 1) Carregar base de clientes
# =============================

base_belfort = pd.read_excel("BASE DE CLIENTES  CONSULTOR BELFORT.xlsx")

if "Acrônimo" in base_belfort.columns:
    clientes_belfort = base_belfort["Acrônimo"].dropna().unique().tolist()
else:
    st.error("A base de clientes não contém a coluna 'Acrônimo'.")
    st.stop()

# =============================
# 2) Função para puxar rentabilidade do Comdinheiro
# =============================

def get_rentabilidade(acronimo):
    url = f"https://www.comdinheiro.com.br/ExtratoCarteira022.php?&nome_portfolio={acronimo}&data_ini=data_ini_acomp&data_fim=ult_du_mmenos1&layout=3"
    try:
        tabelas = pd.read_html(url, decimal=",", thousands=".")
        return tabelas  # retorna todas as tabelas
    except Exception as e:
        return None

# =============================
# 3) Layout no Streamlit
# =============================

st.set_page_config(page_title="Painel Consultor Belfort", layout="wide")
st.title("📊 Painel de Rentabilidade - Clientes Belfort")

# Seleção de cliente
cliente = st.selectbox("Selecione o cliente:", clientes_belfort)

if cliente:
    tabelas = get_rentabilidade(cliente)

    if tabelas is not None:
        # Descobrir qual tabela contém rentabilidade
        df_rent = tabelas[0]  # pode ser [1] ou [2], ajustar conforme necessário

        # Procurar coluna do ano atual
        ano_atual = str(datetime.today().year)
        colunas_possiveis = [c for c in df_rent.columns if ano_atual in str(c) or "Ano" in str(c)]
        
        rentab_ytd = None
        if colunas_possiveis:
            try:
                rentab_ytd = df_rent[colunas_possiveis[0]].iloc[0]
            except:
                pass

        # KPI principal
        col1, col2 = st.columns(2)
        if rentab_ytd is not None:
            col1.metric(f"Rentabilidade {ano_atual}", f"{rentab_ytd}")
        else:
            col1.warning("Não foi possível identificar a rentabilidade anual acumulada.")

        col2.metric("Cliente", cliente)

        st.markdown("---")
        st.subheader("📈 Detalhamento da Rentabilidade")
        st.dataframe(df_rent, use_container_width=True)

    else:
        st.warning("❌ Não foi possível puxar dados de rentabilidade do Comdinheiro.")

