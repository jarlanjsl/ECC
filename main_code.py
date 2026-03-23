import pandas as pd

df_inscricoes = pd.read_csv('arquivos\\encontreiros.csv', sep=';', encoding='latin-1')
df_financeiro = pd.read_csv('arquivos\\conta_financeira.csv', sep=';')

#Filtrando Inscrições - Cancelado = Não
filtro = df_inscricoes['Cancelada?'] == 'Não'
df_filtrado = df_inscricoes[filtro]

#Filtrando Financeiro - Tipo = C
filtro_financeiro = df_financeiro['Tipo'] == 'C'
df_filtrado_financeiro = df_financeiro[filtro_financeiro]

df_filtrado

#Selecionar colunas
equipes = df_filtrado[['Nome Crachá (Ele):', 'Telefone (Ele)', 'Nome Crachá (Ela):', 'Telefone (Ela)', 'Em qual equipe deseja trabalhar :', 'Data da inscrição']]

#Renomear colunas
equipes.columns = ['ELE', 'CONTATO ELE', 'ELA', 'CONTATO ELA', 'EQUIPE', 'DATA INSCRIÇÃO']
equipes['ELE'] = equipes['ELE'].str.title()
equipes['ELA'] = equipes['ELA'].str.title()
equipes['DATA INSCRIÇÃO'] = pd.to_datetime(equipes['DATA INSCRIÇÃO'], dayfirst=True)

#Ordenar por equipe
lista_equipes = equipes.sort_values(by=['EQUIPE', 'DATA INSCRIÇÃO'])

#Exportar relatório
lista_equipes.to_excel('export\\lista_equipes.xlsx', index=False)

lista_equipes.info()

lista_equipes

#Selecionar colunas
camisas = df_filtrado[['Nome Crachá (Ele):', 'Tamanho Camisa (Ele):', 'Nome Crachá (Ela):', 'Tamanho Camisa (Ela):']]

#Renomear colunas
camisas.columns = ['ELE', 'CAMISA ELE', 'ELA', 'CAMISA ELA']
camisas['ELE'] = camisas['ELE'].str.title()
camisas['ELA'] = camisas['ELA'].str.title()
camisas['CAMISA ELE'] = camisas['CAMISA ELE'].str.upper()
camisas['CAMISA ELA'] = camisas['CAMISA ELA'].str.upper()

#Ordenar por Tamanho
lista_camisas_casal = camisas.sort_values(by=['CAMISA ELE', 'CAMISA ELA'], ascending=[True, True])

#Exportar relatório
lista_camisas_casal.to_excel('export\\lista_camisas_casal.xlsx', index=False)

lista_camisas_casal

#Selecionar colunas
camisas_ele = df_filtrado[['Nome Crachá (Ele):', 'Tamanho Camisa (Ele):']]
camisas_ela = df_filtrado[['Nome Crachá (Ela):', 'Tamanho Camisa (Ela):']]

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

# #Exportar relatório
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

with pd.ExcelWriter('export/encontreiros_camisas.xlsx', engine='xlsxwriter') as writer:

    escrever_tabela_formatada(
        writer,
        sheet_name='Lista',
        df=lista_camisas,
        titulo1='Encontreiros',
        titulo2='Lista de Camisas'
    )

    escrever_tabela_formatada(
        writer,
        sheet_name='Resumo',
        df=resumo_camisas.reset_index(),  # inclui índice como coluna
        titulo1='Encontreiros',
        titulo2='Resumo das Camisas'
    )

    escrever_tabela_formatada(
        writer,
        sheet_name='Lista Casais',
        df=lista_camisas_casal,
        titulo1='Encontreiros',
        titulo2='Lista de Camisas por Casal'
    )


lista_camisas

resumo_camisas

#Selecionar colunas
pagamento = df_filtrado_financeiro[['Pagamento', 'Nome do inscrito', 'Descrição', 'Valor']]

#Renomear colunas
pagamento.columns = ['DATA', 'NOME', 'DESCRIÇÃO', 'VALOR']
pagamento['NOME'] = pagamento['NOME'].str.title()
pagamento['DATA'] = pd.to_datetime(pagamento['DATA'], dayfirst=True)

