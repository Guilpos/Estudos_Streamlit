# dashboard.py
import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide", page_title="Dashboard Filtrado")

st.title("🎯 Dashboard com Filtros de API")

# --- 1. SIDEBAR COM FILTROS ---
st.sidebar.header("Configurações")

# Opções fixas para o selectbox
opcoes = ["Todas", "Eletronicos", "Acessorios", "Moveis"]
filtro_selecionado = st.sidebar.selectbox("Selecione a Categoria:", options=opcoes)


# --- 2. COMUNICAÇÃO COM API ---
@st.cache_data(ttl=60)
def carregar_dados(categoria_escolhida):
    # URL base da API
    url = "http://127.0.0.1:8000/vendas"

    # Dicionário de parâmetros (o requests monta a URL pra gente: .../vendas?categoria=X)
    params = {}
    if categoria_escolhida != "Todas":
        params = {"categoria": categoria_escolhida}

    try:
        # A mágica acontece aqui: passamos 'params='
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("Erro na resposta da API")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Erro de conexão! {e}")
        return pd.DataFrame()


# Chamada da função passando o filtro da sidebar
df = carregar_dados(filtro_selecionado)

# --- 3. EXIBIÇÃO ---
if not df.empty:
    st.info(f"Exibindo resultados para: **{filtro_selecionado}**")

    # Métricas
    receita_total = (df['preco'] * df['quantidade_vendida']).sum()
    col1, col2 = st.columns(2)
    col1.metric("Total de Vendas (Qtd)", df['quantidade_vendida'].sum())
    col2.metric("Receita Total", f"R$ {receita_total:,.2f}")

    st.divider()

    # Gráfico e Tabela
    col_graf, col_tab = st.columns([2, 1])

    with col_graf:
        st.bar_chart(df, x="produto", y="quantidade_vendida")

    with col_tab:
        st.dataframe(df, hide_index=True)
else:
    st.warning("Nenhum dado encontrado ou erro na conexão.")