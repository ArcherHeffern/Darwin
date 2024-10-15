from datetime import timedelta
from dotenv import dotenv_values
from os import environ

ms = "MOODLE_SESSION"
cid = "COURSE_ID"
gap = "GOOGLE_APP_PASSWORD"
em = "GMAIL"

env = dotenv_values()

if env[ms] is None or env[cid] is None or env[gap] is None or env[em] is None:
    raise Exception("Config error")

__LOCAL_WEB_HOST = "127.0.0.1:3000"
__DEPLOYED_WEB_HOST = "172.20.129.207:3000"

if environ.get("DEBUG"):
    _web_host = __LOCAL_WEB_HOST
else:
    _web_host = __DEPLOYED_WEB_HOST

class Config:
    PROGRAM_NAME = "Darwin"
    DB_DATA = True
    ACCOUNT_CREATE_TOKEN_EXPR_TIME: timedelta = timedelta(minutes=15)
    AUTH_TOKEN_EXPIRATION: timedelta = timedelta(days=30)

    WEB_HOST = _web_host

    VERIFY_EMAIL_URL = WEB_HOST + "/signup/verify"

    # ============
    # Gmail
    # ============
    GMAIL_HOST: str = "smtp.gmail.com"
    GMAIL_PORT: int = 587
    GMAIL_ACCOUNT: str = env[em]  # type: ignore
    # Create via https://support.google.com/accounts/answer/185833?visit_id=638643888300995887-1529178198&p=InvalidSecondFactor&rd=1
    GOOGLE_APP_PASSWORD: str = env[gap]  # type: ignore

    # Testing
    MOODLE_SESSION: str = env[ms]  # type: ignore
    COURSE_ID: str = env[cid]  # type: ignore
