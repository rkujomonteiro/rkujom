import pandas as pd
import streamlit as st

st.header('Jogo 1')

dic_odd1 = {}

dic_odd1['0-0'] = st.number_input(' Jogo 1 - 0x0:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd1['1-0'] = st.number_input(' Jogo 1 - 1x0:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd1['0-1'] = st.number_input(' Jogo 1 - 0x1:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd1['1-1'] = st.number_input(' Jogo 1 - 1x1:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd1['2-0'] = st.number_input(' Jogo 1 - 2x0:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd1['0-2'] = st.number_input(' Jogo 1 - 0x2:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd1['2-1'] = st.number_input(' Jogo 1 - 2x1:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd1['1-2'] = st.number_input(' Jogo 1 - 1x2:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd1['2-2'] = st.number_input(' Jogo 1 - 2x2:',min_value=1.0,max_value=1000.0,value=1.0)

def dic_prob(dic_odd):
    dic_prob = {}
    prob = 0
    for o in dic_odd:
        dic_prob[o] = 1/dic_odd[o]
        prob += dic_prob[o]
    return dic_prob, prob


dic_prob1, prob1 = dic_prob(dic_odd1)    


st.header('Jogo 2')

dic_odd2 = {}

dic_odd2['0-0'] = st.number_input(' Jogo 2 - 0x0:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd2['1-0'] = st.number_input(' Jogo 2 - 1x0:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd2['0-1'] = st.number_input(' Jogo 2 - 0x1:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd2['1-1'] = st.number_input(' Jogo 2 - 1x1:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd2['2-0'] = st.number_input(' Jogo 2 - 2x0:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd2['0-2'] = st.number_input(' Jogo 2 - 0x2:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd2['2-1'] = st.number_input(' Jogo 2 - 2x1:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd2['1-2'] = st.number_input(' Jogo 2 - 1x2:',min_value=1.0,max_value=1000.0,value=1.0)
dic_odd2['2-2'] = st.number_input(' Jogo 2 - 2x2:',min_value=1.0,max_value=1000.0,value=1.0)


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
    
    retorno = (df_bet.iloc[0,0] * dic_odd1['0-0'] * dic_odd2['0-0'] - total) / total
    return df_bet, retorno


df_bet, retorno = calculo(dic_odd1,dic_odd2,prob1,prob2)

st.dataframe(df_bet)
st.text(retorno)
