import pandas as pd
import streamlit as st

dic_odd1 = {}

dic_odd1['0-0'] = int(st.number('0x0:'))
dic_odd1['1-0'] = int(st.number('1x0:'))
dic_odd1['0-1'] = int(st.number('0x1:'))
dic_odd1['1-1'] = int(st.number('1x1:'))
dic_odd1['2-0'] = int(st.number('2x0:'))
dic_odd1['0-2'] = int(st.number('0x2:'))
dic_odd1['2-1'] = int(st.number('2x1:'))
dic_odd1['1-2'] = int(st.number('1x2:'))
dic_odd1['2-2'] = int(st.number('2x2:'))


dic_prob1 = {}
prob1 = 0
for o in dic_odd1:
    dic_prob1[o] = 1/dic_odd1[o]
    prob1 += dic_prob1[o]
    



dic_odd2 = {}

dic_odd2['0-0'] = int(st.number('0x0:'))
dic_odd2['1-0'] = int(st.number('1x0:'))
dic_odd2['0-1'] = int(st.number('0x1:'))
dic_odd2['1-1'] = int(st.number('1x1:'))
dic_odd2['2-0'] = int(st.number('2x0:'))
dic_odd2['0-2'] = int(st.number('0x2:'))
dic_odd2['2-1'] = int(st.number('2x1:'))
dic_odd2['1-2'] = int(st.number('1x2:'))
dic_odd2['2-2'] = int(st.number('2x2:'))


dic_prob2 = {}
prob2 = 0
for o in dic_odd2:
    dic_prob2[o] = 1/dic_odd2[o]
    prob2 += dic_prob2[o]



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

print(df_bet)
print(retorno)
