import streamlit as st
import pandas as pd
from src.dashboard_utils import obter_indicadores_principais

st.set_page_config(page_title="Dashboard - ECC", layout="wide")
st.title("📊 Indicadores do ECC")

# Check if data exists in memory
df_encontreiros = st.session_state.get('df_encontreiros', None)

if df_encontreiros is not None:
    st.subheader("📌 Inscrições (Encontreiros)")
    indicadores = obter_indicadores_principais(df_encontreiros)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Inscritos", indicadores['total_inscricoes'])
    col2.metric("Confirmados (Ok)", indicadores['confirmados'])
    col3.metric("Pendentes", indicadores['pendentes'])
    col4.metric("Atrasados", indicadores['atrasados'])
    col5.metric("Cancelados", indicadores['cancelados'])
    
    st.divider()
    
    st.markdown("### Prévia Rápida dos Dados")
    st.dataframe(df_encontreiros.head(10))
    
else:
    st.warning("Nenhum dado de Encontreiros importado. Volte à página de 'Importação e Relatórios' e anexe o '.csv' para visualizar os indicadores.")

st.divider()

df_encontristas = st.session_state.get('df_encontristas', None)
if df_encontristas is not None:
    st.subheader("📌 Inscrições (Encontristas)")
    st.metric("Total Encontristas", len(df_encontristas))
    st.dataframe(df_encontristas.head(10))
