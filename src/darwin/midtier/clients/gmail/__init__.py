from darwin.config import Config
from email.message import EmailMessage
from smtplib import SMTP


class __Gmail:
    def __init__(self):
        self.s = SMTP(Config.GMAIL_HOST, Config.GMAIL_PORT)
        self.s.starttls()
        self.s.login(Config.GMAIL_ACCOUNT, Config.GOOGLE_APP_PASSWORD)

    def send(self, recipient: str, subject: str, body: str):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["To"] = recipient
        msg.set_content(body)
        self.s.send_message(msg)

    def close(self):
        self.s.quit()


Gmail = __Gmail()
