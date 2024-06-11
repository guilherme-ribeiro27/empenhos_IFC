import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit.logger import get_logger
from utils import *

LOGGER = get_logger(__name__)

class DataframeManager:
    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        if "error_message" not in st.session_state:
            st.session_state.error_message = ''
        if "df_master" not in st.session_state:
            st.session_state.df_master = pd.read_csv("assets/xls/empenhos.csv", encoding='ISO-8859-1', sep=";", decimal=",")
        if "month" not in st.session_state:
            st.session_state.month = "01"

    def get_df_month_values(self, months):
        self.to_float()
        visible_columns = [
            'Natureza Despesa',
            'Mês',
            'Empenhado',
            'Liquidado',
        ]

        df = st.session_state.df_master[visible_columns]
        if isinstance(months, str):
            months = [months]

        df_month_values = df[df["Mês"].isin(months)]
        visible_columns = [
            'Natureza Despesa',
            'Empenhado',
            'Liquidado',
        ]
        df_month_values = df_month_values[visible_columns]
        df_month_values = (
            df_month_values.groupby(["Natureza Despesa"])[
                ["Empenhado", "Liquidado"]
            ]
            .sum()
            .reset_index()
        )
        total_empenhado = df_month_values["Empenhado"].sum()
        total_liquidado = df_month_values["Liquidado"].sum()
        df_total = pd.DataFrame({"Natureza Despesa": ["Total"], "Empenhado": [total_empenhado], "Liquidado": [total_liquidado]})
        df_month_values = pd.concat([df_month_values, df_total])
        df_month_values["Empenhado"] = df_month_values["Empenhado"].map("R$ {:,.2f}".format)
        df_month_values["Liquidado"] = df_month_values["Liquidado"].map("R$ {:,.2f}".format)

        return df_month_values

    def get_df_month_monetary_values(self, months, tipo):
        self.to_float()
        visible_columns = [
            "Natureza Despesa",
            "Mês",
            "Empenhado",
            "Liquidado",
        ]

        df = st.session_state.df_master[visible_columns]
        df_month_values = df[df["Mês"].isin(months)]
        df_month_values = (
            df_month_values.groupby(["Mês", "Natureza Despesa"])[["Empenhado", "Liquidado"]]
            .sum()
            .reset_index()
        )
        visible_columns = [
            "Natureza Despesa",
            "Empenhado",
            "Liquidado",
        ]
        df_month_values = df_month_values[visible_columns]
        df_month_values = (
            df_month_values.groupby(["Natureza Despesa"])[
                ["Empenhado", "Liquidado"]
            ]
            .sum()
            .reset_index()
        )
        raw_datas = df_month_values.copy()

        visible_columns = ["Natureza Despesa", tipo]
        raw_datas = raw_datas[visible_columns]
        return raw_datas

    def get_df_month_detail(self, value='Empenhado'):
        self.to_float()
        visible_columns = [
            'Natureza Despesa',
            'Mês',
            'Empenhado',
            'Liquidado',
        ]

        df = st.session_state.df_master[visible_columns]
        df_month_detail = df.groupby(['Mês', 'Natureza Despesa'])[['Empenhado', 'Liquidado']].sum().reset_index()
        df_month_detail['Empenhado (R$)'] = st.session_state.df_master['Empenhado'].map('R$ {:,.2f}'.format)
        df_month_detail['Liquidado (R$)'] = st.session_state.df_master['Liquidado'].map('R$ {:,.2f}'.format)
        pivoted = pd.pivot_table(df_month_detail, values=value, index='Natureza Despesa', columns='Mês')
        pivoted = pivoted.fillna(0)
        raw_datas = pivoted.reset_index()

        formatted_datas = pivoted.copy()
        formatted_columns = {col: formatted_months(col) for col in formatted_datas.columns}
        formatted_datas = formatted_datas.rename(columns=formatted_columns).applymap(lambda x: 'R$ {:,.2f}'.format(x))

        return [raw_datas, formatted_datas]

    def get_options_main(self):
        self.to_float()
        visible_columns = [
            'Mês',
            'Empenhado',
            'Liquidado',
        ]

        df = st.session_state.df_master[visible_columns]
        df_main = df.groupby(['Mês'])[['Empenhado', 'Liquidado']].sum().reset_index()
        df_main["Empenhado (R$)"] = df_main["Empenhado"].map("R$ {:,.2f}".format)
        df_main["Liquidado (R$)"] = df_main["Liquidado"].map("R$ {:,.2f}".format)
        df_main['Mês'] = df_main['Mês'].map(lambda x: formatted_months(x))

        return [{
            "title": {"text": ""},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": ["Liquidado", "Empenhado"], "left": "1%"},
            "grid": {"left": "1%", "right": "2%", "bottom": "3%", "containLabel": True},
            "toolbox": {"feature": {"saveAsImage": {}}},
            "xAxis": {
                "type": "category",
                "boundaryGap": False, 
                "axisLabel": {"margin": 20 }, 
                "data": df_main['Mês'].tolist(),
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "name": "Liquidado",
                    "type": "line",
                    "stack": "Liquidado",
                    "smooth": True,
                    "data": df_main['Liquidado'].tolist(),
                },
                {
                    "name": "Empenhado",
                    "type": "line",
                    "stack": "Empenhado",
                    "smooth": True,
                    "data": df_main['Empenhado'].tolist(),
                },
            ],
        }, df_main[['Mês', 'Empenhado (R$)', 'Liquidado (R$)']]]

    def get_df_by_all_nature(self):
        self.to_float()
        visible_columns = [
            'Natureza Despesa',
            'Empenhado',
            'Liquidado',
        ]

        all_nature = st.session_state.df_master['Natureza Despesa'].unique().tolist()
        df = st.session_state.df_master[visible_columns]
        df_by_all_nature = df[df['Natureza Despesa'].isin(all_nature)]
        df_by_all_nature = df_by_all_nature.groupby(['Natureza Despesa'])[['Empenhado', 'Liquidado']].sum().reset_index()

        option2 = {
            "yAxis": {
                "type": 'category',
                "data": df_by_all_nature['Natureza Despesa'].tolist()
            },
            "series": [
                {
                "name": 'Empenhado',
                "type": 'bar',
                "emphasis": {
                    "focus": 'series'
                },
                "data": df_by_all_nature['Empenhado'].tolist()
                },
                {
                "name": 'Liquidado',
                "type": 'bar',
                "emphasis": {
                    "focus": 'series'
                },
                "data": df_by_all_nature['Liquidado'].tolist()
                }
            ]
        }

        df_by_all_nature['Empenhado'] = df_by_all_nature['Empenhado'].map('R$ {:,.2f}'.format)
        df_by_all_nature['Liquidado'] = df_by_all_nature['Liquidado'].map('R$ {:,.2f}'.format)

        return [option2, df_by_all_nature]
    
    def get_df_by_nature(self, nature):
        if nature == []:
            return [{}, pd.DataFrame()]
        self.to_float()
        visible_columns = [
            'Natureza Despesa',
            'Natureza Despesa Detalhada',
            'Empenhado',
            'Liquidado',
        ]

        df = st.session_state.df_master[visible_columns]
        df_by_nature = df[df['Natureza Despesa'] == (nature)]
        visible_columns = [
            'Natureza Despesa Detalhada',
            'Empenhado',
            'Liquidado',
        ]
        df_by_nature = df_by_nature.groupby(['Natureza Despesa Detalhada'])[['Empenhado', 'Liquidado']].sum().reset_index()

        option = {
            "yAxis": {
                "type": 'category',
                "data": df_by_nature['Natureza Despesa Detalhada'].tolist()
            },
            "series": [
                {
                "name": 'Empenhado',
                "type": 'bar',
                "emphasis": {
                    "focus": 'series'
                },
                "data": df_by_nature['Empenhado'].tolist()
                },
                {
                "name": 'Liquidado',
                "type": 'bar',
                "emphasis": {
                    "focus": 'series'
                },
                "data": df_by_nature['Liquidado'].tolist()
                }
            ]
        }

        df_by_nature['Empenhado'] = df_by_nature['Empenhado'].map('R$ {:,.2f}'.format)
        df_by_nature['Liquidado'] = df_by_nature['Liquidado'].map('R$ {:,.2f}'.format)

        return [option, df_by_nature]

    def get_indicators(self):
        self.to_float()
        df = st.session_state.df_master
        committed = df['Empenhado'].sum()
        settled = df['Liquidado'].sum()
        balance = (committed - settled) * -1
        committed_formatted = "{:,.2f}".format(committed)
        settled_formatted = "{:,.2f}".format(settled)
        balance_formatted = "{:,.2f}".format(balance)

        return [committed_formatted, settled_formatted, balance_formatted]

    def clean_df(self):
        pass

    def to_float(self):
        if st.session_state.df_master['Empenhado'].apply(lambda x: isinstance(x, str)).any():
            st.session_state.df_master['Empenhado'] = st.session_state.df_master['Empenhado'].str.replace('.', '').str.replace(',', '.').astype(float)
        if st.session_state.df_master['Liquidado'].apply(lambda x: isinstance(x, str)).any():
            st.session_state.df_master['Liquidado'] = st.session_state.df_master['Liquidado'].str.replace('.', '').str.replace(',', '.').astype(float)
