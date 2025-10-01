import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Painel de Rentabilidade", layout="wide")

st.title("📊 Painel de Rentabilidade - Consultor Belfort")

# Função para localizar arquivo pelo nome aproximado
def localizar_arquivo(palavra_chave):
    arquivos = os.listdir(".")
    for f in arquivos:
        if palavra_chave.lower() in f.lower():
            return f
    return None

# Localiza os arquivos necessários
arquivo_belfort = localizar_arquivo("BELFORT")
arquivo_cadastro = localizar_arquivo("CADASTRAL")

# Mostra os arquivos encontrados
st.subheader("📂 Arquivos encontrados no repositório:")
st.write(os.listdir("."))

try:
    if not arquivo_belfort:
        st.error("❌ Arquivo da base do Belfort não encontrado no repositório.")
    else:
        base_belfort = pd.read_excel(arquivo_belfort)

        if not arquivo_cadastro:
            st.warning("⚠️ Base cadastral não encontrada, carregando apenas Belfort.")
            base_cadastro = None
        else:
            base_cadastro = pd.read_excel(arquivo_cadastro)

        # Exemplo de visualização simples
        st.success(f"✅ Arquivo '{arquivo_belfort}' carregado com sucesso!")
        st.dataframe(base_belfort.head())

        if base_cadastro is not None:
            st.success(f"✅ Arquivo '{arquivo_cadastro}' carregado com sucesso!")
            st.dataframe(base_cadastro.head())

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
