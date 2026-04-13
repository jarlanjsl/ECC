import streamlit as st

st.set_page_config(page_title="Sistema ECC", page_icon="⛪", layout="wide")

import src.auth as auth
if not auth.check_password():
    st.stop()

st.title("Sistema de Gestão - ECC")
st.write("Bem-vindo ao portal unificado para o gerenciamento do ECC.")
st.write("Utilize o menu da esquerda para navegar pelo aplicativo:")

st.markdown("""
### 📥 Importação e Relatórios
Carregue seus arquivos `.csv` de **Encontreiros** ou **Encontristas** e obtenha os painéis atualizados em formato `.xlsx`.

### 📊 Indicadores
Acesse um Dashboard contendo as contagens de inscritos, status, e outros insights.
""")

st.info("Nota: Os dados inseridos ficam salvos apenas temporariamente na memória enquanto a sessão do seu navegador estiver aberta.")
