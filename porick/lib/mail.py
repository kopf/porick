import smtplib
from email.mime.text import MIMEText

from pylons import config


reset_password_text = """
Hi,

A password reset has been requested for your account on Porick.

To reset your password, please click the link below. 

http://{server_domain}/reset_password?key={key}

This URL will be valid for 2 hours.

If you did not initiate this password reset then you may simply disregard this email.

Cheers,
Porick

"""


def send_reset_password_email(user_email, key):
    s = smtplib.SMTP(config['smtp_server'])
    s.sendmail(
        config['SMTP_REPLYTO'], [user_email],
        MIMEText(reset_password_text.format(server_domain=config['SERVER_DOMAIN'], key=key)).as_string()
    )
    s.quit()