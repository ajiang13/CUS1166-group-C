import os

class Config(object):
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    # Edit these to match your environment
    MAIL_USERNAME=os.environ['GROUPC_EMAIL']
    MAIL_PASSWORD=os.environ['GROUPC_EMAIL_PW']
    MAIL_DEFAULT_SENDER=os.environ['GROUPC_EMAIL']