#Ordenar por Data
relacao_pagamento = pagamento.sort_values(by='DATA')

#Exportar relatório
relacao_pagamento.to_excel('export\\relacao_pagamento.xlsx', index=False)

relacao_pagamento

#Lista do sorteio
sorteio_array = pagamento['NOME'].unique()

#Lista em dataframe
sorteio = pd.DataFrame(sorteio_array, columns=['NOME'])

#Ordenar pelo Nome
lista_sorteio = sorteio.sort_values(by='NOME')

#Exportar relatório
lista_sorteio.to_excel('export\\sorteio.xlsx', index=False)

lista_sorteio

lista_sorteio.info()

sorteados = pd.read_csv('arquivos\\sorteados.csv', sep=';')

sorteados['Nome Casal'] = sorteados['Nome Casal'].str.title()

sorteados

# 1. Garantir padronização nas chaves de busca para o Merge
df_filtrado['Nome'] = df_filtrado['Nome'].str.strip().str.title()
lista_sorteio['NOME'] = lista_sorteio['NOME'].str.strip().str.title()

# 2. Realizando o 'PROCV' (Merge) incluindo a coluna da Igreja
lista_sorteio_completa = pd.merge(
    lista_sorteio, 
    df_filtrado[['Nome', 'Nome Crachá (Ele):', 'Telefone (Ele)', 'Nome Crachá (Ela):', 'Telefone (Ela)', 'Igreja em que congregam:']],
    left_on='NOME', 
    right_on='Nome', 
    how='left'
)
# Coloque isso após o Passo 2 para ver quem deu erro no "PROCV"
casais_nao_encontrados = lista_sorteio_completa[lista_sorteio_completa['Nome'].isna()]
print("Nomes na lista de sorteio que não foram encontrados no df_filtrado:")
print(casais_nao_encontrados['NOME'])

# 3. Criando a coluna 'Nome Casal'
lista_sorteio_completa['Nome Casal'] = (
    lista_sorteio_completa['Nome Crachá (Ele):'].str.title() + 
    ' e ' + 
    lista_sorteio_completa['Nome Crachá (Ela):'].str.title()
)

# 4. Selecionando colunas e REMOVENDO DUPLICADOS (Unique)
lista_final = lista_sorteio_completa[['Nome Casal', 'Telefone (Ele)', 'Telefone (Ela)', 'Igreja em que congregam:']]
lista_final = lista_final.drop_duplicates(subset=['Nome Casal']) # <--- Adicionado aqui

# 5. Remoção de quem já foi sorteado
lista_final['NOME_COMPARA'] = lista_final['Nome Casal'].str.upper().str.strip()
sorteados['NOME_COMPARA'] = sorteados['Nome Casal'].str.upper().str.strip()

lista_final_disponivel = lista_final[~lista_final['NOME_COMPARA'].isin(sorteados['NOME_COMPARA'])].copy()

# 6. Limpeza e exportação
lista_final_disponivel.drop(columns=['NOME_COMPARA'], inplace=True)
lista_final_disponivel.to_excel('export\\lista_sorteio.xlsx', index=False)

# Resultados
print(f"Total de casais únicos: {len(lista_final)}")
print(f"Restantes para o sorteio (após remover ganhadores): {len(lista_final_disponivel)}")

lista_final_disponivel

# 1. Padronização dos nomes das Igrejas
# Remove espaços extras, converte para Title Case (Cada Palavra Iniciada em Maiúscula)
lista_final_disponivel['Igreja em que congregam:'] = lista_final_disponivel['Igreja em que congregam:'].str.strip().str.title()

# 2. Criar a análise por Igreja (Contagem)
analise_igreja = lista_final_disponivel['Igreja em que congregam:'].value_counts().reset_index()
analise_igreja.columns = ['IGREJA', 'QUANTIDADE DE CASAIS']

# 3. Ordenar pela quantidade (do maior para o menor)
analise_igreja = analise_igreja.sort_values(by='QUANTIDADE DE CASAIS', ascending=False)

# 4. Exportar a análise
analise_igreja.to_excel('export\\analise_por_igreja.xlsx', index=False)

# Visualizar o resumo
print("Resumo de Casais por Igreja:")
analise_igreja

