import requests
import os
import json

####CONFIGS####
cwd = os.getcwd()
config_path = os.path.join(cwd , "config.json")
if os.path.isfile(config_path):
    with open(config_path , "r") as f:
        configurations = f.read()
        f.close()
    configurations = json.loads(configurations)

    sender_email = configurations["sender_email"]
    sender_name = configurations["sender_name"]
    subject_notif = configurations["subject_notif"]
    message_notif = configurations["message_notif"]
    subject_walled = configurations["subject_walled"]
    message_walled = configurations["message_walled"]
    api_key = configurations["api_key"]
    email_domain = configurations["email_domain"]
else:
    sender_email = ''
    sender_name = "URX Shortener"
    subject_notif = "Click on shortened link"
    message_notif = "Someone clicked on your link `shortened` which redirects to `og_url`"
    subject_walled = "Walled Garden Entry"
    message_walled = "If you tried to access the short link `shortened`, here is its orignal url `og_url`"
    api_key = ""
    email_domain = ""
####CONFIGS####

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

    files = [
        ('from', (None, f'{sender_name} <{sender_email}@{email_domain}>')),
        ('to', (None, 'notification_email')),
        ('subject', (None, subject)),
        ('text', (None, message.replace("`og_url`" , og_url).replace("`shortened`" , shortened))),
    ]

    response = requests.post(
        f'https://api.mailgun.net/v3/{email_domain}/messages',
        files=files,
        auth=('api', api_key),
)