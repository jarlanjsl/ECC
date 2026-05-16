# Sistema de Gestão e Relatórios - ECC (Encontro de Casais com Cristo)

Este é um sistema web desenvolvido em **Python** utilizando o framework **Streamlit**, projetado para facilitar a gestão, cruzamento de dados e geração de relatórios para equipes e coordenação do ECC.

## 🚀 Funcionalidades Principais

*   **Gestão de Dados via CSV**: Upload simplificado das planilhas extraídas do sistema E-Inscrição (Encontristas, Encontreiros e Financeiro).
*   **Geração de Relatórios em PDF**: Exportação instantânea de listas de equipes, relatórios financeiros e camisas utilizando a biblioteca leve e nativa `xhtml2pdf`.
*   **Dashboards Interativos**: Visualização rápida do status financeiro e métricas gerais do encontro através de gráficos.
*   **Assistente Virtual (Inteligência Artificial)**: Chatbot integrado na plataforma alimentado pelo **Google Gemini**. O assistente é capaz de ler milhares de linhas das suas planilhas de uma só vez e responder a perguntas complexas em linguagem natural (Ex: *"Quantos casais da paróquia X ainda não pagaram a inscrição?"*).

## 🛠️ Tecnologias Utilizadas

*   [Streamlit](https://streamlit.io/) - Interface Web e Roteamento
*   [Pandas](https://pandas.pydata.org/) - Processamento e Cruzamento de Dados
*   [xhtml2pdf](https://pypi.org/project/xhtml2pdf/) - Geração de PDFs
*   [Google GenAI SDK](https://ai.google.dev/) - Integração com o LLM Gemini

## ⚙️ Como Executar Localmente (Windows/Mac/Linux)

### 1. Pré-requisitos
Certifique-se de ter o **Python 3.10+** instalado em sua máquina.

### 2. Instalação das Dependências
Abra o terminal na pasta do projeto e instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 3. Configuração das Chaves de Segurança
O sistema requer senhas e chaves de API para funcionar. Crie uma pasta chamada `.streamlit` na raiz do projeto e dentro dela crie um arquivo chamado `secrets.toml`:

**.streamlit/secrets.toml**
```toml
password = "sua_senha_de_acesso_ao_app"
gemini_api_key = "AIzaSy_Sua_Chave_da_API_do_Google_Gemini"
```
*(Nota: Nunca faça o commit deste arquivo para o GitHub para não vazar suas credenciais!)*

### 4. Rodando o Aplicativo
Execute o comando abaixo no terminal:
```bash
streamlit run main_code.py
```
O sistema abrirá automaticamente no seu navegador.

## ☁️ Deploy no Streamlit Community Cloud

O sistema está 100% pronto para ser hospedado gratuitamente na nuvem do Streamlit:
1. Conecte este repositório do GitHub ao Streamlit Cloud.
2. Na etapa de configuração do deploy, acesse **Advanced Settings > Secrets** e cole o exato conteúdo do seu arquivo `secrets.toml`.
3. Não é necessário configurar o sistema operacional, pois a geração de PDF utiliza Python puro.

---
*Desenvolvido para otimizar o trabalho da coordenação do ECC.*
