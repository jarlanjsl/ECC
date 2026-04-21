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
    return output.getvalue()

def gerar_lista_sorteio(df_inscricoes, df_financeiro, df_sorteados, formato='excel'):
    df_filtrado = filtrar_ativos(df_inscricoes).copy()
    df_filtrado_financeiro = df_financeiro[df_financeiro['Tipo'] == 'C'].copy()
    
    df_filtrado_financeiro['Nome do inscrito'] = df_filtrado_financeiro['Nome do inscrito'].str.title()
    sorteio_array = df_filtrado_financeiro['Nome do inscrito'].unique()
    lista_sorteio = pd.DataFrame(sorteio_array, columns=['NOME'])
    
    df_filtrado['Nome'] = df_filtrado['Nome'].str.strip().str.title()
    lista_sorteio['NOME'] = lista_sorteio['NOME'].str.strip().str.title()
    
    def remove_accents(s):
        return s.astype(str).str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    lista_sorteio['NOME_MERGE'] = remove_accents(lista_sorteio['NOME']).str.upper()
    df_filtrado['NOME_MERGE'] = remove_accents(df_filtrado['Nome']).str.upper()
    
    lista_sorteio_completa = pd.merge(
        lista_sorteio, 
        df_filtrado[['NOME_MERGE', 'Nome', 'Nome Crachá (Ele):', 'Telefone (Ele)', 'Nome Crachá (Ela):', 'Telefone (Ela)', 'Igreja em que congregam:']],
        on='NOME_MERGE', 
        how='left'
    )
    
    # Se faltarem Nomes Crachá por causa de dados incompletos, preencher com Vazio para evitar erro ao concatenar
    lista_sorteio_completa['Nome Crachá (Ele):'] = lista_sorteio_completa['Nome Crachá (Ele):'].fillna('')
    lista_sorteio_completa['Nome Crachá (Ela):'] = lista_sorteio_completa['Nome Crachá (Ela):'].fillna('')

    lista_sorteio_completa['Nome Casal'] = (
        lista_sorteio_completa['Nome Crachá (Ele):'].str.title() + 
        ' e ' + 
        lista_sorteio_completa['Nome Crachá (Ela):'].str.title()
    )
    
    lista_final = lista_sorteio_completa[['Nome Casal', 'Telefone (Ele)', 'Telefone (Ela)', 'Igreja em que congregam:']].copy()
    lista_final = lista_final.drop_duplicates(subset=['Nome Casal'])
    
    lista_final['NOME_COMPARA'] = remove_accents(lista_final['Nome Casal']).str.upper().str.strip()
    
    if df_sorteados is not None and not df_sorteados.empty:
        df_sorteados['NOME_COMPARA'] = remove_accents(df_sorteados['Nome Casal']).str.upper().str.strip()
        lista_final_disponivel = lista_final[~lista_final['NOME_COMPARA'].isin(df_sorteados['NOME_COMPARA'])].copy()
    else:
        lista_final_disponivel = lista_final.copy()
        
    lista_final_disponivel.drop(columns=['NOME_COMPARA'], inplace=True, errors='ignore')
    
    if formato == 'pdf':
        return dataframe_to_pdf(lista_final_disponivel, 'Eventos', 'Lista para Sorteio')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Sorteio', lista_final_disponivel, 'Eventos', 'Lista para Sorteio')
    output.seek(0)
    return output.getvalue()

def gerar_analise_igrejas(df_inscricoes, formato='excel'):
    df_filtrado = filtrar_ativos(df_inscricoes).copy()
    df_filtrado['Igreja em que congregam:'] = df_filtrado['Igreja em que congregam:'].astype(str).str.strip().str.title()
    analise_igreja = df_filtrado['Igreja em que congregam:'].value_counts().reset_index()
    analise_igreja.columns = ['IGREJA', 'QUANTIDADE DE CASAIS']
    analise_igreja = analise_igreja.sort_values(by='QUANTIDADE DE CASAIS', ascending=False)
    
    if formato == 'pdf':
        return dataframe_to_pdf(analise_igreja, 'Encontreiros', 'Análise por Igrejas')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        escrever_tabela_formatada(writer, 'Analise_Igrejas', analise_igreja, 'Encontreiros', 'Análise por Igrejas')
    output.seek(0)
    return output.getvalue()
