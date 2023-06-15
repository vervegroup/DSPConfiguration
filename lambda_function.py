import json
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

def get_data(id,secret): 
    # Define the request headers and data
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"client_secret":secret, "client_id":id, "grant_type": "client_credentials"}

    # Send the POST request
    response = requests.post("https://auth-test.smaatolabs.net/v2/auth/token/", headers=headers, data=data)

    # Print the response content (access token)
    print(response.content)
    Response = json.loads(response.content.decode("utf-8"))
    token=Response["access_token"]
    print(token)

    API_TOKEN = token
    HEADERS = {"Content-Type": "application/json",
            "Authorization": "Bearer " + API_TOKEN}

    r = requests.get('https://sdx-api-test.smaatolabs.net/demand-partners/?expand=endpoints', headers=HEADERS)
    response = json.loads(r.content.decode("utf-8"))
    print("successfully fetched data")
    return response

def fill_table(account,table):
     for key in account:
            if key=="id":
                table["Id"].append(account[key])
            if key=="name":
                table["Name"].append(account[key])
            if key=="status":
                table["Status"].append(account[key])

def send_email(table,recipient):
    # converting dictionary into dataframe
    new= pd.DataFrame(table)
    # Save dataframe to CSV file
    new.to_csv('/tmp/DSPConfiguration.csv', index=False) 
    # Email parameters
    sender_email ="no-reply@smaato.com"
    # recipient_email = "musab.mehadi@smaato.com"
    password ="d634767129504136f15eb2b89ea0bca5"  
    # Create message object
    msg = MIMEMultipart()
    email_body = 'Please find attached the current account configurations of Smaato active demand partners from SDX Admin.'
    message= f"Hello,\n{email_body}\n\nBest,\nSE team."
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "DSP Configurations Table" 
    msg.attach(MIMEText(message, 'plain'))
    # Open CSV file in binary mode and add as attachment
    with open("/tmp/DSPConfiguration.csv", "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment", filename="DSP Configuration.csv")
        msg.attach(part)  
    # Create SMTP session and login
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_session = smtplib.SMTP(smtp_server, smtp_port)
    smtp_session.starttls()
    email_user = sender_email
    email_password =password
    smtp_session.login(email_user, email_password) 
    # Send email and check if successful
    sendmail_status = smtp_session.sendmail(sender_email, recipient, msg.as_string())
    if not sendmail_status:
        print("Email sent successfully")
    else:
        print("Email could not be sent to:", sendmail_status) 
    # Terminate SMTP session and delete CSV file
    smtp_session.quit()
    os.remove("/tmp/DSPConfiguration.csv")
    

def lambda_handler(event, context):
    # Fill in your client ID and client secret below
    client_id = "ChVPFjESF7SMaIXpppT7qXHdxm7e0rALC5EqHHK1"
    client_secret = "JqznrTQ8MbRAldZKqUjl3AstSrhi8L2fmozSZ9r8vCm2u8Lbah66mmKJqRy7b7Jrwbzg8VSE7nH19NiDOf9mnx6xeF9UoHbSTgzGIXv6dt7U8RKl44lxjq25CR1v9J8L"
    data=get_data(client_id, client_secret)
    table={"Name":[],'Id':[],"Status":[]}
    
    for account in data:
        fill_table(account,table)
    send_email(table,"musab.mehadi@smaato.com")