import pickle
import pandas as pd
import time
import datetime as dt


with open('base_fbref.pkl', 'rb') as f:
    base_fbref = pickle.load(f)


ligas_fbref = {'Serie-A':'24',
               'Premier-League':'9',
               'La-Liga':'12',
               'Serie-A-Ita':'11',
               'Bundesliga':'20',
               'Ligue-1':'13',
               'Primeira-Liga':'32'}




base_aovivo = pd.DataFrame()

for liga in ligas_fbref:
 
    link = 'https://fbref.com/pt/comps/'+ligas_fbref[liga]+'/'+'/cronograma/'+liga+'-Resultados-e-Calendarios'

    base_liga = pd.read_html(link)[0]
    
    base_liga['Liga'] = liga

    base_aovivo = pd.concat([base_aovivo,base_liga])
    
    time.sleep(3)
    
base_aovivo = base_aovivo[pd.isna(base_aovivo.Sem)==False].reset_index(drop=True)  

base_aovivo.Data = pd.to_datetime(base_aovivo.Data)


hoje = dt.datetime.now().date()

passado = base_aovivo[(base_aovivo.Data.dt.date < hoje)&
                      (pd.isna(base_aovivo.Resultado)==False)]


passado['PlacarCasa'] = passado['Resultado'].str[:1].astype(int)
passado['PlacarFora'] = passado['Resultado'].str[-1].astype(int)

futuro = base_aovivo[base_aovivo.Data.dt.date >= hoje]









df_tabelas = pd.DataFrame()
    
for liga in ligas_fbref:
    
    df_liga = passado[passado.Liga == liga]
    
    equipes = pd.unique(df_liga['Em casa'])
        
    df_semana = df_liga[df_liga.Sem <= max(df_liga.Sem)]
    
    lista_equipe = []
    lista_vit = []
    lista_der = []
    lista_emp = []
    lista_gm = []
    lista_gs = []
    
    for equipe in equipes:
        
        df_equipe = df_semana[(df_semana['Em casa']==equipe)|
                              (df_semana['Visitante']==equipe)]
        
        gms = (df_equipe[df_equipe['Em casa']==equipe]['PlacarCasa'].sum()+
               df_equipe[df_equipe['Visitante']==equipe]['PlacarFora'].sum())
        
        gss = (df_equipe[df_equipe['Visitante']==equipe]['PlacarCasa'].sum()+
               df_equipe[df_equipe['Em casa']==equipe]['PlacarFora'].sum())
        
        vs = len(df_equipe[(df_equipe['Em casa']==equipe)&
                         (df_equipe['PlacarCasa'] > df_equipe['PlacarFora'])|
                         (df_equipe['Visitante']==equipe)&
                         (df_equipe['PlacarCasa'] < df_equipe['PlacarFora'])])
        
        ds = len(df_equipe[(df_equipe['Visitante']==equipe)&
                         (df_equipe['PlacarCasa'] > df_equipe['PlacarFora'])|
                         (df_equipe['Em casa']==equipe)&
                         (df_equipe['PlacarCasa'] < df_equipe['PlacarFora'])])
        
        es = len(df_equipe[df_equipe['PlacarCasa'] == df_equipe['PlacarFora']])
        
        lista_equipe.append(equipe)
        lista_vit.append(vs)
        lista_der.append(ds)
        lista_emp.append(es)
        lista_gm.append(gms)
        lista_gs.append(gss)
        
    tabela_sem = pd.DataFrame({'Equipe':lista_equipe,
                               'V':lista_vit,
                               'E':lista_emp,
                               'D':lista_der,
                               'GM':lista_gm,
                               'GS':lista_gs})
    
    tabela_sem['SG'] = tabela_sem.GM - tabela_sem.GS
    tabela_sem['P'] = 3*tabela_sem.V + tabela_sem.E
    tabela_sem['GM/Jogo'] = tabela_sem['GM'] / max(df_liga.Sem)
    tabela_sem['GS/Jogo'] = tabela_sem['GS'] / max(df_liga.Sem)
    tabela_sem['Sem'] = max(df_liga.Sem)
    
    tabela_sem['Liga'] = liga
    
    tabela_sem = tabela_sem.sort_values(by=['P','V','SG'],ascending=[False,False,False])
    
    tabela_sem['Clas'] = range(1,len(tabela_sem)+1)
    
    
    df_tabelas = pd.concat([df_tabelas,tabela_sem])


proxs = pd.DataFrame()

for liga in ligas_fbref:
    df_liga = futuro[futuro.Liga == liga]
    
    df_sem = df_liga[df_liga.Sem == min(pd.unique(df_liga.Sem))]
    
    proxs = pd.concat([proxs,df_sem])

proxs = proxs.reset_index(drop=True)

proxs['PosCasa'] = ''
proxs['PosFora'] = ''

for index, row in proxs.iterrows():
    pos_casa = df_tabelas[df_tabelas.Equipe == proxs['Em casa'][index]]['Clas'].tolist()[0]
    pos_fora = df_tabelas[df_tabelas.Equipe == proxs['Visitante'][index]]['Clas'].tolist()[0]
    
    proxs['PosCasa'][index] = pos_casa
    proxs['PosFora'][index] = pos_fora
    
proxs['DifPos'] = proxs['PosCasa'] - proxs['PosFora']


