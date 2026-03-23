import pandas as pd

df_encontristas = pd.read_csv('arquivos\\encontristas.csv', sep=';', encoding='latin-1')

df_encontristas.to_excel('export\\lista_encontristas.xlsx', index=False)

df_encontristas.head()

df_encontristas.info()

localizacao = df_encontristas[['Nome', 'Status', 'Nome (Ele):', 'Telefone (Ele):', 'Nome (Ela):', 'Telefone (Ela):', 'Endereço:', 'Número da ficha:']]

localizacao.columns = ['Responsavel', 'Status', 'Nome (Ele)', 'Telefone (Ele)', 'Nome (Ela)', 'Telefone (Ela)', 'Endereço', 'Numero ficha']

localizacao

localizacao.to_excel('export\\endereco_encontristas.xlsx', index=False)

#Selecionar colunas
camisas = df_encontristas[['Como Gostaria de ser chamado? ', 'Tamanho Camisa (Ele):', 'Como Gostaria de ser chamada?', 'Tamanho Camisa (Ela):']]

#Renomear colunas
camisas.columns = ['ELE', 'CAMISA ELE', 'ELA', 'CAMISA ELA']
camisas['ELE'] = camisas['ELE'].str.title()
camisas['ELA'] = camisas['ELA'].str.title()
camisas['CAMISA ELE'] = camisas['CAMISA ELE'].str.upper()
camisas['CAMISA ELA'] = camisas['CAMISA ELA'].str.upper()

#Ordenar por Tamanho
lista_camisas_casal = camisas.sort_values(by=['CAMISA ELE', 'CAMISA ELA'], ascending=[True, True])

#Exportar relatório
lista_camisas_casal.to_excel('export\\encontristas_camisas_casal.xlsx', index=False)

#Selecionar colunas
camisas_ele = df_encontristas[['Como Gostaria de ser chamado? ', 'Tamanho Camisa (Ele):']]
camisas_ela = df_encontristas[['Como Gostaria de ser chamada?', 'Tamanho Camisa (Ela):']]

#Renomear colunas
camisas_ele.columns = ['NOME', 'TAMANHO']
camisas_ela.columns = ['NOME', 'TAMANHO']
camisas_ele['NOME'] = camisas_ele['NOME'].str.title()
camisas_ela['NOME'] = camisas_ela['NOME'].str.title()
camisas_ele['TAMANHO'] = camisas_ele['TAMANHO'].str.upper()
camisas_ela['TAMANHO'] = camisas_ela['TAMANHO'].str.upper()

#Juntar datasets - camisas_ele + camisas_ela
lista_camisas = pd.concat([camisas_ele, camisas_ela], ignore_index=True)

#Ordenar por Tamanho
lista_camisas = lista_camisas.sort_values(by='TAMANHO', ascending=True)

#Resumo Camisas
resumo_camisas = lista_camisas['TAMANHO'].value_counts()

#Exportar relatório
def escrever_tabela_formatada(writer, sheet_name, df, titulo1, titulo2, startrow=2, estilo='Table Style Medium 1'):
    workbook = writer.book

    # Criar worksheet
    worksheet = workbook.add_worksheet(sheet_name)
    writer.sheets[sheet_name] = worksheet

    # Formato do título
    formato_titulo = workbook.add_format({
        'bold': True,
        'font_size': 12
    })

    # Escrever títulos
    worksheet.write('A1', titulo1, formato_titulo)
    worksheet.write('A2', titulo2, formato_titulo)

    # Escrever DataFrame
    df.to_excel(writer, sheet_name=sheet_name, startrow=startrow, index=False)

    # Criar tabela
    nlinhas, ncols = df.shape
    worksheet.add_table(
        startrow, 0, startrow + nlinhas, ncols - 1,
        {
            'name': f'Tabela_{sheet_name.replace(" ", "_")}',
            'columns': [{'header': col} for col in df.columns],
            'style': estilo
        }
    )

    # --- Autoajuste das colunas ---
    for col_idx, col in enumerate(df.columns):
        # tamanho do cabeçalho
        max_len = len(str(col))

        # tamanho máximo dos valores da coluna
        max_len = max(max_len, *(df[col].astype(str).map(len)))

        # margem para não ficar apertado
        worksheet.set_column(col_idx, col_idx, max_len + 2)

    return worksheet

with pd.ExcelWriter('export/encontristas_camisas.xlsx', engine='xlsxwriter') as writer:

    escrever_tabela_formatada(
        writer,
        sheet_name='Lista',
        df=lista_camisas,
        titulo1='Encontristas',
        titulo2='Lista de Camisas'
    )

    escrever_tabela_formatada(
        writer,
        sheet_name='Resumo',
        df=resumo_camisas.reset_index(),  # inclui índice como coluna
        titulo1='Encontristas',
        titulo2='Resumo das Camisas'
    )

    escrever_tabela_formatada(
        writer,
        sheet_name='Lista Casais',
        df=lista_camisas_casal,
        titulo1='Encontristas',
        titulo2='Lista de Camisas por Casal'
    )


resumo_camisas

