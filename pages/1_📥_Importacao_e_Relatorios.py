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

with st.expander("Sincronização Online (🤖 Robô E-Inscrição)", expanded=True):
    st.write("Acione o robô para baixar automaticamente Encontreiros, Encontristas e Financeiro:")
    
    def executa_sincronizacao_total():
        if "einscricao_email" in st.secrets and "einscricao_senha" in st.secrets:
            from src.extrator_bot import extrair_todos_dados_einscricao
            with st.spinner("Rodando Automação para sincronização global... Aguarde!"):
                resultado = extrair_todos_dados_einscricao(st.secrets["einscricao_email"], st.secrets["einscricao_senha"])
                
                if resultado:
                    if resultado["encontreiros"] is not None:
                        st.session_state["df_encontreiros"] = resultado["encontreiros"]
                    if resultado["encontristas"] is not None:
                        st.session_state["df_encontristas"] = resultado["encontristas"]
                    if resultado["financeiro"] is not None:
                        st.session_state["df_financeiro"] = resultado["financeiro"]
                        
                    st.success("Bases de dados sincronizadas com sucesso!")
                else:
                    st.error("Falha geral ao sincronizar dados. Inspecione o terminal e os logs.")
        else:
            st.warning("⚠️ Suas chaves secretas einscricao_email e einscricao_senha sumiram!")
            
    if st.button("⏬ Sincronizar Tudo", use_container_width=True):
        executa_sincronizacao_total()
        
st.divider()
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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        file_encontreiros = st.file_uploader("Encontreiros (CSV)", type=['csv'], key='f_encontreiros')
    with col2:
        file_financeiro = st.file_uploader("Conta Financeira (CSV)", type=['csv'], key='f_financeiro')
    with col3:
        file_sorteados = st.file_uploader("Sorteados (CSV) - Opcional", type=['csv'], key='f_sorteados')

    df_inscricoes = st.session_state.get('df_encontreiros', None)
    df_financeiro = st.session_state.get('df_financeiro', None)
    df_sort = None
    
    if df_inscricoes is None and file_encontreiros is not None:
        try:
            df_inscricoes = pd.read_csv(file_encontreiros, sep=';', encoding='latin-1')
            st.session_state['df_encontreiros'] = df_inscricoes
        except Exception as e:
            st.error(f"Erro no CSV de Encontreiros: {e}")

    if df_financeiro is None and file_financeiro is not None:
        try:
            df_financeiro = pd.read_csv(file_financeiro, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
            st.session_state['df_financeiro'] = df_financeiro
        except Exception as e:
            st.error(f"Erro no CSV de Financeiro: {e}")
            
    if file_sorteados is not None:
        df_sort = pd.read_csv(file_sorteados, sep=';')

    if df_inscricoes is not None:
        try:
            st.success("Tabela de inscrições de Encontreiros carregada com sucesso!")
            
            st.subheader("Relatórios Disponíveis")
            b_col1, b_col2, b_col3 = st.columns(3)
            
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
                dados_igrejas = gerar_analise_igrejas(df_inscricoes, formato=formato_str)
                st.download_button(
                    label=f"Baixar Análise de Igrejas", data=dados_igrejas,
                    file_name=f"analise_por_igreja_{agora}{extensao}", mime=mime_type
                )
                
            if df_financeiro is not None:
                with b_col3:
                    dados_pagamento = gerar_relacao_pagamento(df_financeiro, formato=formato_str)
                    st.download_button(
                        label=f"Baixar Relação de Pagamento", data=dados_pagamento,
                        file_name=f"relacao_pagamento_{agora}{extensao}", mime=mime_type
                    )
                    
                    dados_sorteio = gerar_lista_sorteio(df_inscricoes, df_financeiro, df_sort, formato=formato_str)
                    st.download_button(
                        label=f"Baixar Lista de Sorteio", data=dados_sorteio,
                        file_name=f"lista_sorteio_{agora}{extensao}", mime=mime_type
                    )

        except Exception as e:
            st.error(f"Erro ao processar arquivo(s): {e}")
            if df_financeiro is not None:
                st.write("Colunas encontradas no arquivo Financeiro:", list(df_financeiro.columns))
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
                dados_lista_ent = gerar_lista_encontristas(df_encontristas, formato=formato_str)
                st.download_button(
                    label=f"Baixar Lista Encontristas", data=dados_lista_ent,
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
