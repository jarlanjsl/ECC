import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
import src.auth as auth

st.set_page_config(page_title="Assistente Virtual", layout="wide")

if not auth.check_password():
    st.stop()

st.title("🤖 Assistente Virtual (Gemini)")
st.write("Pergunte qualquer coisa sobre as suas planilhas de Encontreiros, Encontristas e Financeiro!")

# Verifica chaves
gemini_api_key = st.secrets.get("gemini_api_key", None)

with st.sidebar:
    st.header("Configurações")
    if not gemini_api_key:
        st.warning("⚠️ Chave API do Google Gemini não encontrada no `secrets.toml`.")
        gemini_api_key = st.text_input("Insira sua Gemini API Key:", type="password")
        if gemini_api_key:
            st.success("Chave fornecida com sucesso!")
    else:
        st.success("✔️ Conectado à API do Gemini")

if not gemini_api_key:
    st.info("Para usar o assistente, adicione sua chave de API na barra lateral ou no arquivo secrets.toml.")
    st.stop()

client = genai.Client(api_key=gemini_api_key)

# Carrega os dataframes da sessão corrente
dfs_context = []
df_encontreiros = st.session_state.get('df_encontreiros', None)
df_encontristas = st.session_state.get('df_encontristas', None)
df_financeiro = st.session_state.get('df_financeiro', None)

if df_encontreiros is not None:
    dfs_context.append(f"### Tabela de Encontreiros:\n```csv\n{df_encontreiros.to_csv(index=False)}\n```")
if df_encontristas is not None:
    dfs_context.append(f"### Tabela de Encontristas:\n```csv\n{df_encontristas.to_csv(index=False)}\n```")
if df_financeiro is not None:
    dfs_context.append(f"### Tabela do Financeiro:\n```csv\n{df_financeiro.to_csv(index=False)}\n```")

if not dfs_context:
    st.warning("Nenhum dado das planilhas foi encontrado na memória! Vá na aba de 'Importação e Relatórios', deixe o robô extrair ou faça upload dos arquivos CSV primeiro para que eu possa estudá-los.")
    st.stop()

contexto_completo = "\n\n".join(dfs_context)

system_instruction = f"""
Você é um assistente virtual especialista voltado para análise de dados do Encontro de Casais com Cristo (ECC). 
Sua tarefa é responder em Português-BR com extrema precisão às dúvidas da organização cruzando e analisando as seguintes bases de dados do sistema E-Inscrição fornecidas aqui no prompt.

REGRAS ESTABELECIDAS:
1. Responda APENAS baseado nos dados fornecidos abaixo em formato CSV.
2. Se não souber a resposta ou os dados não possuírem a informação, não finja saber. Diga explicitamente que os dados não contêm a informação. NÃO invente nomes, emails ou quantitativos.
3. Se a pergunta for estatística (ex: contar equipes, somar valores pagos, ver idades), conte as linhas lógicas e faça o cálculo fiel.
4. Ao citar e listar pessoas ou casais como resposta, apresente no formato de lista (bullet points) ou tabelas curtas para facilitar a leitura.
5. Seja útil e cordial.

DADOS DISPONÍVEIS:
{contexto_completo}
"""

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {"role": "assistant", "content": "Olá! Sou o seu Assistente de IA. Já avaliei as planilhas carregadas. Você pode me perguntar coisas como: *'Quem são os casais da equipe de circulos?'* ou *'Quantos encontristas ainda não pagaram?'*. O que vamos investigar agora?"}
    ]

# Renderizar mensagens anteriores
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ex: 'Identifique na lista de finanças quem ainda não tem pagamento confirmado'"):
    # Adicionar mensagem do ususario na tela
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Analisando e raciocinando sobre as planilhas..."):
            try:
                # Prepara histórico pro formato Gemini (descartando o primeiro que é o hello default local)
                history = []
                for m in st.session_state.chat_messages[1:-1]:
                    if m["role"] == "user":
                        history.append(types.Content(role="user", parts=[types.Part.from_text(text=m["content"])]))
                    elif m["role"] == "assistant":
                        history.append(types.Content(role="model", parts=[types.Part.from_text(text=m["content"])]))

                # Criando o chat e aplicando a system_instruction
                chat = client.chats.create(
                    model='gemini-2.5-flash',
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction
                    ),
                    history=history
                )
                response = chat.send_message(prompt)
                
                resposta_texto = response.text
                st.write(resposta_texto)
                st.session_state.chat_messages.append({"role": "assistant", "content": resposta_texto})
            except Exception as e:
                st.error(f"Ocorreu um erro ao contactar as antenas do Gemini. Verifique a chave da API ou sua conexão. Detalhes: {e}")
