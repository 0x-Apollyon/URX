import os
import json

#CONFIG
cwd = os.getcwd()
config_path = os.path.join(cwd , "config.json")
if os.path.isfile(config_path):
    with open(config_path , "r") as f:
        configurations = f.read()
        f.close()
    configurations = json.loads(configurations)
    email_method = configurations["email_method"]
else:
    email_method = "smtp"
#Methods --> SMTP, Mailtrap-API , Sendgrid-API , Mailersend-API , Mailgun-API
def notify(notification_email, og_url , shortened , purpose):
    match email_method.lower():
        case "smtp":
            import in_house.email_handlers.smtp as mailer
        case "mailtrap_api" | "mailtrapapi" | "mailtrap":
            import in_house.email_handlers.mailtrap_api as mailer
        case "mailersend_api" | "mailersendapi" | "mailersend":
            import in_house.email_handlers.mailersend_api as mailer
        case "mailgun_api" | "mailgunapi" | "mailgun":
            import in_house.email_handlers.mailgun_api as mailer
        case _:
            print("VALID EMAIL NOTIFICATION SERVICE NOT SELECTED")

    try:
        mailer.send(notification_email , og_url , shortened , purpose)
    except:
        print("Error while sending mail")
        
