import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run():
    df = pd.read_csv(
        "./assets/xls/empenhos.csv", encoding="ISO-8859-1", sep=";", decimal=","
    )

    colunas_visiveis = [
        "Natureza Despesa",
        "Natureza Despesa Detalhada",
        "Métrica",
        "Empenhado",
        "Liquidado",
    ]

    df = df[colunas_visiveis]
    df["Empenhado"] = (
        df["Empenhado"].str.replace(".", "").str.replace(",", ".").astype(float)
    )
    df["Liquidado"] = (
        df["Liquidado"].str.replace(".", "").str.replace(",", ".").astype(float)
    )

    # Aqui começa o código do nested_pie.py
    st.write("Dataframe Janeiro")
    df_mes = (
        df.groupby(["Natureza Despesa"])[["Empenhado", "Liquidado"]]
        .sum()
        .reset_index()
    )
    df_mes["Pendente"] = df_mes["Empenhado"] - df_mes["Liquidado"]


    # x1 = df_mes[df_mes["Mês"] == "01/2024"]
    x1 = df_mes.copy()
    x1 = x1.sort_values(by="Natureza Despesa")


    fig, ax = plt.subplots()

    size = 0.3
    vals = x1.sort_values(by="Natureza Despesa")["Empenhado"]

    st.write(x1)

    outer_colors = [
        "blue",
        "darkblue",
        "blue",
        "darkblue",
        "blue",
        "darkblue",
        "blue",
        "darkblue",
    ]  # Cores para as fatias externas
    inner_colors = [
        "grey",
        "darkgrey",
        "grey",
        "darkgrey",
        "grey",
        "darkgrey",
        "grey",
        "darkgrey",
        "grey",
        "darkgrey",
        "grey",
        "darkgrey",
        "grey",
        "darkgrey",
        "grey",
        "darkgrey",
    ]

    ax.pie(
        vals,
        labels=x1["Natureza Despesa"],
        radius=1,
        colors=outer_colors,
        wedgeprops=dict(width=size, edgecolor="w"),
        # autopct=lambda pct: f"{int(pct * sum(vals) / 100)}",
    )

    # Transformar dados
    df_melted = pd.melt(
        x1,
        id_vars=["Natureza Despesa"],
        value_vars=["Liquidado", "Pendente"],
        var_name="Tipo",
        value_name="Valor",
    )
    tipo_mapping = {"Liquidado": "L", "Pendente": "P"}
    df_melted["Tipo"] = df_melted["Tipo"].map(tipo_mapping)
    tipo_mapping = {"AUXILIO FINANCEIRO A ESTUDANTES": "AFE",
                    "DIARIAS - PESSOAL CIVIL": "DPC",
                    "LOCACAO DE MAO-DE-OBRA": "LMO",
                    "MATERIAL DE CONSUMO": "MC",
                    "OBRIGACOES TRIBUTARIAS E CONTRIBUTIVAS": "OTC",
                    "OUTROS SERVICOS DE TERCEIROS - PESSOA FISICA": "OSTPF",
                    "OUTROS SERVICOS DE TERCEIROS - PESSOA JURIDICA": "OSTPJ",
                    "SERVICOS DE TECNOLOGIA DA INFORMACAO E COMUNICACAO - PJ": "STIC",
                }
    df_melted["Natureza Despesa"] = df_melted["Natureza Despesa"].map(tipo_mapping)
    df_melted = df_melted.sort_values(["Natureza Despesa", "Tipo"])
    st.write(df_melted)
    ax.pie(
        df_melted.sort_values(["Natureza Despesa", "Tipo"])["Valor"],
        labels=df_melted.sort_values("Natureza Despesa")["Natureza Despesa"],
        radius=1 - size,
        colors=inner_colors,
        wedgeprops=dict(width=size, edgecolor="w"),
        # autopct=lambda pct: f"{int(pct * sum(vals) / 100)}",
        labeldistance=0.5,
        textprops={"fontsize": 5},
    )

    ax.set(aspect="equal", title="Empenhado x Liquidado - Natureza da Despesa")
    st.pyplot(fig)

if __name__ == "__main__":
    run()
