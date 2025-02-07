# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:55:46 2025

@author: RafaelKujo
"""


def gerar_proxs_intervalo(opcao, inicio, df_proxs):


    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from datetime import datetime, timedelta
    
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
    
    
    
    
    lista_dias = []
    
    driver = webdriver.Chrome(options=chrome_options)
    
    for index, row in df_proxs.iterrows():
        
        link = df_proxs.link[index]
        
        pagina = link + '#1X2/2'
        driver.get(pagina)
    
        try:
            # Wait until the element is present, up to 10 seconds
            dia = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-gray-dark font-main item-center flex gap-1 text-xs font-normal')]"))
            )
            data = dia.text
        except:
            # If the element is not found within 10 seconds, get the latest date
            data = lista_dias[index-1]
    
        print(link + data)
        lista_dias.append(data)
        
        
    driver.quit()
        
        
    df_proxs['data'] = lista_dias
        
    
    
    month_translation = {
        'Jan': 'Jan', 'Fev': 'Feb', 'Mar': 'Mar', 'Abr': 'Apr', 'Mai': 'May', 'Jun': 'Jun',
        'Jul': 'Jul', 'Ago': 'Aug', 'Set': 'Sep', 'Out': 'Oct', 'Nov': 'Nov', 'Dez': 'Dec'
    }
    
    
    
    def parse_date(date_str):
        # Remove the unnecessary part ("Hoje," or other day names)
        
        date_str = date_str.split(',\n')[1]
    
    # Replace Portuguese month abbreviation with English
        for pt_month, en_month in month_translation.items():
            date_str = date_str.replace(pt_month, en_month)
        
        # Parse the string into a datetime object
        return datetime.strptime(date_str, '%d %b %Y')
    
    
    df_proxs['data'] = df_proxs['data'].apply(parse_date)
    
    
    
    weekend_days = [4, 5, 6, 0]  # Friday to Monday (0 = Monday)
    midweek_days = [1, 2, 3]  # Tuesday to Thursday
    
    def filter_by_week(df, option):
        today = datetime.today().date()
        df['date_only'] = df['data'].dt.date  # Convert datetime to date
    
        if option == 'fim de semana':
            valid_days = weekend_days
        elif option == 'meio de semana':
            valid_days = midweek_days
        else:
            raise ValueError("Invalid option. Choose 'fim de semana' or 'meio de semana'.")
    
        # Filter by selected days
        df_filtered = df[df['data'].dt.weekday.isin(valid_days)]
        
        # Get the minimum valid date in the future
        future_dates = df_filtered[df_filtered['date_only'] >= today]
    
        if future_dates.empty:
            return df_filtered.iloc[:0]  # Return empty DataFrame if no future dates
    
        next_valid_date = future_dates['date_only'].min()  # Get first available day
    
        # Determine the end of the period (Monday for weekend, Thursday for midweek)
        if option == 'fim de semana':
            end_date = next_valid_date + timedelta(days=(7 - next_valid_date.weekday()) % 7)
        else:  # 'meio de semana'
            end_date = next_valid_date + timedelta(days=(3 - next_valid_date.weekday()) % 7)
    
        # Filter all dates within this period
        return df_filtered[(df_filtered['date_only'] >= next_valid_date) & 
                           (df_filtered['date_only'] <= end_date)].drop(columns=['date_only'])
    
    
    
    # Filter the rows based on the option selected
    
    
    df_proxs_intervalo = filter_by_week(df_proxs, opcao)
    
    df_proxs_intervalo.to_pickle(f'proxs_{opcao}_{inicio}_sem_odds.pkl')
    
    
    return df_proxs_intervalo
    