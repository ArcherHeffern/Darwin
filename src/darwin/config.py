from datetime import timedelta
from dotenv import dotenv_values

ms = "MOODLE_SESSION"
cid = "COURSE_ID"
gap = "GOOGLE_APP_PASSWORD"
em = "GMAIL"

env = dotenv_values()

if env[ms] is None or env[cid] is None or env[gap] is None or env[em] is None:
    raise Exception("Config error")


class Config:
    DB_DATA = True
    ACCOUNT_CREATE_TOKEN_EXPR_TIME: timedelta = timedelta(minutes=15)
    WEB_HOST = "127.0.0.1:3000"

    # ============
    # Gmail
    # ============
    GMAIL_HOST: str = 'smtp.gmail.com'
    GMAIL_PORT: int = 587
    GMAIL_ACCOUNT: str = env[em] # type: ignore
    # Create via https://support.google.com/accounts/answer/185833?visit_id=638643888300995887-1529178198&p=InvalidSecondFactor&rd=1
    GOOGLE_APP_PASSWORD: str = env[gap] # type: ignore

    # Testing
    MOODLE_SESSION: str = env[ms]  # type: ignore
    COURSE_ID: str = env[cid] # type: ignore
