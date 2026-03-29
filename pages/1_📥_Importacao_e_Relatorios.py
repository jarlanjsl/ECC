import streamlit as st
import pandas as pd
from src.encontreiros_utils import *
from src.encontristas_utils import *

st.set_page_config(page_title="Relatórios - ECC", layout="wide")
st.title("📥 Importação e Geração de Relatórios")

aba1, aba2 = st.tabs(["Encontreiros", "Encontristas"])

with aba1:
    st.header("Upload de Arquivos - Encontreiros")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        file_encontreiros = st.file_uploader("Encontreiros (CSV)", type=['csv'], key='f_encontreiros')
    with col2:
        file_financeiro = st.file_uploader("Conta Financeira (CSV)", type=['csv'], key='f_financeiro')
    with col3:
        file_sorteados = st.file_uploader("Sorteados (CSV) - Opcional", type=['csv'], key='f_sorteados')

    if file_encontreiros is not None:
        try:
            df_inscricoes = pd.read_csv(file_encontreiros, sep=';', encoding='latin-1')
            st.session_state['df_encontreiros'] = df_inscricoes
            st.success("Tabela de inscrições carregada com sucesso!")
            
            st.subheader("Relatórios Disponíveis")
            b_col1, b_col2, b_col3 = st.columns(3)
            
            with b_col1:
                excel_equipes = gerar_lista_equipes(df_inscricoes)
                st.download_button(
                    label="Baixar Lista de Equipes", data=excel_equipes,
                    file_name="lista_equipes.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                excel_camisas = gerar_todas_camisas(df_inscricoes)
                st.download_button(
                    label="Baixar Lista de Camisas", data=excel_camisas,
                    file_name="encontreiros_camisas.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with b_col2:
                excel_igrejas = gerar_analise_igrejas(df_inscricoes)
                st.download_button(
                    label="Baixar Análise de Igrejas", data=excel_igrejas,
                    file_name="analise_por_igreja.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            if file_financeiro is not None:
                df_financeiro = pd.read_csv(file_financeiro, sep=';', on_bad_lines='skip')
                st.session_state['df_financeiro'] = df_financeiro
                
                df_sort = None
                if file_sorteados is not None:
                    df_sort = pd.read_csv(file_sorteados, sep=';')
                
                with b_col3:
                    excel_pagamento = gerar_relacao_pagamento(df_financeiro)
                    st.download_button(
                        label="Baixar Relação de Pagamento", data=excel_pagamento,
                        file_name="relacao_pagamento.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                    excel_sorteio = gerar_lista_sorteio(df_inscricoes, df_financeiro, df_sort)
                    st.download_button(
                        label="Baixar Lista de Sorteio", data=excel_sorteio,
                        file_name="lista_sorteio.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

        except Exception as e:
            st.error(f"Erro ao processar arquivo(s): {e}")

with aba2:
    st.header("Upload de Arquivos - Encontristas")
    file_encontristas = st.file_uploader("Encontristas (CSV)", type=['csv'], key='f_encontristas')
    
    if file_encontristas is not None:
        try:
            df_encontristas = pd.read_csv(file_encontristas, sep=';', encoding='latin-1')
            st.session_state['df_encontristas'] = df_encontristas
            st.success("Tabela de encontristas carregada com sucesso!")
            
            st.subheader("Relatórios Disponíveis")
            b_col1, b_col2 = st.columns(2)
            
            with b_col1:
                excel_lista = gerar_lista_encontristas(df_encontristas)
                st.download_button(
                    label="Baixar Lista Encontristas", data=excel_lista,
                    file_name="lista_encontristas.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                excel_endereco = gerar_endereco_encontristas(df_encontristas)
                st.download_button(
                    label="Baixar Endereços", data=excel_endereco,
                    file_name="endereco_encontristas.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            with b_col2:
                excel_camisas_ent = gerar_camisas_encontristas(df_encontristas)
                st.download_button(
                    label="Baixar Camisas Encontristas", data=excel_camisas_ent,
                    file_name="encontristas_camisas.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
