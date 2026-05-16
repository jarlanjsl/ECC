import pandas as pd
import io
from xhtml2pdf import pisa
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
        
    # Escrevendo PDF em orientação retrato ou paisagem dependendo do número de colunas do primeiro DF
    df_ref = lista_dfs[0][1]
    if len(df_ref.columns) > 5:
        # Modo paisagem (landscape)
        page_css = "@page { size: A4 landscape; margin: 1cm; }"
    else:
        # Modo retrato (portrait)
        page_css = "@page { size: A4 portrait; margin: 1cm; }"
        
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            {page_css}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; }}
            h1 {{ color: #2c3e50; font-size: 20px; text-align: center; margin-bottom: 5px; }}
            h2 {{ color: #34495e; font-size: 16px; text-align: left; margin-bottom: 10px; margin-top: 30px; border-bottom: 1px solid #ccc; }}
            table {{ border-collapse: collapse; width: 100%; font-size: 11px; margin-bottom: 20px; }}
            tr {{ page-break-inside: avoid; }}
            th {{ background-color: #3498db; color: white; border: 1px solid #bdc3c7; padding: 8px; text-align: left; }}
            td {{ border: 1px solid #bdc3c7; padding: 6px; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    # Gera o PDF diretamente em memória usando xhtml2pdf
    result_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(html_template, dest=result_file)
    
    if pisa_status.err:
        raise Exception(f"Erro ao gerar PDF: {pisa_status.err}")
        
    return result_file.getvalue()
