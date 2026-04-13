import pandas as pd
import os
from playwright.sync_api import sync_playwright

def dataframe_to_pdf(df_or_list, titulo1, titulo2=""):
    # Converte dataframe para HTML com um design responsivo e de tabela corporativa
    html_body = f"<h1>{titulo1}</h1>"
    
    # Verifica se é apenas um DataFrame ou uma lista de tuplas (titulo2, df)
    if isinstance(df_or_list, pd.DataFrame):
        lista_dfs = [(titulo2, df_or_list)]
    else:
        lista_dfs = df_or_list
        
    for tit, df in lista_dfs:
        if tit:
            html_body += f"<h2>{tit}</h2>"
        html_body += df.to_html(index=False)
        html_body += "<br><br>"
        
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #2c3e50; font-size: 20px; text-align: center; margin-bottom: 5px; }}
            h2 {{ color: #34495e; font-size: 16px; text-align: left; margin-bottom: 10px; margin-top: 30px; border-bottom: 1px solid #ccc; }}
            table {{ border-collapse: collapse; width: 100%; font-size: 11px; margin-bottom: 20px; page-break-inside: auto; }}
            tr {{ page-break-inside: avoid; page-break-after: auto; }}
            th {{ background-color: #3498db; color: white; border: 1px solid #bdc3c7; padding: 8px; text-align: left; }}
            td {{ border: 1px solid #bdc3c7; padding: 6px; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            tr:hover {{ background-color: #e8f4f8; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    temp_html = "temp_report.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            abs_path = os.path.abspath(temp_html)
            page.goto(f"file:///{abs_path.replace(chr(92), '/')}")
            # Escrevendo PDF em orientação retrato ou paisagem dependendo do número de colunas do primeiro DF
            df_ref = lista_dfs[0][1]
            if len(df_ref.columns) > 5:
                landscape_mode = True
            else:
                landscape_mode = False
                
            pdf_bytes = page.pdf(format="A4", landscape=landscape_mode, margin={"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"})
            browser.close()
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)
            
    return pdf_bytes
