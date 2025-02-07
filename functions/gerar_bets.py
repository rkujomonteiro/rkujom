# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:09:55 2025

@author: RafaelKujo
"""

from itertools import combinations
import pandas as pd


def gerar_bets(df, threshold, opcao, inicio):
    # Melt the dataframe to get all probabilities in one column along with their respective teams
    lista_probs = list(df['prob_max_2.5_gols_casa']) + list(df['prob_max_2.5_gols_fora'])
    lista_times = list(df['casa']) + list(df['fora'])
    
    df_melted = pd.DataFrame({'time': lista_times, 'prob': lista_probs})
    
    # Filter teams with probability above threshold
    df_filtered = df_melted[df_melted['prob'] > threshold]
    
    # If less than 8 teams, return empty DataFrame
    num_teams = len(df_filtered)
    
    if num_teams < 8:
        return pd.DataFrame(), "Not enough teams to recommend bets."
    
    # If more than 20 teams, take the top 20
    if num_teams > 20:
        df_filtered = df_filtered.nlargest(20, 'prob')
    
    
    lista_odd_real = []
    lista_time_excluir = []
    
    for team in df_filtered.time:
        
        while True:
            
            odd_time = float(input(f'Odd under2.5 para {team} (Se não houver, inserir 0): '))
            
            if odd_time == 0:
            
                lista_time_excluir.append(team)
                lista_odd_real.append(odd_time)
                break
                
            elif odd_time > 0:
            
                lista_odd_real.append(odd_time)
                break
                
            else:
                
                print('Odd menor que 0 inválida.')
                odd_time = float(input(f'Odd under2.5 para {team} (Se não houver, inserir 0): '))
                
    
    df_filtered['odd_real'] = lista_odd_real

    
    
    
    df_melted = df_melted[~df_melted['time'].isin(lista_time_excluir)]
    

    df_filtered_2 = df_melted[df_melted['prob'] > threshold]
    

    # If less than 8 teams, return empty DataFrame
    num_teams = len(df_filtered_2)
    
    if num_teams < 8:
        return pd.DataFrame(), "Not enough teams to recommend bets."
    
    # If more than 20 teams, take the top 20
    if num_teams > 20:
        df_filtered_2 = df_filtered_2.nlargest(20, 'prob')
    
    num_teams = len(df_filtered_2)

    # Generate pairs based on team count

    if 8 <= num_teams <= 15:
        pairs = list(combinations(df_filtered_2.itertuples(index=False, name=None), 2))
    elif 16 <= num_teams <= 20:
        df_filtered_2 = df_filtered_2.sort_values(by='prob', ascending=False).reset_index(drop=True)
        group1, group2 = [], []
        for i in range(num_teams):
            if i % 2 == 0:
                group1.append(df_filtered_2.iloc[i])
            else:
                group2.append(df_filtered_2.iloc[i])
        pairs = list(combinations(group1, 2)) + list(combinations(group2, 2))
    
    
    df_filtered_2['odd_real'] = ''
    
    for index, row in df_filtered_2.iterrows():
        
        team = df_filtered_2.time[index]
        
        if team in df_filtered.time.tolist():
            df_filtered_2['odd_real'][index] = df_filtered[df_filtered.time == team]['odd_real'].tolist()[0]
            
        else:
            odd_real = float(input(f'Odd under2.5 para {team}: '))
            df_filtered_2['odd_real'][index] = odd_real
    

    # Create bets DataFrame
    bets = pd.DataFrame({
        'team1': [p1[0] for p1, p2 in pairs],
        'team2': [p2[0] for p1, p2 in pairs],
        'prob1': [p1[1] for p1, p2 in pairs],
        'prob2': [p2[1] for p1, p2 in pairs],
        'prob_total': [p1[1] * p2[1] for p1, p2 in pairs]
    })    
    
    
    bets['odd_real1'] = ''
    bets['odd_real2'] = ''
    
    for index, row in bets.iterrows():
        
        time1 = bets.team1[index]
        time2 = bets.team2[index]
        
        bets['odd_real1'][index] = df_filtered_2[df_filtered_2.time == time1]['odd_real'].tolist()[0]

        bets['odd_real2'][index] = df_filtered_2[df_filtered_2.time == time2]['odd_real'].tolist()[0]
      
        
    
    bets['odd_real_comb'] = bets['odd_real1'] * bets['odd_real2']
            


    # Calculate % stake
    mean_prob_total = bets['prob_total'].mean()
    mean_odd_real = bets['odd_real_comb'].mean()
    
    
    bets['stake_percent'] = (1 / len(pairs)) * ((bets['prob_total'] / mean_prob_total) * 
                                                (bets['odd_real_comb'] / mean_odd_real))
    
    bets.to_pickle(f'bets_{opcao}_{inicio}.pkl')
    
    return bets