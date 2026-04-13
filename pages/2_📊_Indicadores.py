import streamlit as st
import pandas as pd
from src.dashboard_utils import obter_indicadores_principais

st.set_page_config(page_title="Dashboard - ECC", layout="wide")

import src.auth as auth
if not auth.check_password():
    st.stop()

st.title("📊 Indicadores do ECC")

# Check if data exists in memory
df_encontreiros = st.session_state.get('df_encontreiros', None)

if df_encontreiros is not None:
    st.subheader("📌 Inscrições (Encontreiros)")
    indicadores = obter_indicadores_principais(df_encontreiros)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Inscritos", indicadores['total_inscricoes'])
    col2.metric("Confirmados", indicadores['confirmados'])
    col3.metric("Pendentes", indicadores['pendentes'])
    
else:
    st.warning("Nenhum dado de Encontreiros importado. Volte à página de 'Importação e Relatórios' e anexe o '.csv' para visualizar os indicadores.")

st.divider()

df_encontristas = st.session_state.get('df_encontristas', None)
if df_encontristas is not None:
    st.subheader("📌 Inscrições (Encontristas)")
    indicadores_encontristas = obter_indicadores_principais(df_encontristas)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Inscritos", indicadores_encontristas['total_inscricoes'])
    col2.metric("Confirmados", indicadores_encontristas['confirmados'])
    col3.metric("Pendentes", indicadores_encontristas['pendentes'])
