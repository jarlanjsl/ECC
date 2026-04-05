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
            viewport={"width": 800, "height": 700},
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled", "--window-size=800,700"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        print(f"Iniciando extração do tipo: {tipo.upper()}")
        
        # 1. Login Persistente Seguro
        page.goto("https://www.e-inscricao.com/users/sign_in")
        page.wait_for_load_state("domcontentloaded")
        
        if "users/sign_in" in page.url:
            print("Login necessário...")
            try:
                try:
                    page.wait_for_selector('input[type="email"]', state='visible', timeout=3000)
                except Exception:
                    pass

                if "users/sign_in" in page.url and page.locator('input[type="email"]').is_visible():
                    page.locator('input[type="email"]').type(email, delay=100)
                    page.locator('input[type="password"]').type(senha, delay=100)
                    page.click('input[type="submit"], button[type="submit"]')
                    print("Aguardando login concluir...")
                    page.wait_for_timeout(5000) # tempo pro servidor autorizar e gerar o cookie
            except Exception as e:
                print(f"Erro grave no login: {e}")
                context.close()
                return None
        
        # 2. Navegação para as páginas de Exportação
        download = None
        try:
            if tipo == "encontreiros":
                page.goto("https://www.e-inscricao.com/eccdapazceara/encontreiroxviiecc/enrollments/beta#/")
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(3000) # dá tempo pro framework Javascript de terceiros renderizar os botões
                
                print("Acionando o botão 'Exportar Lista'...")
                with page.expect_download(timeout=15000) as download_info:
                    # Usando first() pro caso de existirem dois textos ou ícones com a mesma label atrapalhando o script
                    page.get_by_text("Exportar Lista", exact=False).first.click()
                download = download_info.value
                
            elif tipo == "encontristas":
                page.goto("https://www.e-inscricao.com/eccdapazceara/encontristaxviiecc/enrollments/beta#/")
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(3000)
                
                print("Acionando o botão 'Exportar Lista'...")
                with page.expect_download(timeout=15000) as download_info:
                    page.get_by_text("Exportar Lista", exact=False).first.click()
                download = download_info.value
                
            elif tipo == "financeiro":
                page.goto("https://www.e-inscricao.com/financial_accounts/42141")
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(3000)
                print("Tentando aplicar filtros automáticos na área Financeira...")
                
                # Preenche de acordo com os Selects e Inputs visuais prováveis
                page.get_by_label("Evento", exact=False).select_option(label="encontreiroXVIIECC")
                page.get_by_label("Filtro", exact=False).select_option(label="Pagas em")
                
                # Forçando inputar data num campo que não sabemos o ID certeiro
                # Vamos varrer os labels mais comuns de Data Inicial
                campo_data = page.get_by_label("Data Inicial", exact=False)
                campo_data.fill("01/01/2026")
                campo_data.press("Enter") # Confirma o preenchimento e fecha calendários suspensos
                
                page.get_by_role("button", name="Filtrar").click()
                page.wait_for_timeout(3000) # Aguarda o filtro aplicar sem depender do networkidle
                
                print("Tentando clicar em CSV...")
                with page.expect_download() as download_info:
                    page.get_by_text("CSV", exact=True).click()
                download = download_info.value
                    
            else:
                print(f"Tipo desconhecido: {tipo}")
                context.close()
                return None
            
            # 3. Leitura e Retorno
            print("Download concluído com sucesso!")
            path = download.path()
            
            # O novo formato do sistema usa UTF-8 com BOM, mas se falhar, tentamos o formato antigo (latin1)
            try:
                df = pd.read_csv(path, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
            except UnicodeDecodeError:
                df = pd.read_csv(path, sep=';', encoding='latin1', on_bad_lines='skip')
            context.close()
            return df

        except Exception as e:
            print(f"Uma falha na navegação encerrou a tentativa: {e}")
            context.close()
            return None
