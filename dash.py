import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


df = pd.read_csv("finances.csv")
del df["ID"]
df["Mês"] = df["Data"].apply(lambda x: "-".join(x.split("-")[:-1]))
df["Data"] = pd.to_datetime(df["Data"])
df["Data"] = df["Data"].apply(lambda x: x.date())
df = df[df["Categoria"]!="Receitas"]
df["Valor"] = 1

def filter_data(df, mes, selected_categories):
    df_filtered = df[df['Mês'] == mes]
    if selected_categories:
        df_filtered = df_filtered[df_filtered['Categoria'].isin(selected_categories)]
    return df_filtered

# Título do Dashboard
st.title("Dashboard de Finanças Pessoais")

# Filtros de data
st.sidebar.header("Filtros")

# Definir intervalo de data
mes = st.sidebar.selectbox("Mês", df["Mês"].unique())


# Filtro de categoria
categories = df["Categoria"].unique().tolist()
selected_categories = st.sidebar.multiselect("Filtrar por Categorias", categories, default=categories)

df_filtered = filter_data(df, mes, selected_categories)


# ====================
c1, c2 = st.columns([0.6, 0.4])

# c1.subheader("Tabela de Finanças Filtradas")
c1.dataframe(df_filtered)
 

# c2.subheader("Distribuição de Categorias")
category_distribution = df_filtered.groupby("Categoria")["Valor"].sum().reset_index()
fig = px.pie(category_distribution, values='Valor', names='Categoria', 
            title='Distribuição por Categoria', hole=0.3
                )
c2.plotly_chart(fig, use_container_width=True)