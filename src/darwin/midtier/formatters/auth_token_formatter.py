from darwin.models.backend_models import AuthToken as BE_AuthToken
from darwin.models.midtier_models import AuthToken as MT_AuthToken

def BE_2_MT(BE_auth_token: BE_AuthToken) -> MT_AuthToken:
    return MT_AuthToken(auth_token=BE_auth_token.token, expiration=BE_auth_token.expiration)
    