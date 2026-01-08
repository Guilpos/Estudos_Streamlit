# dashboard.py
import streamlit as st
import pandas as pd
import requests
import numpy as np

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
    # Tenta conectar na API local
    url = "http://127.0.0.1:8000/vendas"
    params = {}
    if categoria_escolhida != "Todas":
        params = {"categoria": categoria_escolhida}

    try:
        response = requests.get(url, params=params, timeout=2)  # Timeout curto para não travar
        if response.status_code == 200:
            return pd.DataFrame(response.json())
    except Exception as e:
        # Se der erro (API desligada ou rodando na nuvem), entra aqui
        pass

        # --- MODO DEMONSTRAÇÃO (FALLBACK) ---
    # Se chegamos aqui, a API falhou. Vamos gerar dados falsos para o Dashboard não quebrar.
    st.warning(f"⚠️ API Indisponível. Exibindo dados simulados para: {categoria_escolhida}")

    # Gera dados aleatórios parecidos com os da API
    dados_ficticios = []
    produtos_demo = ["Notebook", "Mouse", "Teclado", "Monitor", "Cadeira"]

    for _ in range(20):  # Cria 20 linhas falsas
        dados_ficticios.append({
            "produto": np.random.choice(produtos_demo),
            "categoria": categoria_escolhida if categoria_escolhida != "Todas" else "Mista",
            "preco": np.random.uniform(100, 5000),
            "quantidade_vendida": np.random.randint(1, 10)
        })

    return pd.DataFrame(dados_ficticios)


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