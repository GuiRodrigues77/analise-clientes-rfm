import streamlit as st
import pandas as pd
import plotly.express as px

# página
st.set_page_config(page_title="Dashboard de Clientes", layout="wide")

st.title("Análise de Clientes")

st.markdown("""
Análise de comportamento de clientes usando RFM (Recência, Frequência e Valor).
""")

# carregar dados
df = pd.read_csv("data/vendas.csv")
rfm = pd.read_csv("data/analise_clientes.csv")


# churn
st.subheader("Análise de Churn")

def classificar_churn(dias):
    if dias <= 30:
        return "Ativo"
    elif dias <= 60:
        return "Atenção"
    else:
        return "Churn"

rfm["status_churn"] = rfm["dias_sem_compra"].apply(classificar_churn)

churn_counts = rfm["status_churn"].value_counts()

col1, col2, col3 = st.columns(3)
col1.metric("Ativos", churn_counts.get("Ativo", 0))
col2.metric("Atenção", churn_counts.get("Atenção", 0))
col3.metric("Churn", churn_counts.get("Churn", 0))

fig = px.pie(
    names=churn_counts.index,
    values=churn_counts.values,
    title="Churn"
)
st.plotly_chart(fig)


# KPIs
st.subheader(" Visão Geral")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Clientes", rfm["cliente_id"].nunique())
col2.metric("Compras", len(df))
col3.metric("Faturamento", f"R$ {df['valor_compra'].sum():,.2f}")
col4.metric("Ticket médio", f"R$ {df['valor_compra'].mean():,.2f}")


# receita por mês
st.subheader("Receita por mês")

df["data_compra"] = pd.to_datetime(df["data_compra"])
df["mes"] = df["data_compra"].dt.to_period("M").astype(str)

receita = df.groupby("mes")["valor_compra"].sum()
st.line_chart(receita)


# categorias
st.subheader("Receita por categoria")

categoria = df.groupby("categoria")["valor_compra"].sum()
st.bar_chart(categoria)

# ---------------------------
# segmentos
# ---------------------------
st.subheader("Clientes por segmento")

segmento = rfm["classificacao_rfm"].value_counts()
st.bar_chart(segmento)


# top clientes
st.subheader("Top clientes")

top = rfm.sort_values(by="faturamento_total", ascending=False).head(10)
st.dataframe(top)


# dados
st.subheader("Dados")

st.dataframe(rfm)