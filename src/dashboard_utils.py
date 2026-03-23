import pandas as pd

def obter_indicadores_principais(df_inscricoes):
    indicadores = {}
    
    if df_inscricoes is not None and not df_inscricoes.empty:
        indicadores['total_inscricoes'] = len(df_inscricoes)
        indicadores['confirmados'] = len(df_inscricoes[df_inscricoes['Status'].str.strip() == 'Ok'])
        indicadores['pendentes'] = len(df_inscricoes[df_inscricoes['Status'].str.strip() == 'Pendente'])
        
        if 'Cancelada?' in df_inscricoes.columns:
            indicadores['cancelados'] = len(df_inscricoes[df_inscricoes['Cancelada?'].str.strip() == 'Sim'])
            indicadores['atrasados'] = len(df_inscricoes[(df_inscricoes['Status'].str.strip() == 'Pendente') & (df_inscricoes['Cancelada?'].str.strip() == 'Não')])
        else:
            indicadores['cancelados'] = 0
            indicadores['atrasados'] = len(df_inscricoes[df_inscricoes['Status'].str.strip() == 'Pendente'])
            
    else:
        indicadores = {
            'total_inscricoes': 0, 'confirmados': 0, 'pendentes': 0, 'cancelados': 0, 'atrasados': 0
        }
        
    return indicadores
