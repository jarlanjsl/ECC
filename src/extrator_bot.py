import time
import sys
import asyncio
import pandas as pd
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def extrair_dados_einscricao(email, senha, tipo):
    """
    Aciona o robô do E-Inscrição, faz login persistente,
    navega até a rota especificada por `tipo` e exporta o CSV apropriado.
    Tipos permitidos: 'encontreiros', 'encontristas', 'financeiro'
    """
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./.playwright_session",
            headless=False,
            no_viewport=True,
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        print(f"Iniciando extração do tipo: {tipo.upper()}")
        
        # 1. Login Persistente Seguro
        page.goto("https://www.e-inscricao.com/users/sign_in")
        page.wait_for_load_state("networkidle")
        
        if "users/sign_in" in page.url:
            print("Login necessário...")
            try:
                try:
                    page.wait_for_selector('input[type="email"]', state='visible', timeout=3000)
                except Exception:
                    print(">>> INTERVENÇÃO (Cloudflare) <<< Resolva e aperte Play/Resume.")
                    page.pause()

                if "users/sign_in" in page.url and page.locator('input[type="email"]').is_visible():
                    page.locator('input[type="email"]').type(email, delay=100)
                    page.locator('input[type="password"]').type(senha, delay=100)
                    page.click('input[type="submit"], button[type="submit"]')
                    
                    print(">>> INTERVENÇÃO (Pós-login) <<< Se pedir Captcha, resolva e dê Resume.")
                    page.pause()
            except Exception as e:
                print(f"Erro grave no login: {e}")
                context.close()
                return None
        
        # 2. Navegação para as páginas de Exportação
        download = None
        try:
            if tipo == "encontreiros":
                page.goto("https://www.e-inscricao.com/eccdapazceara/encontreiroxviiecc/enrollments/beta#/")
                page.wait_for_load_state("networkidle")
                
                print("Acionando o botão 'Exportar Lista'...")
                try:
                    with page.expect_download(timeout=15000) as download_info:
                        # Usando first() pro caso de existirem dois textos ou ícones com a mesma label atrapalhando o script
                        page.get_by_text("Exportar Lista", exact=False).first.click()
                    download = download_info.value
                except Exception as click_err:
                    print(f"O script não conseguiu clicar ou aguardar o Export: {click_err}")
                    print(">>> INTERVENÇÃO NECESSÁRIA. PAUSANDO... <<<")
                    print("A tela do E-Inscrição deve ter aberto algum pop-up ou bloqueado o clique único.")
                    print("Por favor, localize e CLIQUE VOCÊ MESMO no botão que gera o CSV!")
                    with page.expect_download(timeout=60000) as download_info:
                        page.pause()
                    download = download_info.value
                
            elif tipo == "encontristas":
                page.goto("https://www.e-inscricao.com/eccdapazceara/encontristaxviiecc/enrollments/beta#/")
                page.wait_for_load_state("networkidle")
                
                print("Acionando o botão 'Exportar Lista'...")
                try:
                    with page.expect_download(timeout=15000) as download_info:
                        page.get_by_text("Exportar Lista", exact=False).first.click()
                    download = download_info.value
                except Exception as click_err:
                    print(f"O script não conseguiu clicar no Export: {click_err}")
                    print(">>> INTERVENÇÃO NECESSÁRIA. PAUSANDO... <<<")
                    print("Por favor, CLIQUE VOCÊ MESMO no botão de baixar CSV no navegador aberto!")
                    with page.expect_download(timeout=60000) as download_info:
                        page.pause()
                    download = download_info.value
                
            elif tipo == "financeiro":
                page.goto("https://www.e-inscricao.com/financial_accounts/42141")
                page.wait_for_load_state("networkidle")
                print("Tentando aplicar filtros automáticos na área Financeira...")
                
                try:
                    # Preenche de acordo com os Selects e Inputs visuais prováveis
                    page.get_by_label("Evento", exact=False).select_option(label="encontreiroXVIIECC")
                    page.get_by_label("Filtro", exact=False).select_option(label="Pagas em")
                    
                    # Forçando inputar data num campo que não sabemos o ID certeiro
                    # Vamos varrer os labels mais comuns de Data Inicial
                    campo_data = page.get_by_label("Data Inicial", exact=False)
                    campo_data.fill("01/01/2026")
                    campo_data.press("Enter") # Confirma o preenchimento e fecha calendários suspensos
                    
                    page.get_by_role("button", name="Filtrar").click()
                    page.wait_for_load_state("networkidle")
                    
                    print("Tentando clicar em CSV...")
                    with page.expect_download() as download_info:
                        page.get_by_text("CSV", exact=True).click()
                    download = download_info.value
                except Exception as ex:
                    print("Atenção: Os seletores HTML fugiram do padrão imaginado! >>> PAUSA DE SEGURANÇA <<<")
                    print("1. Por favor, coloque os filtros na tela, e clique no botão FILTRAR manualmente.")
                    print("2. Agora fique atento DENTRO da janela do E-Inscrição, localize e clique no botão 'CSV'!")
                    print("O código aguardará você fazer o clique de Download manualmente, e vai pegar o arquivo voando para o Streamlit quando ele começar baixar.")
                    
                    with page.expect_download() as download_info:
                        # Nessa pausa, sua função será apenas clicar no botão CSV que faltou na tela.
                        page.pause()
                    download = download_info.value
                    
            else:
                print(f"Tipo desconhecido: {tipo}")
                context.close()
                return None
            
            # 3. Leitura e Retorno
            print("Download concluído com sucesso!")
            path = download.path()
            
            # A lib Pandas precisa ler usando charset Brasileiro (latin-1) e delimitador ;
            df = pd.read_csv(path, sep=';', encoding='latin-1', on_bad_lines='skip')
            context.close()
            return df

        except Exception as e:
            print(f"Uma falha na navegação encerrou a tentativa: {e}")
            context.close()
            return None
