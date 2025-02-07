# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:01:23 2025

@author: RafaelKujo
"""


def busca_odds_proxs(df_proxs_intervalo, casa_escolhida):


    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    import time
    from selenium.webdriver.common.by import By
    
    
    chrome_options = Options()
    
    # Emulate a human-like browser:
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disables the automation flag
    chrome_options.add_argument("--start-maximized")  # Start browser maximized
    chrome_options.add_argument("--disable-infobars")  # Disable 'Chrome is being controlled' message
    chrome_options.add_argument("--no-sandbox")  # Avoid using a sandbox
    chrome_options.add_argument("--disable-dev-shm-usage")# Avoid /dev/shm on Chrome in Docker
    chrome_options.add_argument("--headless") 
    
    # Spoof the User-Agent to appear like a real browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36")
    
    
    
    
    df_odds_proxs_jogo = pd.DataFrame()
    df_odds_proxs_bts = pd.DataFrame()
    df_odds_proxs_o35 = pd.DataFrame()
    df_odds_proxs_o45 = pd.DataFrame()
    
    
    for link in df_proxs_intervalo.link:
        
        
        lista_links_jogo = {'odds_jogo': link + '#1X2/2',
                            'odds_bts_jogo': link + '#bts/2'}
                            #'odds_over35_jogo':link + '#over-under;2;3.50;0',
                            #'odds_over45_jogo':link + '#over-under;2;4.50;0'}
        
        
        for item in lista_links_jogo:
            
            pagina = lista_links_jogo[item]
            
            index_key = list(lista_links_jogo.keys()).index(item)
            
            if index_key == 0:
                
                lista_casa_aposta_jogo = []
                
                lista_odd_casa_jogo = []
    
                lista_odd_emp_jogo = []
    
                lista_odd_fora_jogo = []
                
                
                
                driver = webdriver.Chrome(options=chrome_options)
                
                driver.get(pagina)
                
                time.sleep(2)
                
                odds = driver.find_elements(By.XPATH, "//div[contains(@class, 'border-black-borders flex h-9 border-b border-l border-r text-xs')]")
                
    
                lista_odds = []        
                for odd in odds:
                    lista_odds.append(odd.text)
                    
                for lista in lista_odds:
                    
                    if not lista:
                        continue
                    
                    else:                
                        
                        lista_casa_aposta_jogo.append(lista.split('\n')[0])
                        lista_odd_casa_jogo.append(lista.split('\n')[-4])
                        lista_odd_emp_jogo.append(lista.split('\n')[-3])
                        lista_odd_fora_jogo.append(lista.split('\n')[-2])
                        
                        dia = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-gray-dark font-main item-center flex gap-1 text-xs font-normal')]")
                        data = dia[0].text
                        
                
                driver.quit()
                        
                df_odds_win_jogo = pd.DataFrame({'link':link,
                                             'data':data,
                                             
                                             'casa_aposta_jogo':lista_casa_aposta_jogo,
                                             
                                             'odd_casa_jogo':lista_odd_casa_jogo,
    
                                             'odd_emp_jogo':lista_odd_emp_jogo,
    
                                             'odd_fora_jogo':lista_odd_fora_jogo,
                                             
                                             })
                
                df_odds_proxs_jogo = pd.concat([df_odds_proxs_jogo,
                                                df_odds_win_jogo])
                
                print(item+' : '+pagina)
                
                
                
            elif index_key == 1:
                
                lista_casa_aposta_bts = []
                
                lista_odd_bts_sim_jogo = []
    
                lista_odd_bts_nao_jogo = []
                
                
                driver = webdriver.Chrome(options=chrome_options)
                
                driver.get(pagina)
                
                time.sleep(2)
                
                odds = driver.find_elements(By.XPATH, "//div[contains(@class, 'border-black-borders flex h-9 border-b border-l border-r text-xs')]")
                
    
                lista_odds = []        
                for odd in odds:
                    lista_odds.append(odd.text)
                    
                for lista in lista_odds:
                    
                    if not lista:
                        continue
                    
                    else:
                        
                        lista_casa_aposta_bts.append(lista.split('\n')[0])
                        lista_odd_bts_sim_jogo.append(lista.split('\n')[-3])
                        lista_odd_bts_nao_jogo.append(lista.split('\n')[-2])
                        
                        dia = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-gray-dark font-main item-center flex gap-1 text-xs font-normal')]")
                        data = dia[0].text
                 
                        
                 
                driver.quit()
                
                df_odds_bts_jogo = pd.DataFrame({'link':link,
                                             'data':data,
                                             
                                             'casa_aposta_bts':lista_casa_aposta_bts,
                                             
                                             'odd_bts_sim_jogo':lista_odd_bts_sim_jogo,
                                             
                                             'odd_bts_nao_jogo':lista_odd_bts_nao_jogo})
                
                df_odds_proxs_bts = pd.concat([df_odds_proxs_bts,
                                                df_odds_bts_jogo])
                
                print(item+' : '+pagina)
                
                
                
            elif index_key == 2:
                
                lista_casa_aposta_over35 = []
                
                lista_odd_over35_sim_jogo = []
                
                lista_odd_over35_nao_jogo = []
                
                
                driver = webdriver.Chrome(options=chrome_options)
                
                driver.get(pagina)
                
                time.sleep(2)
                
                odds = driver.find_elements(By.XPATH, "//div[contains(@class, 'border-black-borders flex h-9 border-b border-l border-r text-xs')]")
                
    
                lista_odds = []        
                for odd in odds:
                    lista_odds.append(odd.text)
                    
                for lista in lista_odds:
                    
                    if not lista:
                        continue
                    
                    else:
                        
                        lista_casa_aposta_over35.append(lista.split('\n')[0])
                        lista_odd_over35_sim_jogo.append(lista.split('\n')[-3])
                        lista_odd_over35_nao_jogo.append(lista.split('\n')[-2])
                        
                        dia = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-gray-dark font-main item-center flex gap-1 text-xs font-normal')]")
                        data = dia[0].text
                        
                
                driver.quit()
                
                df_odds_over35_jogo = pd.DataFrame({'link':link,
                                             'data':data,
                                             
                                             'casa_aposta_over35':lista_casa_aposta_over35,
                                             
                                             'odd_over35':lista_odd_over35_sim_jogo,
                                             
                                             'odd_under35': lista_odd_over35_nao_jogo})
                
                df_odds_proxs_o35 = pd.concat([df_odds_proxs_o35,
                                                df_odds_over35_jogo])
                
                print(item+' : '+pagina)
                
            
            
            elif index_key == 3:
                
                lista_casa_aposta_over45 = []
                
                lista_odd_over45_sim_jogo = []
                
                lista_odd_over45_nao_jogo = []
                
                
                driver = webdriver.Chrome(options=chrome_options)
                
                driver.get(pagina)
                
                time.sleep(2)
                
                odds = driver.find_elements(By.XPATH, "//div[contains(@class, 'border-black-borders flex h-9 border-b border-l border-r text-xs')]")
                
    
                lista_odds = []        
                for odd in odds:
                    lista_odds.append(odd.text)
                    
                for lista in lista_odds:
                    
                    if not lista:
                        continue
                    
                    else:
                        
                        lista_casa_aposta_over45.append(lista.split('\n')[0])
                        lista_odd_over45_sim_jogo.append(lista.split('\n')[-3])
                        lista_odd_over45_nao_jogo.append(lista.split('\n')[-2])
                        
                        dia = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-gray-dark font-main item-center flex gap-1 text-xs font-normal')]")
                        data = dia[0].text
                        
                
                driver.quit()
                
                df_odds_over45_jogo = pd.DataFrame({'link':link,
                                             'data':data,
                                             
                                             'casa_aposta_over45':lista_casa_aposta_over45,
                                             
                                             'odd_over45':lista_odd_over45_sim_jogo,
                                             
                                             'odd_under45': lista_odd_over45_nao_jogo})
                
                df_odds_proxs_o45 = pd.concat([df_odds_proxs_o45,
                                                df_odds_over45_jogo])
                
                print(item+' : '+pagina)
    
    
    

    '''escolhendo casa de apostas para ver odds dos proxs'''
    
    casas = pd.unique(df_odds_proxs_jogo.casa_aposta_jogo)
    
    while True:
        if casa_escolhida in casas:
            break
        print('Casa não disponível, favor escolher novamente.')
    
    
    '''filtrando as bases de apostas pela casa'''
    
    filtered_win = df_odds_proxs_jogo[df_odds_proxs_jogo.casa_aposta_jogo == casa_escolhida][['link','odd_casa_jogo', 'odd_emp_jogo', 'odd_fora_jogo']]
    filtered_bts = df_odds_proxs_bts[df_odds_proxs_bts.casa_aposta_bts == casa_escolhida][['link', 'odd_bts_sim_jogo', 'odd_bts_nao_jogo']]
    '''filtered_o35 = df_odds_proxs_o35[df_odds_proxs_o35.casa_aposta_over35 == casa_escolhida][['link', 'odd_over35', 'odd_under35']]
    filtered_o45 = df_odds_proxs_o45[df_odds_proxs_o45.casa_aposta_over45 == casa_escolhida][['link','odd_over45', 'odd_under45']]
    '''
    
    
    
    
    '''unindo, por link, com o df_proxs_intervalo'''
    
    df_proxs_intervalo = df_proxs_intervalo.merge(filtered_win, on='link', how='left')
    df_proxs_intervalo = df_proxs_intervalo.merge(filtered_bts, on='link', how='left')
    '''df_proxs_intervalo = df_proxs_intervalo.merge(filtered_o35, on='link', how='left')
    df_proxs_intervalo = df_proxs_intervalo.merge(filtered_o45, on='link', how='left')
    '''
    
    return df_proxs_intervalo