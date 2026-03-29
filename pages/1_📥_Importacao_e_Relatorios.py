import streamlit as st
import pandas as pd
from src.encontreiros_utils import *
from src.encontristas_utils import *

st.set_page_config(page_title="Relatórios - ECC", layout="wide")

import src.auth as auth
if not auth.check_password():
    st.stop()

st.title("📥 Importação e Geração de Relatórios")

with st.expander("Sincronização Online (🤖 Robô E-Inscrição)", expanded=True):
    st.write("Selecione qual pacote de dados o sistema deve extrair rodando diretamente no painel oficial:")
    
    # Criando 3 colunas para colocar os botões lado-a-lado
    colA, colB, colC = st.columns(3)
    
    def executa_sincronizacao(tipo_bot, chave_tabela):
        if "einscricao_email" in st.secrets and "einscricao_senha" in st.secrets:
            from src.extrator_bot import extrair_dados_einscricao
            with st.spinner(f"Rodando Automação para {tipo_bot.upper()}... Olhe a aba do robô!"):
                df = extrair_dados_einscricao(st.secrets["einscricao_email"], st.secrets["einscricao_senha"], tipo_bot)
                
                if df is not None:
                    st.session_state[chave_tabela] = df
                    st.success(f"Tabela de {tipo_bot.upper()} interceptada com maestria!")
                else:
                    st.error(f"Erro ou cancelamento do download da lista de {tipo_bot}. Veja o log ou a janela.")
        else:
            st.warning("⚠️ Suas chaves secretas einscricao_email e einscricao_senha sumiram!")
            
    with colA:
        if st.button("⏬ Sincronizar Encontreiros"):
            executa_sincronizacao("encontreiros", "df_encontreiros")
    with colB:
        if st.button("⏬ Sincronizar Encontristas"):
            executa_sincronizacao("encontristas", "df_encontristas")
    with colC:
        if st.button("⏬ Banco / Financeiro"):
            executa_sincronizacao("financeiro", "df_financeiro")

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

    df_inscricoes = st.session_state.get('df_encontreiros', None)
    if df_inscricoes is None and file_encontreiros is not None:
        try:
            df_inscricoes = pd.read_csv(file_encontreiros, sep=';', encoding='latin-1')
            st.session_state['df_encontreiros'] = df_inscricoes
        except Exception as e:
            st.error(f"Erro no CSV de Encontreiros: {e}")

    if df_inscricoes is not None:
        try:
            st.success("Tabela de inscrições de Encontreiros carregada com sucesso!")
            
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

            df_financeiro = st.session_state.get('df_financeiro', None)
            if df_financeiro is None and file_financeiro is not None:
                df_financeiro = pd.read_csv(file_financeiro, sep=';', on_bad_lines='skip')
                st.session_state['df_financeiro'] = df_financeiro
                
            if df_financeiro is not None:
                
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
    
    df_encontristas = st.session_state.get('df_encontristas', None)
    if df_encontristas is None and file_encontristas is not None:
        try:
            df_encontristas = pd.read_csv(file_encontristas, sep=';', encoding='latin-1')
            st.session_state['df_encontristas'] = df_encontristas
        except Exception as e:
            st.error(f"Erro no CSV de Encontristas: {e}")

    if df_encontristas is not None:
        try:
            st.success("Tabela de Encontristas carregada com sucesso!")
            
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
