import smtplib
import os
from email.mime.text import MIMEText
import json

#configs
cwd = os.getcwd()
config_path = os.path.join(cwd , "config.json")
if os.path.isfile(config_path):
    with open(config_path, "r") as f:
        configurations = f.read()
        f.close()
    configurations = json.loads(configurations)
    smtp_hostname = configurations["smtp_hostname"]
    smtp_port = configurations["smtp_port"]
    smtp_username = configurations["smtp_username"]
    sender_email = configurations["sender_email"]
    sender_pass = configurations["sender_pass"]

    subject_notif = configurations["subject_notif"]
    message_notif = configurations["message_notif"]
    subject_walled = configurations["subject_walled"]
    message_walled = configurations["message_walled"]
else:
    smtp_hostname = ""
    smtp_port = 123456789
    smtp_username = ""
    sender_email = "" 
    sender_pass = ""

    subject_notif = "Click on shortened link"
    message_notif = "Someone clicked on your link `shortened` which redirects to `og_url`"
    subject_walled = "Walled Garden Entry"
    message_walled = "If you tried to access the short link `shortened`, here is its orignal url `og_url`"

def send(notification_email , og_url , shortened , purpose):

    match purpose:
        case "notify":
            subject = subject_notif
            message = message_notif
        case "walled":
            subject = subject_walled
            message = message_walled
        case _:
            print("INVALID PURPOSE TYPE. Must be either walled or notify")

    message = message.replace("`og_url`" , og_url).replace("`shortened`" , shortened)
    print("SENT MAIL")

    message = MIMEText(message)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = notification_email

    with smtplib.SMTP(smtp_hostname, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, sender_pass)
        server.sendmail(sender_email, notification_email, message.as_string())