proxs['Odd2-2'] = ''
proxs['PtsUltsCasa'][index] = ''
proxs['GMsUltsCasa'][index] = ''
proxs['GSsUltsCasa'][index] = ''
proxs['PtsUltsFora'][index] = ''
proxs['GMsUltsFora'][index] = ''
proxs['GSsUltsFora'][index] = ''

rodadas_hist = 5


for index, row in proxs.iterrows():

    posicasa = proxs['PosCasa'][index]
    posifora = proxs['PosFora'][index]
    rodada = int(proxs['Sem'][index])
    liga = proxs['Liga'][index]
    
    lista_odds = []
    
    for int_rodada in range(1,10):
        
        for int_pos in range(1,6):
    
            base_jogo = base_fbref[(base_fbref.PosCasa.isin(range(posicasa-int_pos,posicasa+int_pos)))&
                                   (base_fbref.PosFora.isin(range(posifora-int_pos,posifora+int_pos)))&
                                   (base_fbref.Sem.isin(range(rodada-int_rodada,rodada+int_rodada)))&
                                   (base_fbref.Liga==liga)]
            
            golscasa = base_jogo.PlacarCasa.mean()
            golsfora = base_jogo.PlacarFora.mean()
            
            if len(base_jogo) == 0:
                chance_result = 1
            else:        
                chance_result = len(base_jogo[(base_jogo.PlacarCasa <= 2)&
                                          (base_jogo.PlacarFora <= 2)])/len(base_jogo)
                    
            if chance_result == 0:
                chance_result = 1
            
            odd_justa = 1 / chance_result
            
            lista_odds.append(odd_justa)
    
    odd = sum(lista_odds)/len(lista_odds)
    
    proxs['Odd2-2'][index] = odd
    
    
    
    ult_casa = passado[(passado.Liga == liga)&
                           (passado['Em casa'] == proxs['Em casa'][index])&
                           (passado.Sem.isin(range(rodada-rodadas_hist,rodada)))|
                           (passado.Liga == liga)&
                           (passado['Visitante'] == proxs['Em casa'][index])&
                           (passado.Sem.isin(range(rodada-rodadas_hist,rodada)))]
    
    ult_fora = passado[(passado.Liga == liga)&
                           (passado['Em casa'] == proxs['Visitante'][index])&
                           (passado.Sem.isin(range(rodada-rodadas_hist,rodada)))|
                           (passado.Liga == liga)&
                           (passado['Visitante'] == proxs['Visitante'][index])&
                           (passado.Sem.isin(range(rodada-rodadas_hist,rodada)))]
    
    ## estatisticas casa
    
    gms_casa = (ult_casa[ult_casa['Em casa']==proxs['Em casa'][index]]['PlacarCasa'].sum()
                +
                ult_casa[ult_casa['Visitante']==proxs['Em casa'][index]]['PlacarFora'].sum()) / len(ult_casa)
    
    gss_casa = (ult_casa[ult_casa['Em casa']==proxs['Em casa'][index]]['PlacarFora'].sum()
                +
                ult_casa[ult_casa['Visitante']==proxs['Em casa'][index]]['PlacarCasa'].sum()) / len(ult_casa)
    
    vs_casa = len(ult_casa[(ult_casa['Em casa'] == proxs['Em casa'][index])&
                           (ult_casa.PlacarCasa > ult_casa.PlacarFora)|
                           (ult_casa['Visitante'] == proxs['Em casa'][index])&
                           (ult_casa.PlacarCasa < ult_casa.PlacarFora)])
    
    es_casa = len(ult_casa[ult_casa.PlacarCasa == ult_casa.PlacarFora])
    
    ds_casa = rodadas_hist - vs_casa - es_casa
    
    ps_casa = vs_casa * 3 + es_casa
    
    
    proxs['PtsUltsCasa'][index] = ps_casa
    proxs['GMsUltsCasa'][index] = gms_casa
    proxs['GSsUltsCasa'][index] = gss_casa   
    
    
    
    
    ## estatisticas fora
    
    gms_fora = (ult_fora[ult_fora['Em casa']==proxs['Visitante'][index]]['PlacarCasa'].sum()
                +
                ult_fora[ult_fora['Visitante']==proxs['Visitante'][index]]['PlacarFora'].sum()) / len(ult_fora)
    
    gss_fora = (ult_fora[ult_fora['Em casa']==proxs['Visitante'][index]]['PlacarFora'].sum()
                +
                ult_fora[ult_fora['Visitante']==proxs['Visitante'][index]]['PlacarCasa'].sum()) / len(ult_fora)
    
    vs_fora = len(ult_fora[(ult_fora['Em casa'] == proxs['Visitante'][index])&
                           (ult_fora.PlacarCasa > ult_fora.PlacarFora)|
                           (ult_fora['Visitante'] == proxs['Visitante'][index])&
                           (ult_fora.PlacarCasa < ult_fora.PlacarFora)])
    
    es_fora = len(ult_fora[ult_fora.PlacarCasa == ult_fora.PlacarFora])
    
    ds_fora = rodadas_hist - vs_fora - es_fora
    
    ps_fora = vs_fora * 3 + es_fora
    
    proxs['PtsUltsFora'][index] = ps_fora
    proxs['GMsUltsFora'][index] = gms_fora
    proxs['GSsUltsFora'][index] = gss_fora
