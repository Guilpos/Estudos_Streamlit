import streamlit as st
import pandas as pd
import numpy as np

# Configuração da Página (Sempre o primeiro comando)
st.set_page_config(page_title="Revisão Streamlit", layout="wide")

# --- 1. BARRA LATERAL (SIDEBAR) PARA FILTROS ---
st.sidebar.header("Filtros do Dashboard")
st.sidebar.write("Use os widgets abaixo para controlar a página.")

user_name = st.sidebar.text_input("Digite seu nome", "Dev Python")
category_filter = st.sidebar.selectbox("Escolha a Categoria: ", ["Vendas", "Marketing", "TI"])
show_data = st.sidebar.checkbox("Mostrar dados brutos", value=True)
slider_data = st.sidebar.slider(label="Slider", min_value=0, max_value=100, value=30)


# --- 2. ÁREA PRINCIPAL ---
st.title(f"Bem vindo, {user_name}!")
st.markdown(f"Você está visualizando o painel de **{category_filter}**")

# Simulando dados simples com Pandas
df = pd.DataFrame(
    np.random.randint(0, 100, size=(3, 20)),
    columns=["Vendas", "Custos", "Lucro"]
)

# --- APLICAÇÃO DO FILTRO (O SEGREDO) ---
# Aqui usamos a variável do seu slider para filtrar o Pandas
df_filtrado = df[df['Vendas'] > slider_data]

# --- 3. LAYOUT EM COLUNAS (METRICAS) ---
# --- VISUALIZAÇÃO ---
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Valores de Vendas > {slider_data}")
    # Note que agora passamos o df_filtrado, não o df original
    st.line_chart(df_filtrado['Vendas'])

with col2:
    st.subheader("Tabela Filtrada")
    if show_data:
        st.dataframe(df_filtrado, use_container_width=True)
        # Mostra quantos registros sobraram
        st.caption(f"Exibindo {len(df_filtrado)} registros de 20.")

# --- 4. ABAS E DADOS (TABS) ---
st.divider()
tab1, tab2, tab3 = st.tabs("📊 Gráficos", "📋 Dados")


with tab1:
    st.subheader("Análise Visual")
    st.line_chart(df)
    st.info("Este gráfico é gerado automaticamente a partir do DataFrame.")
with tab2:
    st.subheader("Dados detalhados")
    if show_data:
        st.dataframe(df, use_containter_width=True)
    else:
        st.warning("A Visualização de Dados está desativada no sidebar.")

# --- 5. INTERATIVIDADE EXTRA ---
with st.expander("Ver explicação técnica"):
    st.write("""
        - A Sidebar controla as variáveis globais.
        - As colunas organizam  os KPIs no topo.
        - As abas separam Visualização de Dados Brutos.
    """)
