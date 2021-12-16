'''
Initialize SMTP instance
'''

def connect():
    import smtplib
    import os
    s = smtplib.SMTP(host=os.environ.get("EMAIL_HOST"), port=587)
    s.starttls()
    s.login(user=os.environ.get("SENDER_EMAIL"), password=os.environ.get("SENDER_PASSWORD"))
    return s