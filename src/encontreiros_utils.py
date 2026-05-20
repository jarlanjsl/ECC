import pandas as pd
import io
from src.pdf_utils import dataframe_to_pdf
def filtrar_ativos(df_inscricoes):
    filtro = df_inscricoes['Cancelada?'] == 'Não'
    return df_inscricoes[filtro]

def gerar_lista_equipes(df_inscricoes, formato='excel'):
    df_filtrado = filtrar_ativos(df_inscricoes).copy()
    
    equipes = df_filtrado[['Nome Crachá (Ele):', 'Telefone (Ele)', 'Nome Crachá (Ela):', 'Telefone (Ela)', 'Em qual equipe deseja trabalhar :', 'Data da inscrição']].copy()
    equipes.columns = ['ELE', 'CONTATO ELE', 'ELA', 'CONTATO ELA', 'EQUIPE', 'DATA INSCRIÇÃO']
    equipes['ELE'] = equipes['ELE'].str.title()
    equipes['ELA'] = equipes['ELA'].str.title()
    equipes['DATA INSCRIÇÃO'] = pd.to_datetime(equipes['DATA INSCRIÇÃO'], dayfirst=True)
    
    lista_equipes = equipes.sort_values(by=['EQUIPE', 'DATA INSCRIÇÃO'])
    
    if formato == 'pdf':
        return dataframe_to_pdf(lista_equipes, 'Encontreiros', 'Lista de Equipes')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Equipes', lista_equipes, 'Encontreiros', 'Lista de Equipes')
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

def gerar_todas_camisas(df_inscricoes, formato='excel'):
    df_filtrado = filtrar_ativos(df_inscricoes).copy()
    
    # 1. Lista Camisas Casal
    camisas = df_filtrado[['Nome Crachá (Ele):', 'Tamanho Camisa (Ele):', 'Nome Crachá (Ela):', 'Tamanho Camisa (Ela):']].copy()
    camisas.columns = ['ELE', 'CAMISA ELE', 'ELA', 'CAMISA ELA']
    camisas['ELE'] = camisas['ELE'].str.title()
    camisas['ELA'] = camisas['ELA'].str.title()
    camisas['CAMISA ELE'] = camisas['CAMISA ELE'].str.upper()
    camisas['CAMISA ELA'] = camisas['CAMISA ELA'].str.upper()
    lista_camisas_casal = camisas.sort_values(by=['CAMISA ELE', 'CAMISA ELA'], ascending=[True, True])
    
    # 2. Resumo e Lista Individual
    camisas_ele = df_filtrado[['Nome Crachá (Ele):', 'Tamanho Camisa (Ele):']].copy()
    camisas_ela = df_filtrado[['Nome Crachá (Ela):', 'Tamanho Camisa (Ela):']].copy()
    
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
        ], 'Encontreiros')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Lista', lista_camisas, 'Encontreiros', 'Lista de Camisas')
        escrever_tabela_formatada(writer, 'Resumo', resumo_camisas, 'Encontreiros', 'Resumo das Camisas')
        escrever_tabela_formatada(writer, 'Lista Casais', lista_camisas_casal, 'Encontreiros', 'Lista de Camisas por Casal')
    
    output.seek(0)
    return output.getvalue()

def gerar_relacao_pagamento(df_financeiro, formato='excel'):
    filtro_financeiro = df_financeiro['Tipo'] == 'C'
    df_filtrado_financeiro = df_financeiro[filtro_financeiro].copy()
    
    pagamento = df_filtrado_financeiro[['Pagamento', 'Nome do inscrito', 'Descrição', 'Valor']].copy()
    pagamento.columns = ['DATA', 'NOME', 'DESCRIÇÃO', 'VALOR']
    pagamento['NOME'] = pagamento['NOME'].str.title()
    pagamento['DATA'] = pd.to_datetime(pagamento['DATA'], dayfirst=True)
    relacao_pagamento = pagamento.sort_values(by='DATA')
    
    if formato == 'pdf':
        return dataframe_to_pdf(relacao_pagamento, 'Financeiro', 'Relação de Pagamentos')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Pagamentos', relacao_pagamento, 'Financeiro', 'Relação de Pagamentos')
    output.seek(0)


def gerar_relatorio_status(df_inscricoes, formato='excel'):
    df_filtrado = filtrar_ativos(df_inscricoes).copy()
    
    colunas_necessarias = [
        'Nome Crachá (Ele):', 'Telefone (Ele)', 
        'Nome Crachá (Ela):', 'Telefone (Ela)', 
        'Status', 'Em qual equipe deseja trabalhar :'
    ]
    
    # Verifica quais colunas realmente existem para evitar erros caso a planilha mude
    colunas_presentes = [col for col in colunas_necessarias if col in df_filtrado.columns]
    status_df = df_filtrado[colunas_presentes].copy()
    
    # Renomear colunas se elas existirem
    mapa_colunas = {
        'Nome Crachá (Ele):': 'NOME (ELE)',
        'Telefone (Ele)': 'TELEFONE (ELE)',
        'Nome Crachá (Ela):': 'NOME (ELA)',
        'Telefone (Ela)': 'TELEFONE (ELA)',
        'Status': 'STATUS',
        'Em qual equipe deseja trabalhar :': 'EQUIPE DESEJADA'
    }
    status_df.rename(columns=mapa_colunas, inplace=True)
    
    # Formatar nomes
    for col in ['NOME (ELE)', 'NOME (ELA)']:
        if col in status_df.columns:
            status_df[col] = status_df[col].astype(str).str.title()
            
    # Ordenar por status e equipe
    cols_sort = [c for c in ['STATUS', 'EQUIPE DESEJADA'] if c in status_df.columns]
    if cols_sort:
        status_df = status_df.sort_values(by=cols_sort)
    
    if formato == 'pdf':
        return dataframe_to_pdf(status_df, 'Encontreiros', 'Relatório de Status')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Status', status_df, 'Encontreiros', 'Relatório de Status')
    output.seek(0)
    return output.getvalue()
