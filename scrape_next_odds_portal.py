# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 17:03:01 2024

@author: RafaelKujo
"""

from datetime import datetime, timedelta
import os


from functions.busca_ligas import busca_ligas
from functions.gerar_proxs_intervalo import gerar_proxs_intervalo
from functions.busca_odds_proxs import busca_odds_proxs
from functions.predict_goals import predict_goals
from functions.predict_prob_25 import predict_prob_25
from functions.gerar_bets import gerar_bets
from functions.envio_email_bets import envio_email_bets



# VER ARQUIVOS NA ORDEM INVERSA: TODOS, PROXS SEM ODD, PROXS COM ODD, BETS

hoje = datetime.today().date()
print(hoje)

opcao = input('Selecione a opção (meio de semana; fim de semana): ')


if opcao == 'fim de semana':
    inicio = hoje + timedelta(days=(4 - hoje.weekday()) % 7)  # Next Friday
    if inicio == hoje:  # If today is already Friday, check for Saturday instead
        inicio += timedelta(days=1)
else:  # 'meio de semana'
    inicio = hoje + timedelta(days=(1 - hoje.weekday()) % 7)  # Next Tuesday
    if inicio == hoje:  # If today is already Tuesday, check for Wednesday instead
        inicio += timedelta(days=1)




if os.path.exists(f'bets_{opcao}_{inicio}.pkl') == True: ## já tem o bets
    
    import pandas as pd

    ## imprimir o df bets para o período selecionado
    bets = pd.read_pickle(f'bets_{opcao}_{inicio}.pkl')

    print('Arquivo já existente.')    
    print(bets)
    
else: # bets nao existe
    
    if os.path.exists(f'proxs_{opcao}_{inicio}.pkl') == True: # já tem os proxs com odds
        
        ## rodar a partir do cálculo de und2.5 e geeração de bets
        
        df_proxs_intervalo = pd.read_pickle(f'proxs_{opcao}_{inicio}.pkl')
        
        df_proxs_intervalo = predict_prob_25(df_proxs_intervalo)
        
        
        threshold = .85
        
        bets = gerar_bets(df_proxs_intervalo, threshold, opcao, inicio)
        
        
        
        receivers = ['rkujomonteiro@gmail.com',
                     'luigisaldanha@hotmail.com']
        
        envio_email_bets(bets, opcao, inicio, receivers)
        
        
 
        
    else: # nem bets nem proxs com odds existem
        
        if os.path.exists(f'proxs_{opcao}_{inicio}_sem_odds.pkl') == True: # já tem o proxs mas sem odds
            
            ## rodar a partir da busca de odds
            
            df_proxs_intervalo = pd.read_pickle(f'proxs_{opcao}_{inicio}_sem_odds.pkl')
            
            df_proxs_intervalo = busca_odds_proxs(df_proxs_intervalo, 'bet365')
            
            df_proxs_intervalo = predict_goals(df_proxs_intervalo, opcao, inicio)
            
            df_proxs_intervalo = predict_prob_25(df_proxs_intervalo)
            
            
            threshold = .85
            
            bets = gerar_bets(df_proxs_intervalo, threshold, opcao, inicio)
            
            
            
            receivers = ['rkujomonteiro@gmail.com',
                         'luigisaldanha@hotmail.com']
            
            envio_email_bets(bets, opcao, inicio, receivers)
            
            
            
        else: # nem bets nem proxs sem odds existem
            
            if os.path.exists(f'todos_proxs_{hoje}.pkl') == True: # já foi feita busca de proxs hoje
            
                ## seguir a partir dos proxs com opcao gerando o df_proxs_intervalo
                
                df_proxs = pd.read_pickle(f'todos_proxs_{hoje}.pkl')
                
                df_proxs_intervalo = gerar_proxs_intervalo(opcao, inicio, df_proxs)
                
                df_proxs_intervalo = busca_odds_proxs(df_proxs_intervalo, 'bet365')
                
                df_proxs_intervalo = predict_goals(df_proxs_intervalo, opcao, inicio)
                
                df_proxs_intervalo = predict_prob_25(df_proxs_intervalo)
                
                
                threshold = .85
                
                bets = gerar_bets(df_proxs_intervalo, threshold, opcao, inicio)
                
                
                
                receivers = ['rkujomonteiro@gmail.com',
                             'luigisaldanha@hotmail.com']
                
                envio_email_bets(bets, opcao, inicio, receivers)
                
            else: # não existe nada
            

                df_proxs = busca_ligas(hoje)
                
                df_proxs_intervalo = gerar_proxs_intervalo(opcao, inicio, df_proxs)
                
                df_proxs_intervalo = busca_odds_proxs(df_proxs_intervalo, 'bet365')
                
                df_proxs_intervalo = predict_goals(df_proxs_intervalo, opcao, inicio)
                
                df_proxs_intervalo = predict_prob_25(df_proxs_intervalo)
                
                
                threshold = .85
                
                bets = gerar_bets(df_proxs_intervalo, threshold, opcao, inicio)
                
                
                
                receivers = ['rkujomonteiro@gmail.com',
                             'luigisaldanha@hotmail.com']
                
                envio_email_bets(bets, opcao, inicio, receivers)