'''
Initialize SMTP instance
'''

def connect():
    import smtplib
    import os
    s = smtplib.SMTP(host=os.environ.get("EMAIL_HOST"), port=587) # type: ignore
    s.starttls()
    s.login(user=os.environ.get("SENDER_EMAIL"), password=os.environ.get("SENDER_PASSWORD")) # type: ignore
    return s