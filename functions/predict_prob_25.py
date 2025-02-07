# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:07:57 2025

@author: RafaelKujo
"""

def predict_prob_25(df_proxs_intervalo):
    

    from scipy.stats import poisson
    
    max_gols_time = 2.5
    
    
    df_proxs_intervalo[f'prob_max_{max_gols_time}_gols_casa'] = ''
    df_proxs_intervalo[f'prob_max_{max_gols_time}_gols_fora'] = ''
    
    for index, row in df_proxs_intervalo.iterrows():
    
        exp_gols_casa = df_proxs_intervalo.casa_esperado[index]
    
        exp_gols_fora = df_proxs_intervalo.fora_esperado[index]
        
        prob_casa = 0
        
        prob_fora = 0
    
        for gols in range(0,int(max_gols_time+.5)):
        
            prob_casa += poisson.pmf(gols, exp_gols_casa)
            
            prob_fora += poisson.pmf(gols, exp_gols_fora)
        
        df_proxs_intervalo[f'prob_max_{max_gols_time}_gols_casa'][index] =  prob_casa
        df_proxs_intervalo[f'prob_max_{max_gols_time}_gols_fora'][index] =  prob_fora
        
        
    return df_proxs_intervalo