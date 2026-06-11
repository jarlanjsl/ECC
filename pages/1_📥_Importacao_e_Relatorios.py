import streamlit as st
import pandas as pd
from datetime import datetime
from src.encontreiros_utils import *
from src.encontristas_utils import *

st.set_page_config(page_title="Relatórios - ECC", layout="wide")

import src.auth as auth
if not auth.check_password():
    st.stop()

st.title("📥 Importação e Geração de Relatórios")

st.divider()

# Mobile upload tip
st.info("📱 **Dica para celular:** Ao abrir o seletor de arquivos, escolha **'Fotos e Vídeos'** → **'Gerenciador de Arquivos'** e selecione o arquivo CSV. Toque simples no arquivo já envia automaticamente.")

col_fmt1, col_fmt2 = st.columns([1, 3])
with col_fmt1:
    formato_saida = st.radio("Formato de Exportação:", options=["Excel", "PDF"])

formato_str = "pdf" if formato_saida == "PDF" else "excel"
extensao = ".pdf" if formato_str == "pdf" else ".xlsx"
mime_type = "application/pdf" if formato_str == "pdf" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
agora = datetime.now().strftime("%d%m%Y_%H%M")

aba1, aba2 = st.tabs(["Encontreiros", "Encontristas"])

with aba1:
    st.header("Upload de Arquivos - Encontreiros")
    col1, col2 = st.columns(2)
    
    with col1:
        file_encontreiros = st.file_uploader("Encontreiros (CSV)", key='f_encontreiros')
        
    with col2:
        file_financeiro = st.file_uploader("Conta Financeira (CSV)", key='f_financeiro')

    if file_encontreiros is not None:
        if not file_encontreiros.name.lower().endswith('.csv'):
            st.error(f"Erro: O arquivo '{file_encontreiros.name}' não é um CSV válido.")
            file_encontreiros = None
        else:
            try:
                df_inscricoes = pd.read_csv(file_encontreiros, sep=';', encoding='latin-1')
                st.session_state['df_encontreiros'] = df_inscricoes
            except Exception as e:
                st.error(f"Erro no CSV de Encontreiros: {e}")
    else:
        df_inscricoes = st.session_state.get('df_encontreiros', None)

    if file_financeiro is not None:
        if not file_financeiro.name.lower().endswith('.csv'):
            st.error(f"Erro: O arquivo '{file_financeiro.name}' não é um CSV válido.")
            file_financeiro = None
        else:
            try:
                df_financeiro = pd.read_csv(file_financeiro, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
                st.session_state['df_financeiro'] = df_financeiro
            except Exception as e:
                st.error(f"Erro no CSV de Financeiro: {e}")
    else:
        df_financeiro = st.session_state.get('df_financeiro', None)

    if df_inscricoes is not None or df_financeiro is not None:
        if df_inscricoes is not None:
            st.success("✅ Tabela de Encontreiros em memória!")
        if df_financeiro is not None:
            st.success("✅ Tabela de Conta Financeira em memória!")

    if df_inscricoes is not None or df_financeiro is not None:
        st.subheader("Relatórios Disponíveis")
        
        b_col1, b_col2, b_col3 = st.columns(3)
        
        if df_inscricoes is not None:
            try:
                with b_col1:
                    dados_equipes = gerar_lista_equipes(df_inscricoes, formato=formato_str)
                    st.download_button(
                        label=f"Baixar Lista de Equipes", data=dados_equipes,
                        file_name=f"lista_equipes_{agora}{extensao}", mime=mime_type
                    )
                    
                    dados_camisas = gerar_todas_camisas(df_inscricoes, formato=formato_str)
                    st.download_button(
                        label=f"Baixar Lista de Camisas", data=dados_camisas,
                        file_name=f"encontreiros_camisas_{agora}{extensao}", mime=mime_type
                    )
                
                with b_col2:
                    dados_status = gerar_relatorio_status(df_inscricoes, formato=formato_str)
                    st.download_button(
                        label=f"Baixar Relatório de Status", data=dados_status,
                        file_name=f"encontreiros_status_{agora}{extensao}", mime=mime_type
                    )
            except Exception as e:
                st.error(f"Erro ao processar relatórios de Encontreiros: {e}")
                
        if df_financeiro is not None:
            try:
                with b_col3:
                    dados_pagamento = gerar_relacao_pagamento(df_financeiro, formato=formato_str)
                    st.download_button(
                        label=f"Baixar Relação de Pagamento", data=dados_pagamento,
                        file_name=f"relacao_pagamento_{agora}{extensao}", mime=mime_type
                    )
            except Exception as e:
                st.error(f"Erro ao processar relatórios de Financeiro: {e}")

with aba2:
    st.header("Upload de Arquivos - Encontristas")
    file_encontristas = st.file_uploader("Encontristas (CSV)", key='f_encontristas')
    
    if file_encontristas is not None:
        if not file_encontristas.name.lower().endswith('.csv'):
            st.error(f"Erro: O arquivo '{file_encontristas.name}' não é um CSV válido.")
            file_encontristas = None
        else:
            try:
                df_encontristas = pd.read_csv(file_encontristas, sep=';', encoding='latin-1')
                st.session_state['df_encontristas'] = df_encontristas
            except Exception as e:
                st.error(f"Erro no CSV de Encontristas: {e}")
    else:
        df_encontristas = st.session_state.get('df_encontristas', None)

    if df_encontristas is not None:
        try:
            st.success("Tabela de Encontristas carregada com sucesso!")
            
            st.subheader("Relatórios Disponíveis")
            b_col1, b_col2 = st.columns(2)
            
            with b_col1:
                dados_lista_completa = gerar_lista_encontristas(df_encontristas, formato=formato_str)
                st.download_button(
                    label=f"Baixar Lista Completa", data=dados_lista_completa,
                    file_name=f"lista_completa_encontristas_{agora}{extensao}", mime=mime_type
                )
                
                dados_lista_res = gerar_lista_encontristas_resumida(df_encontristas, formato=formato_str)
                st.download_button(
                    label=f"Baixar Lista Encontristas", data=dados_lista_res,
                    file_name=f"lista_encontristas_{agora}{extensao}", mime=mime_type
                )
                
                dados_endereco = gerar_endereco_encontristas(df_encontristas, formato=formato_str)
                st.download_button(
                    label=f"Baixar Endereços", data=dados_endereco,
                    file_name=f"endereco_encontristas_{agora}{extensao}", mime=mime_type
                )
                
            with b_col2:
                dados_camisas_ent = gerar_camisas_encontristas(df_encontristas, formato=formato_str)
                st.download_button(
                    label=f"Baixar Camisas Encontristas", data=dados_camisas_ent,
                    file_name=f"encontristas_camisas_{agora}{extensao}", mime=mime_type
                )
                
                dados_circulos = gerar_lista_circulos_encontristas(df_encontristas, formato=formato_str)
                st.download_button(
                    label=f"Baixar Lista para Círculos", data=dados_circulos,
                    file_name=f"circulos_encontristas_{agora}{extensao}", mime=mime_type
                )
                
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")