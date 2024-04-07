import smtplib
from sk import *
import re



sender_id = Email
password = Password

# Function to preprocess spoken email
def preprocess_spoken_email(spoken_email):
   
    spoken_email = spoken_email.replace(" ", "")
    spoken_email = spoken_email.replace("attherate", "@")
    spoken_email = spoken_email.replace("underscore", "_")
    return spoken_email

def send_email(reciever_id, subject, body):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(sender_id, password)
    # message to be sent
    message = "\r\n".join([
        f"From: {sender_id}",
        f"To: {reciever_id}",
        f"Subject: {subject}",
        "",
        f"{body}"
    ])
    # sending the mail
    try:
        s.sendmail(sender_id, reciever_id, message)
    except smtplib.SMTPRecipientsRefused:
        print("INVALID EMAIL ADDRESS")
        return False
    except smtplib.SMTPException:
        return False
    # terminating the session
    s.quit()
    return True

def check_email(email):
    verifier = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(verifier, email):
        return True
    else:
        return False