import ofxparse
import pandas as pd
import os
from datetime import datetime

df = pd.DataFrame()
for extrato in os.listdir("extratos"):
    with open(f'extratos/{extrato}', encoding='ISO-8859-1') as ofx_file:
        ofx = ofxparse.OfxParser.parse(ofx_file)
    transactions_data = []

    for account in ofx.accounts:
        for transaction in account.statement.transactions:
            transactions_data.append({
                "Data": transaction.date,
                "Valor": transaction.amount,
                "Descrição": transaction.memo,
                "ID": transaction.id,
            })

    df_temp = pd.DataFrame(transactions_data)
    df_temp["Valor"] = df_temp["Valor"].astype(float)
    df_temp["Data"] = df_temp["Data"].apply(lambda x: x.date())
    df = pd.concat([df, df_temp])
df = df.set_index("ID")
df["Valor"] = 1




# ===============
# LLM

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
template = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados.
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar.

Todos são transações financeiras de uma pessoa física.

Escolha uma dentre as seguintes categorias:
- Alimentação
- Receitas
- Saúde
- Mercado
- Saúde
- Educação
- Compras
- Transporte
- Investimento
- Transferências para terceiros
- Telefone
- Moradia

Escola a categoria deste item:
{text}

Responda apenas com a categoria.
"""

# Local LLM
prompt = PromptTemplate.from_template(template=template)


# Groq
chat = ChatGroq(model="llama-3.1-70b-versatile")
chain = prompt | chat | StrOutputParser()

categorias = chain.batch(list(df["Descrição"].values))
df["Categoria"] = categorias

df = df[df["Data"] >= datetime(2024, 3, 1).date()]
df.to_csv("finances.csv")