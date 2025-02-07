# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:46:49 2025

@author: RafaelKujo
"""

def busca_ligas(hoje):

    import time
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import warnings
    
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    global DRIVER_LOCATION
    DRIVER_LOCATION = r"C:\Users\RafaelKujo\Desktop\Scrape Odds\chromedriver.exe"
    
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
    
    
    ligas = {'brazil':'brasileirao-betano',
             'france':'ligue-1',
             'portugal':'liga-portugal',
             'spain':'laliga',
             'germany':'bundesliga',
             'england':'campeonato-ingles',
             'italy':'serie-a'}
    
    
    jogos_ligas = {'brazil': 10,
             'france': 9,
             'portugal': 9,
             'spain': 10,
             'germany': 9,
             'england': 10,
             'italy': 10}
    
    
    
    lista_textos = []
    lista_links = []
    lista_ligas = []
    
    
    
    for liga in ligas:
    
        driver = webdriver.Chrome(options=chrome_options)
        
        link = 'https://www.oddsportal.com/br/football/'+liga+'/'+ligas[liga]
        
        driver.get(link)
        
        time.sleep(3)
        
        linhas = driver.find_elements(By.XPATH, "//a[contains(@class, 'next-m:flex next-m:!mt-0 ml-2 mt-2 min-h-[32px] w-full hover:cursor-pointer')]")
        
        lista_textos_pag = []
        lista_links_pag = []
        lista_ligas_pag = []
        
        for linha in linhas:
    
            lista_textos_pag.append(linha.text)
            
            lista_links_pag.append(linha.get_attribute('href'))
            
            lista_ligas_pag.append(liga)
    
        
        if len(lista_textos_pag) >= 10:
            
            lista_textos_pag = lista_textos_pag[:jogos_ligas[liga]]
            lista_links_pag = lista_links_pag[:jogos_ligas[liga]]
            lista_ligas_pag = lista_ligas_pag[:jogos_ligas[liga]]
            
            
        lista_textos.append(lista_textos_pag)
        lista_links.append(lista_links_pag)
        lista_ligas.append(lista_ligas_pag)
        
        print(liga+' OK')
        
        driver.quit()
    
    
    
    textos = []
    links = []
    ligas_df = []
    
    
    for lista in lista_textos:
        for item in lista:
            
            textos.append(item)
            links.append(lista_links[lista_textos.index(lista)][lista.index(item)])
            ligas_df.append(lista_ligas[lista_textos.index(lista)][lista.index(item)])
    
    
    casas = []
    foras = []        
    
    for item in textos:
        
        casas.append(item.split('\n')[1])
        foras.append(item.split('\n')[-1])
        
        
    
    
    df_proxs = pd.DataFrame({'casa':casas,
                             'fora':foras,
                             'link':links,
                             'liga':ligas_df})
    
    df_proxs.to_pickle(f'todos_proxs_{hoje}.pkl')
    
    return df_proxs

