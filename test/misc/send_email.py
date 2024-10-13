from darwin.config import Config
from darwin.midtier.clients.gmail import Gmail
import smtplib

"""
https://support.google.com/accounts/answer/185833?visit_id=638643888300995887-1529178198&p=InvalidSecondFactor&rd=1

Must create app password to authenticate with GSMTP
"""
g = Gmail
RECIPIENT = 'xxx@gmail.com'

g.send(RECIPIENT, "TO THIS THING", "WOULD YOU LIKE LOTS OF MUNNY?????")


# s = smtplib.SMTP(Config.GMAIL_HOST, Config.GMAIL_PORT)
# s.starttls()
# s.login(Config.GMAIL_ACCOUNT, Config.GOOGLE_APP_PASSWORD)
# message = f"Verify your email"
# s.sendmail("", RECIPIENT, message)
# s.quit()