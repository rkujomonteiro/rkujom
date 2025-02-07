# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:05:56 2025

@author: RafaelKujo
"""

def predict_goals(df_proxs_intervalo, opcao, inicio):


    import pandas as pd
    
    
    colunas_converter_float = ['odd_casa_jogo',
                               'odd_emp_jogo',
                               'odd_fora_jogo',
                               'odd_bts_sim_jogo',
                               'odd_bts_nao_jogo',
                               'odd_over35',
                               'odd_under35',
                               'odd_over45',
                               'odd_under45']
    
    
    
    for coluna in colunas_converter_float:
        df_proxs_intervalo[coluna] = df_proxs_intervalo[coluna].astype(float)
    
    
    
    ''' importando summary_df e rodando modelo para os proxs'''
    
    
    summary_df_casa = pd.read_pickle('summary_df_casa.pkl')
    summary_df_fora = pd.read_pickle('summary_df_fora.pkl')
    
    
    
    df_proxs_intervalo['casa_esperado'] = ''
    df_proxs_intervalo['fora_esperado'] = ''
    
    
    for index, row in df_proxs_intervalo.iterrows():
        
        summary_df_casa_liga = summary_df_casa[summary_df_casa.Liga == df_proxs_intervalo.liga[index]]
        
        casa_esperado = summary_df_casa_liga['Coef.']['const']
        
        for index2, row in summary_df_casa_liga.iterrows():
            
            if index2 != 'const':
                
                casa_esperado += summary_df_casa_liga['Coef.'][index2] * df_proxs_intervalo[index2][index]
        
        df_proxs_intervalo['casa_esperado'][index] = casa_esperado
        
        
    for index, row in df_proxs_intervalo.iterrows():
        
        summary_df_fora_liga = summary_df_fora[summary_df_fora.Liga == df_proxs_intervalo.liga[index]]
        
        fora_esperado = summary_df_fora_liga['Coef.']['const']
        
        for index2, row in summary_df_fora_liga.iterrows():
            
            if index2 != 'const':
                
                fora_esperado += summary_df_fora_liga['Coef.'][index2] * df_proxs_intervalo[index2][index]
        
        df_proxs_intervalo['fora_esperado'][index] = fora_esperado    
    
    
    
    
    
    ''' SALVANDO O DF_PROXS_INTERVALO JA COM AS ODDS E GOLS ESPERADOS '''
    
    
    df_proxs_intervalo.to_pickle(f'proxs_{opcao}_{inicio}.pkl')
    
    
    return df_proxs_intervalo