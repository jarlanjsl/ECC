import time
import sys
import asyncio
import pandas as pd
from playwright.sync_api import sync_playwright

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def extrair_todos_dados_einscricao(email, senha, data_inicial=None, data_final=None):
    """
    Aciona o robô do E-Inscrição, faz login persistente na validação,
    e exporta os 3 CSVs: encontreiros, encontristas, financeiro sequencialmente.
    Retorna um dicionário: {"encontreiros": df, "encontristas": df, "financeiro": df} ou None
    """
    resultados = {"encontreiros": None, "encontristas": None, "financeiro": None}
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir="./.playwright_session",
            headless=False,
            viewport={"width": 800, "height": 700},
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled", "--window-size=800,700"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        print("Iniciando extração em lote (Sincronização Total)")
        
        # 1. Login Persistente Seguro
        page.goto("https://www.e-inscricao.com/users/sign_in")
        page.wait_for_load_state("domcontentloaded")
        
        if "users/sign_in" in page.url:
            print("Verificando necessidade de login (aguardando Cloudflare)...")
            try:
                try:
                    page.wait_for_selector('input[type="email"]', state='visible', timeout=30000)
                except Exception:
                    print("Campo de email não carregou a tempo (Cloudflare lento ou logado).")
                    pass

                if "users/sign_in" in page.url and page.locator('input[type="email"]').is_visible():
                    print("Realizando login...")
                    page.locator('input[type="email"]').type(email, delay=100)
                    page.locator('input[type="password"]').type(senha, delay=100)
                    page.click('input[type="submit"], button[type="submit"]')
                    print("Aguardando login concluir...")
                    try:
                        page.wait_for_url(lambda url: "users/sign_in" not in url, timeout=15000)
                    except:
                        page.wait_for_timeout(5000)
            except Exception as e:
                print(f"Erro grave no login: {e}")
                context.close()
                return None
        
        def process_download(path):
            try:
                return pd.read_csv(path, sep=';', encoding='utf-8-sig', on_bad_lines='skip')
            except UnicodeDecodeError:
                return pd.read_csv(path, sep=';', encoding='latin1', on_bad_lines='skip')

        import urllib.parse
        
        try:
            query_params = []
            if data_inicial:
                query_params.append(f"start_date={urllib.parse.quote(data_inicial, safe='')}")
            if data_final:
                query_params.append(f"end_date={urllib.parse.quote(data_final, safe='')}")
            query_str = "?" + "&".join(query_params) if query_params else ""

            # Encontreiros
            print("Baixando Encontreiros...")
            page.goto(f"https://www.e-inscricao.com/eccdapazceara/encontreiroxviiecc/enrollments/beta#/{query_str}")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(5000)
            
            with page.expect_download(timeout=15000) as download_info:
                page.get_by_text("Exportar Lista", exact=False).first.click()
            resultados["encontreiros"] = process_download(download_info.value.path())

            # Encontristas
            print("Baixando Encontristas...")
            page.goto(f"https://www.e-inscricao.com/eccdapazceara/encontristaxviiecc/enrollments/beta#/{query_str}")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(5000)
            
            with page.expect_download(timeout=15000) as download_info:
                page.get_by_text("Exportar Lista", exact=False).first.click()
            resultados["encontristas"] = process_download(download_info.value.path())

            # Financeiro
            print("Baixando Financeiro...")
            page.goto("https://www.e-inscricao.com/financial_accounts/42141")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(3000)
            
            page.get_by_label("Evento", exact=False).select_option(label="encontreiroXVIIECC")
            page.get_by_label("Filtro", exact=False).select_option(label="Pagas em")
            
            if data_inicial:
                campo_data_ini = page.get_by_label("Data Inicial", exact=False)
                campo_data_ini.fill(data_inicial)
                campo_data_ini.press("Enter")
                
            if data_final:
                campo_data_fim = page.get_by_label("Data Final", exact=False)
                campo_data_fim.fill(data_final)
                campo_data_fim.press("Enter")
            
            page.get_by_role("button", name="Filtrar").click()
            page.wait_for_timeout(3000)
            
            with page.expect_download() as download_info:
                page.get_by_text("CSV", exact=True).click()
            resultados["financeiro"] = process_download(download_info.value.path())
            
            print("Extração Completa!")
        except Exception as e:
            print(f"Uma falha na navegação encerrou a tentativa: {e}")
        finally:
            context.close()
            
        return resultados
