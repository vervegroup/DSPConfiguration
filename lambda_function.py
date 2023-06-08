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
    response = requests.post("https://auth.smaato.com/v2/auth/token/", headers=headers, data=data)

    # Print the response content (access token)
    print(response.content)
    Response = json.loads(response.content.decode("utf-8"))
    token=Response["access_token"]
    print(token)

    API_TOKEN = token
    HEADERS = {"Content-Type": "application/json",
            "Authorization": "Bearer " + API_TOKEN}

    r = requests.get('https://sdx-api-internal.smaato.net/demand-partners/?expand=endpoints', headers=HEADERS)
    response = json.loads(r.content.decode("utf-8"))
    return response

def fill_table(account,table):
     for key in account:
            if key=="id":
                table["Id"].append(account[key])
            if key=="demand_supported_maximum_timeout":
                table["Demand Supported Timeout"].append(account[key])
            if key=="dsp":                   
                    table["Multi Ad Format"].append(account[key]["multi_ad_format"])
                    table["Multi Ad Sizes"].append(account[key]["multi_ad_sizes"])
                    table["Multiple Seat Bids Enabled"].append(account[key]["multiple_seat_bids_enabled"])
                    table["Native Version"].append(account[key]["native_version"])
                    table["N2D"].append(account[key]["native2display_enabled"])
                    table["D2N"].append(account[key]["display2native_enabled"])
                    table["Open Measurement"].append(account[key]["open_measurement_enabled"])
                    table["ORTB Version"].append(account[key]["open_rtb_version"])
                    table["Bid Loss Notification"].append(account[key]["send_bidloss_notification"])
                    table["Floor Price"].append(account[key]["send_floor_price"])
                    table["Impression Measurement"].append(account[key]["impression_measurement"])
                    string=""
                    for element in account[key]["supported_metric_objects"]:
                        if element==account[key]["supported_metric_objects"][0]:
                            string= element
                        else:
                            string= element +','+ string   
                    table["Supported Metric Objects"].append(string)

                    string=""
                    for element in account[key]["supported_mime_types"]:
                        if element==account[key]["supported_mime_types"][0]:
                            string= element
                        else:
                            string= element +','+ string   
                    table["Supported Mime Types"].append(string)

                    string=""
                    for element in account[key]["supported_user_id_solutions"]:
                        if element==account[key]["supported_user_id_solutions"][0]:
                            string= element
                        else:
                            string= element +','+ string   
                    table["Supported User Id Solutions"].append(string)  
            if key=="iab_eu_vendor_id":
                table["IAB EU Vendor Id"].append(account[key])
            if key=="kpi_reporting_email":
                table["KPI Reporting Email"].append(account[key])
            if key=="legal_relationship_emea":
                table["Legal Relationship"].append(account[key])
            if key=="loose_data_use_contract":
                table["Loose Data Use Contract"].append(account[key])
            if key=="binary_consent":
                table["Binary Consent"].append(account[key])
            if key=="gpp":
                table["GPP"].append(account[key])
            if key=="max_ad_response_size":
                table["Max Ad Response Size"].append(account[key])
            if key=="name":
                table["Name"].append(account[key])
            if key=="official_name":
                table["Official Name"].append(account[key])
            if key=="reporting_email":
                table["Reporting Email"].append(account[key])
            if key=="sales_office":
                table["Sales Office"].append(account[key])
            if key=="status":
                table["Status"].append(account[key])
            if key=="supply_chain_enabled":
                table["SChain"].append(account[key])

def send_email(table,recipient):
    # converting dictionary into dataframe
    new= pd.DataFrame(table)
    # Save dataframe to CSV file
    new.to_csv('/tmp/DSP Configuration.csv', index=False) 
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
    with open("/tmp/DSP Configuration.csv", "rb") as attachment:
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
    os.remove("/tmp/DSP.csv")
    

def lambda_handler(event, context):
    # Fill in your client ID and client secret below
    client_id = "DjzEhbdFj7XqNLXrM7H25yOv8lQ7jOjteQOQXkDR"
    client_secret = "5apJBV6VJLyXbDCUQZ4EuJzzGNXFYkgkbPPNQXVCNj1fQZJsDTDjJr9M7p3h8H9UApfqv08hNxvxTck7dY39Y18Y2HNgzyPj7i7zPwmw3A4gkztraes6ZOnkYpIxN7iE"
    data=get_data(client_id, client_secret)
    table={"Name":[],'id':[],
     'DemandSupportedTimeout':[],
      'MultiAdFormat':[],'MultiAdSizes':[],"MultipleSeatBidsEnabled":[],"NativeVersion":[],"N2D":[],"D2N":[],"OpenMeasurement":[],
      "ORTBVersion":[],"BidLossNotification":[],"FloorPrice":[],"SupportedMetricObjects":[],"SupportedUserIdSolutions":[],"SupportedMimeTypes":[],"ImpressionMeasurement":[],"iabEUvendorId":[],"kpiReportingEmail":[],
      "LegalRelationship":[],"LooseDataUseContract":[],"BinaryConsent":[],"GPP":[],"MaxAdResponseize":[],
      "OfficialName":[],"ReportingEmail":[], "SalesOffice":[],"Status":[],"SChain":[]}
    
    for account in data:
        if account["dsp"]!= None:
            fill_table(account,table)
    send_email(table,"musab.mehadi@smaato.com")