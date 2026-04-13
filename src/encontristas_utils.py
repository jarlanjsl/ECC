import pandas as pd
import io
from src.pdf_utils import dataframe_to_pdf
def gerar_lista_encontristas(df_encontristas, formato='excel'):
    if 'Cancelada?' in df_encontristas.columns:
        df_encontristas = df_encontristas[df_encontristas['Cancelada?'] == 'Não']
        
    if formato == 'pdf':
        return dataframe_to_pdf(df_encontristas, 'Encontristas', 'Lista de Encontristas')
        
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Encontristas', df_encontristas, 'Encontristas', 'Lista de Encontristas')
    output.seek(0)
    return output.getvalue()

def gerar_endereco_encontristas(df_encontristas, formato='excel'):
    if 'Cancelada?' in df_encontristas.columns:
        df_encontristas = df_encontristas[df_encontristas['Cancelada?'] == 'Não']
        
    localizacao = df_encontristas[['Nome', 'Status', 'Nome (Ele):', 'Telefone (Ele):', 'Nome (Ela):', 'Telefone (Ela):', 'Endereço:', 'Número da ficha:']].copy()
    localizacao.columns = ['Responsavel', 'Status', 'Nome (Ele)', 'Telefone (Ele)', 'Nome (Ela)', 'Telefone (Ela)', 'Endereço', 'Numero ficha']
    
    # Adicionando conversão segura e ordenação numérica para a coluna da ficha
    localizacao['Numero ficha'] = pd.to_numeric(localizacao['Numero ficha'], errors='coerce')
    localizacao = localizacao.sort_values(by='Numero ficha', ascending=True, na_position='last')
    
    if formato == 'pdf':
        return dataframe_to_pdf(localizacao, 'Encontristas', 'Endereços')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Enderecos', localizacao, 'Encontristas', 'Endereços')
    output.seek(0)
    return output.getvalue()

def escrever_tabela_formatada(writer, sheet_name, df, titulo1, titulo2, startrow=2, estilo='Table Style Medium 1'):
    workbook = writer.book
    worksheet = workbook.add_worksheet(sheet_name)
    writer.sheets[sheet_name] = worksheet
    
    formato_titulo = workbook.add_format({'bold': True, 'font_size': 12})
    worksheet.write('A1', titulo1, formato_titulo)
    worksheet.write('A2', titulo2, formato_titulo)
    
    df.to_excel(writer, sheet_name=sheet_name, startrow=startrow, index=False)
    
    nlinhas, ncols = df.shape
    worksheet.add_table(
        startrow, 0, startrow + nlinhas, max(0, ncols - 1),
        {
            'name': f'Tabela_{sheet_name.replace(" ", "_")}',
            'columns': [{'header': col} for col in df.columns],
            'style': estilo
        }
    )
    
    for col_idx, col in enumerate(df.columns):
        max_len = len(str(col))
        if nlinhas > 0:
            col_max = df.iloc[:, col_idx].astype(str).str.len().max()
            if pd.notna(col_max):
                max_len = max(max_len, int(col_max))
        worksheet.set_column(col_idx, col_idx, max_len + 2)
    return worksheet

def gerar_camisas_encontristas(df_encontristas, formato='excel'):
    if 'Cancelada?' in df_encontristas.columns:
        df_encontristas = df_encontristas[df_encontristas['Cancelada?'] == 'Não']
        
    # Lista Camisas Casal
    camisas = df_encontristas[['Como Gostaria de ser chamado? ', 'Tamanho Camisa (Ele):', 'Como Gostaria de ser chamada?', 'Tamanho Camisa (Ela):']].copy()
    camisas.columns = ['ELE', 'CAMISA ELE', 'ELA', 'CAMISA ELA']
    camisas['ELE'] = camisas['ELE'].str.title()
    camisas['ELA'] = camisas['ELA'].str.title()
    camisas['CAMISA ELE'] = camisas['CAMISA ELE'].str.upper()
    camisas['CAMISA ELA'] = camisas['CAMISA ELA'].str.upper()
    lista_camisas_casal = camisas.sort_values(by=['CAMISA ELE', 'CAMISA ELA'], ascending=[True, True])
    
    # Resumo e Lista
    camisas_ele = df_encontristas[['Como Gostaria de ser chamado? ', 'Tamanho Camisa (Ele):']].copy()
    camisas_ela = df_encontristas[['Como Gostaria de ser chamada?', 'Tamanho Camisa (Ela):']].copy()
    
    camisas_ele.columns = ['NOME', 'TAMANHO']
    camisas_ela.columns = ['NOME', 'TAMANHO']
    camisas_ele['NOME'] = camisas_ele['NOME'].str.title()
    camisas_ela['NOME'] = camisas_ela['NOME'].str.title()
    camisas_ele['TAMANHO'] = camisas_ele['TAMANHO'].str.upper()
    camisas_ela['TAMANHO'] = camisas_ela['TAMANHO'].str.upper()
    
    lista_camisas = pd.concat([camisas_ele, camisas_ela], ignore_index=True)
    lista_camisas = lista_camisas.sort_values(by='TAMANHO', ascending=True)
    resumo_camisas = lista_camisas['TAMANHO'].value_counts().reset_index()
    resumo_camisas.columns = ['TAMANHO', 'count']
    
    if formato == 'pdf':
        return dataframe_to_pdf([
            ('Lista de Camisas', lista_camisas),
            ('Resumo das Camisas', resumo_camisas),
            ('Lista de Camisas por Casal', lista_camisas_casal)
        ], 'Encontristas')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Lista', lista_camisas, 'Encontristas', 'Lista de Camisas')
        escrever_tabela_formatada(writer, 'Resumo', resumo_camisas, 'Encontristas', 'Resumo das Camisas')
        escrever_tabela_formatada(writer, 'Lista Casais', lista_camisas_casal, 'Encontristas', 'Lista de Camisas por Casal')
    
    output.seek(0)
    return output.getvalue()

def gerar_lista_circulos_encontristas(df_encontristas, formato='excel'):
    if 'Cancelada?' in df_encontristas.columns:
        df_encontristas = df_encontristas[df_encontristas['Cancelada?'] == 'Não']
        
    circulos = df_encontristas[['Número da ficha:', 'Como Gostaria de ser chamado? ', 'Tamanho Camisa (Ele):', 'Como Gostaria de ser chamada?', 'Tamanho Camisa (Ela):', 'Endereço:']].copy()
    circulos.columns = ['Numero Ficha', 'Nome Ele', 'Camisa Ele', 'Nome Ela', 'Camisa Ela', 'Endereço']
    
    circulos['Numero Ficha'] = pd.to_numeric(circulos['Numero Ficha'], errors='coerce')
    circulos = circulos.sort_values(by='Numero Ficha', ascending=True, na_position='last')
    
    if formato == 'pdf':
        return dataframe_to_pdf(circulos, 'Encontristas', 'Lista para Círculos')
        
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Circulos', circulos, 'Encontristas', 'Lista para Círculos')
    output.seek(0)
    return output.getvalue()
