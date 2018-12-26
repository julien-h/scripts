# Sending emails from python.
# Template provided by https://Scripting.Tips
# You may freely reuse, modify and share this piece of code

import emails
import os

SMTP_SERVER   = os.environ['MAIL_NOTIFIER_SMTP']   # 'smtp.mail.yahoo.com'
SMTP_LOGIN    = os.environ['MAIL_NOTIFIER_LOGIN']  # 'linus.t@yahoo.com'
SMTP_PASSWORD = os.environ['MAIL_NOTIFIER_PASS']   # 'mysecretpassword'

SENDER_NAME  = 'Python script'
SENDER_EMAIL = os.environ['MAIL_NOTIFIER_LOGIN']   # 'linus.t@yahoo.com'
RECIPIENT = os.environ['MAIL_NOTIFIER_DST']        # 'james@gmail.com'

def notify(msg, title='Notification', attachment=None):

    message = emails.html(
        subject=title, 
        html=f'<p>{msg}<p>', 
        mail_from=(SENDER_NAME, SENDER_EMAIL)
    )

    if attachment:
        message.attach(data=open(attachment, 'rb'), filename=attachment)

    config = {
        'host': SMTP_SERVER,
        'timeout': 5,
        'ssl': True,
        'user': SMTP_LOGIN,
        'password': SMTP_PASSWORD
    }
             
    r = message.send(to=RECIPIENT, smtp=config)
    return r.success  # r.status_code

