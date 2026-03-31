import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

os.makedirs("data", exist_ok=True)

np.random.seed(42)
random.seed(42)

NUM_CLIENTES = 200
DATA_INICIO = datetime(2024, 1, 1)
DATA_FIM = datetime(2024, 12, 31)

categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Casa', 'Esportes']

nomes_empresas = [
    "Tech Solutions", "Alpha Corp", "Nova Digital", "Prime Systems",
    "InovaTech", "Global Services", "NextGen", "Smart Solutions",
    "Vision Tech", "DataCorp", "Future Systems", "CloudX"
]

# ---------------------------
# Criar clientes
# ---------------------------
clientes = []

for i in range(1, NUM_CLIENTES + 1):
    renda = round(np.random.uniform(1500, 15000), 2)

    cliente = {
        "cliente_id": i,
        "empresa": random.choice(nomes_empresas),
        "idade": np.random.randint(18, 70),
        "renda_mensal": renda
    }
    clientes.append(cliente)

df_clientes = pd.DataFrame(clientes)
df_clientes.to_csv("data/clientes.csv", index=False)

# ---------------------------
# Criar vendas com comportamento mais realista
# ---------------------------
compras = []

def gerar_categoria_por_renda(renda):
    if renda > 10000:
        return np.random.choice(['Eletrônicos', 'Casa'])
    elif renda > 5000:
        return np.random.choice(['Roupas', 'Esportes'])
    else:
        return np.random.choice(['Alimentos', 'Roupas'])

for _, cliente in df_clientes.iterrows():

    renda = cliente["renda_mensal"]

    # variação de comportamento (cliente pode comprar mais ou menos que a média)
    fator_comportamento = np.random.uniform(0.5, 1.5)

    base_compras = int(np.clip((renda / 2000) * fator_comportamento, 1, 25))

    # garante que nunca dá erro
    if base_compras == 1:
        num_compras = 1
    else:
        num_compras = np.random.randint(1, base_compras + 1)

    for _ in range(num_compras):

        # data aleatória no ano
        dia_aleatorio = np.random.randint(0, (DATA_FIM - DATA_INICIO).days)
        data_compra = DATA_INICIO + timedelta(days=dia_aleatorio)

        # valor baseado na renda
        valor_base = renda * np.random.uniform(0.01, 0.08)
        valor_compra = round(np.random.uniform(valor_base * 0.5, valor_base * 1.5), 2)

        compra = {
            "cliente_id": cliente["cliente_id"],
            "data_compra": data_compra,
            "valor_compra": valor_compra,
            "categoria": gerar_categoria_por_renda(renda)
        }

        compras.append(compra)

df_vendas = pd.DataFrame(compras)
df_vendas["data_compra"] = pd.to_datetime(df_vendas["data_compra"])

df_vendas.to_csv("data/vendas.csv", index=False)

print("Bases geradas com comportamento mais realista!")
print("Clientes:", df_clientes.shape)
print("Vendas:", df_vendas.shape)