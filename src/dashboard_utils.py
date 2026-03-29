import pandas as pd

def obter_indicadores_principais(df_inscricoes):
    indicadores = {
        'total_inscricoes': 0, 'confirmados': 0, 'pendentes': 0, 'cancelados': 0, 'atrasados': 0
    }
    
    if df_inscricoes is not None and not df_inscricoes.empty:
        # Tratamento da coluna de cancelamento
        if 'Cancelada?' in df_inscricoes.columns:
            serie_cancelado = df_inscricoes['Cancelada?'].astype(str).str.strip().str.upper()
            indicadores['cancelados'] = len(df_inscricoes[serie_cancelado == 'SIM'])
        elif 'Cancelado' in df_inscricoes.columns:
            serie_cancelado = df_inscricoes['Cancelado'].astype(str).str.strip().str.upper()
            indicadores['cancelados'] = len(df_inscricoes[serie_cancelado == 'SIM'])
        else:
            serie_cancelado = pd.Series(['NÃO'] * len(df_inscricoes), index=df_inscricoes.index)
            indicadores['cancelados'] = 0
            
        # Tratamento da coluna de status
        if 'Status' in df_inscricoes.columns:
            serie_status = df_inscricoes['Status'].astype(str).str.strip().str.upper()
        else:
            serie_status = pd.Series([''] * len(df_inscricoes), index=df_inscricoes.index)

        # Regra 1: Total Inscritos é quando Cancelado = Não
        indicadores['total_inscricoes'] = len(df_inscricoes[serie_cancelado == 'NÃO'])
        
        # Regra 2: Confirmados é quando o Status = OK
        indicadores['confirmados'] = len(df_inscricoes[serie_status == 'OK'])
        
        # Regra 3: Pendentes é quando Status = Pendentes e Cancelado = Não
        indicadores['pendentes'] = len(df_inscricoes[
            (serie_status.isin(['PENDENTE', 'PENDENTES'])) & 
            (serie_cancelado == 'NÃO')
        ])
        
        # Manter a chave 'atrasados' zerada caso seja usada em outro lugar do código
        indicadores['atrasados'] = 0
        
    return indicadores
