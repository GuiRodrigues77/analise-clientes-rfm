# 📊 Análise de Clientes com RFM

Este projeto tem como objetivo analisar o comportamento de clientes utilizando a técnica RFM (Recência, Frequência e Monetário), permitindo identificar padrões de compra e risco de churn.

---

## 🧠 O que foi desenvolvido

- Geração de base de dados simulada com comportamento realista
- Cálculo de métricas RFM
- Segmentação de clientes (VIP, Ativo, Em risco, Inativo)
- Identificação de churn
- Dashboard interativo com Streamlit

---

## 📊 Principais análises

- Distribuição de clientes por segmento
- Receita ao longo do tempo
- Receita por categoria
- Identificação de clientes com risco de churn
- Ranking dos clientes com maior faturamento

---

## 🛠️ Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Streamlit
- Plotly

---

## ▶️ Como executar o projeto

```bash
# Gerar dados
python gerar_base.py

# Calcular RFM
python gerar_rfm.py

# Rodar dashboard
streamlit run dashboard.py
