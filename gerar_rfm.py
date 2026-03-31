import pandas as pd
import os

os.makedirs("data", exist_ok=True)

# carregar dados
df_vendas = pd.read_csv("data/vendas.csv")
df_clientes = pd.read_csv("data/clientes.csv")

# converter data
df_vendas["data_compra"] = pd.to_datetime(df_vendas["data_compra"])

# juntar dados
df = df_vendas.merge(df_clientes, on="cliente_id", how="left")

# data de referência (última compra)
data_ref = df["data_compra"].max()


# calcular RFM
rfm = df.groupby(["cliente_id", "empresa"]).agg({
    "data_compra": lambda x: (data_ref - x.max()).days,
    "valor_compra": ["count", "sum"]
})

# nomes simples
rfm.columns = ["dias_sem_compra", "frequencia", "faturamento_total"]
rfm = rfm.reset_index()

# ticket médio
rfm["ticket_medio"] = rfm["faturamento_total"] / rfm["frequencia"]


# scores (1 a 5)
rfm["r_score"] = pd.qcut(
    rfm["dias_sem_compra"].rank(method="first"),
    5,
    labels=[5,4,3,2,1]
)

rfm["f_score"] = pd.qcut(
    rfm["frequencia"].rank(method="first"),
    5,
    labels=[1,2,3,4,5]
)

rfm["m_score"] = pd.qcut(
    rfm["faturamento_total"].rank(method="first"),
    5,
    labels=[1,2,3,4,5]
)

# score final
rfm["rfm_score"] = (
    rfm["r_score"].astype(str) +
    rfm["f_score"].astype(str) +
    rfm["m_score"].astype(str)
)


# classificação
def classificar(row):
    if row["r_score"] == 5 and row["f_score"] >= 4:
        return "VIP"
    elif row["r_score"] >= 4:
        return "Ativo"
    elif row["r_score"] >= 3:
        return "Em risco"
    else:
        return "Inativo"

rfm["classificacao_rfm"] = rfm.apply(classificar, axis=1)

# churn
rfm["churn"] = rfm["dias_sem_compra"] > 90

# salvar
rfm.to_csv("data/analise_clientes.csv", index=False)

print("RFM gerado com sucesso!")