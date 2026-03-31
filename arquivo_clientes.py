import pandas as pd
import os

# Garantir pasta
os.makedirs("data", exist_ok=True)


# Carregar dados
df_vendas = pd.read_csv("data/vendas.csv")
df_clientes = pd.read_csv("data/clientes.csv")

df_vendas["data_compra"] = pd.to_datetime(df_vendas["data_compra"])

df = df_vendas.merge(df_clientes, on="cliente_id", how="left")

# Data de referência (última data do dataset)
data_ref = df["data_compra"].max()


# Cálculo RFM
rfm = df.groupby(["cliente_id", "empresa"]).agg({
    "data_compra": lambda x: (data_ref - x.max()).days, 
    "valor_compra": ["count", "sum"]  
})

rfm.columns = ["dias_sem_compra", "qtd_pedidos", "faturamento_total"]

# Reset index (transformar em colunas)
rfm = rfm.reset_index()

# Ticket médio
rfm["valor_medio_pedido"] = rfm["faturamento_total"] / rfm["qtd_pedidos"]


# Classificação RFM
def classificar_cliente(row):
    if row["dias_sem_compra"] <= 30 and row["qtd_pedidos"] >= 10:
        return "VIP"
    elif row["dias_sem_compra"] <= 60:
        return "Ativo"
    elif row["dias_sem_compra"] <= 120:
        return "Em risco"
    else:
        return "Inativo"

rfm["classificacao_rfm"] = rfm.apply(classificar_cliente, axis=1)


# Renomear colunas finais
rfm.rename(columns={
    "cliente_id": "id_cliente",
    "empresa": "nome_empresa"
}, inplace=True)


# Outputs
print("\n VISÃO GERAL:")
print(rfm.describe())

print("\n CLIENTES POR SEGMENTO:")
print(rfm["classificacao_rfm"].value_counts())

print("\n TOP CLIENTES:")
print(rfm.sort_values(by="faturamento_total", ascending=False).head(10))

# Salvar CSV final
rfm.to_csv("data/analise_clientes.csv", index=False)

print("\n Análise salva em data/analise_clientes.csv")