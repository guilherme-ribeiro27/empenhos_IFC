import streamlit as st
import pandas as pd
from utils import *
from classes.dataframe_manager import DataframeManager
from streamlit_echarts import st_echarts

def by_nature_details(onlyTable=False):
    df_manager = DataframeManager()
    [option, get_dataframe_by_nature] = df_manager.get_df_by_all_nature()
    options = {
        **option,
        "title": {
            "text": '',
        },
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow'
            },
        },
        "legend": {
            "data": ['Empenhado', 'Liquidado'],
            "left": '0%',
            "top": '1%',
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "top": '8%',
            "containLabel": True
        },
        "xAxis": {
            "type": 'value',
            "boundaryGap": [0, 0.01]
        }
    }

    if 'show_graph' not in st.session_state:
        st.session_state['show_graph'] = False

    # if st.button("Mostrar o total de cada tipo de Natureza", type="secondary", key=f'sacvsadfgsdf{onlyTable}', help="Clique para ver o total de cada tipo de Natureza", use_container_width=True):
    #     st.session_state['show_graph'] = not st.session_state['show_graph']

    # if st.session_state['show_graph']:
    #     st_echarts(options=options, height="500px", key=f'{onlyTable}_id_dessa_porra')


    nature = [item for item in st.session_state.df_master["Natureza Despesa"].unique()]
    st.session_state.nature = st.selectbox(
        label="Selecione a Natureza da Despesa",
        key=f"get_m123onth_{onlyTable}_{id}",
        options=nature,
        index=None,
        placeholder="Selecione a Natureza da Despesa",
    )
    if st.session_state.nature == None:
        st.info("Selecione uma Natureza da Despesa", icon="ℹ️")
    else:
        [option2, df_by_nature] = df_manager.get_df_by_nature(st.session_state.nature)
        st.table(df_by_nature)