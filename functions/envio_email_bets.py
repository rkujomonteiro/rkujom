# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 17:12:38 2025

@author: RafaelKujo
"""

def envio_email_bets(bets, opcao, inicio, receivers):

    
    import smtplib
    from email.message import EmailMessage
    
    
    csv_filename_bets = f'bets_{opcao}_{inicio}.csv'
    
    files = [csv_filename_bets]
    
    
    bets.to_csv(csv_filename_bets, index=False)
    
    
    sender_email = "rkujomonteiro@gmail.com"
    subject = f"Apostas recomendadas para {opcao} com início em {inicio}"
    body = ""
    
    
    
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_password = "ebdh jpqm tnac tbrk"
    
    for email in receivers:
    
        receiver_email = email
        
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.set_content(body)
        
        with open(csv_filename_bets, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="csv", filename=csv_filename_bets)
    
    
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, email_password)
            server.send_message(msg)
            
            print(f'Apostas de {opcao} com início em {inicio} enviadas para {email}.')