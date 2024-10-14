from typing import Optional
from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import AuthToken as M_AuthToken, AuthTokenId, AccountId
from darwin.backend.schemas import AuthToken as S_AuthToken


class AuthTokenDal(Dal_I):
    def create(self, token: M_AuthToken):
        db_auth_token = S_AuthToken(
            token=token.token,
            account_f=token.account_f,
            expiration=token.expiration,
            revoked=token.revoked,
        )
        with self.db_session() as db:
            db.add(db_auth_token)

    def get(self, token: AuthTokenId) -> Optional[M_AuthToken]:
        with self.db_session() as db:
            maybe_auth_token = db.get(S_AuthToken, token)
            if maybe_auth_token is None:
                return None
            return M_AuthToken.model_validate(maybe_auth_token)

    def delete_by_account(self, account_id: AccountId):
        with self.db_session() as db:
            db.query(S_AuthToken).filter_by(account_f=account_id).delete()