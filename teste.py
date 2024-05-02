import pandas as pd
import streamlit as st

col1, col2 = st.columns(2)

dic_odd1 = {}
with col1:

    st.header('Jogo 1')

    pos_fora1 = st.number_input('Posição Equipe Casa 1',min_value=1,max_value=30,value=1)
    pos_fora2 = st.number_input('Posição Equipe Fora 1',min_value=1,max_value=30,value=1)
    rodada1 = st.number_input('Rodada Jogo 1',min_value=1,max_value=46,value=1)
    
    
    dic_odd1['0-0'] = st.number_input(' Jogo 1 - 0x0:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd1['1-0'] = st.number_input(' Jogo 1 - 1x0:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd1['0-1'] = st.number_input(' Jogo 1 - 0x1:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd1['1-1'] = st.number_input(' Jogo 1 - 1x1:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd1['2-0'] = st.number_input(' Jogo 1 - 2x0:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd1['0-2'] = st.number_input(' Jogo 1 - 0x2:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd1['2-1'] = st.number_input(' Jogo 1 - 2x1:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd1['1-2'] = st.number_input(' Jogo 1 - 1x2:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd1['2-2'] = st.number_input(' Jogo 1 - 2x2:',min_value=1.0,max_value=1000.0,value=1.0)

dic_odd2 = {}
with col2:

    st.header('Jogo 2')

    pos_casa2 = st.number_input('Posição Equipe Casa 2',min_value=1,max_value=30,value=1)
    pos_fora2 = st.number_input('Posição Equipe Fora 2',min_value=1,max_value=30,value=1)
    rodada2 = st.number_input('Rodada Jogo 2',min_value=1,max_value=46,value=1)
    
    dic_odd2['0-0'] = st.number_input(' Jogo 2 - 0x0:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd2['1-0'] = st.number_input(' Jogo 2 - 1x0:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd2['0-1'] = st.number_input(' Jogo 2 - 0x1:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd2['1-1'] = st.number_input(' Jogo 2 - 1x1:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd2['2-0'] = st.number_input(' Jogo 2 - 2x0:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd2['0-2'] = st.number_input(' Jogo 2 - 0x2:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd2['2-1'] = st.number_input(' Jogo 2 - 2x1:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd2['1-2'] = st.number_input(' Jogo 2 - 1x2:',min_value=1.0,max_value=1000.0,value=1.0)
    dic_odd2['2-2'] = st.number_input(' Jogo 2 - 2x2:',min_value=1.0,max_value=1000.0,value=1.0)  


def dic_prob(dic_odd):
    dic_prob = {}
    prob = 0
    for o in dic_odd:
        dic_prob[o] = 1/dic_odd[o]
        prob += dic_prob[o]
    return dic_prob, prob

dic_prob1, prob1 = dic_prob(dic_odd1)    
dic_prob2, prob2 = dic_prob(dic_odd2)



def calculo(dic_odd1,dic_odd2,prob1,prob2):

    somaprod = prob1 * prob2
    total = 1000
        
    df_bet = pd.DataFrame()   
    
    for o in dic_odd1:
        
        lista_coluna = []
        
        for od in dic_odd2:
            
            val = round(total * (1/(dic_odd1[o] * dic_odd2[od])) / somaprod,2)
            
            lista_coluna.append(val)
            
        df_bet[str(o)] = lista_coluna
    
        
    while df_bet.min().min() > .76:
        
        df_bet = pd.DataFrame()   
    
        for o in dic_odd1:
            
            lista_coluna = []
            
            for od in dic_odd2:
                
                val = round(total * (1/(dic_odd1[o] * dic_odd2[od])) / somaprod,2)
                
                lista_coluna.append(val)
                
            df_bet[str(o)] = lista_coluna
            
        total = total - 0.5

    df_bet.index = df_bet.columns.tolist()
    
    retorno = (df_bet.iloc[0,0] * dic_odd1['0-0'] * dic_odd2['0-0'] - total) / total
    return df_bet, retorno, total

if st.button('Calcular Valores'):
    df_bet, retorno, total = calculo(dic_odd1,dic_odd2,prob1,prob2)
    st.dataframe(df_bet)
    st.text(retorno)
    st.text(total)
