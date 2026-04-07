from sqlalchemy import create_engine
import plotly.express as px
import numpy as np
import pandas as pd
import streamlit as st
st.set_page_config(page_title="ENEM 2024", layout="wide")

st.set_page_config(layout="wide")
st.title("📊 Análise do ENEM 2024")
st.markdown(
    "Painel interativo para exploração das notas por UF e faixa de valores.")

# ===== TENTAR CONEXÃO
try:
    engine = create_engine(
        'postgresql://data_iesb:iesb@bigdata.dataiesb.com/iesb')

    df = pd.read_sql("""
        SELECT sg_uf_esc, nota_media_5_notas
        FROM ed_enem_2024_resultados_amos_per
    """, engine)

    st.success("Conectado ao banco!")

except:
    st.warning("Usando dados simulados")

    np.random.seed(0)
    df = pd.DataFrame({
        "sg_uf_esc": np.random.choice(["DF", "SP", "RJ", "MG"], 1000),
        "nota_media_5_notas": np.random.normal(500, 100, 1000)
    })

# ===== FILTROS
st.sidebar.header("⚙️ Filtros")

ufs = st.sidebar.multiselect(
    "Selecione a UF",
    df["sg_uf_esc"].unique(),
    default=df["sg_uf_esc"].unique()
)

nota_min, nota_max = st.sidebar.slider(
    "Faixa de nota",
    int(df["nota_media_5_notas"].min()),
    int(df["nota_media_5_notas"].max()),
    (300, 700)
)

# ===== FILTRO
df_filtrado = df[
    (df["sg_uf_esc"].isin(ufs)) &
    (df["nota_media_5_notas"] >= nota_min) &
    (df["nota_media_5_notas"] <= nota_max)
]
colA, colB = st.columns(2)
colA.metric("Total de Registros", len(df_filtrado))
colB.metric("Média das Notas", round(
    df_filtrado["nota_media_5_notas"].mean(), 2))

# ===== GRÁFICOS
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(df_filtrado, x="nota_media_5_notas",
                        nbins=30, title="Histograma das Notas")
    fig1.update_layout(title="Distribuição das Notas (Histograma)")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.box(df_filtrado, x="sg_uf_esc",
                  y="nota_media_5_notas", title="Boxplot por UF")
    fig2.update_layout(title="Distribuição das Notas por UF (Boxplot)")
    st.plotly_chart(fig2, use_container_width=True)

# ===== ESTATÍSTICAS
st.subheader("Estatísticas")
st.write(df_filtrado["nota_media_5_notas"].describe())
