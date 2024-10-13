from ast import Delete
from typing import Optional
from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import (
    AccountCreateToken as M_AccountCreateToken,
    AccountCreateTokenId,
)
from darwin.backend.schemas import AccountCreateToken as S_AccountCreateToken


class AccountCreateTokenDal(Dal_I):
    def create(self, account_create_token: M_AccountCreateToken):
        with self.db_session() as db:
            db_account_create_token = S_AccountCreateToken(
                id=account_create_token.id,
                email=account_create_token.email,
                expiration=account_create_token.expiration,
            )
            db.add(db_account_create_token)

    def get(
        self, account_create_token_id: AccountCreateTokenId
    ) -> Optional[M_AccountCreateToken]:
        with self.db_session() as db:
            maybe_account_create_token = db.get(
                S_AccountCreateToken, account_create_token_id
            )
            if maybe_account_create_token is None:
                return None
            return M_AccountCreateToken.model_validate(maybe_account_create_token)

    def delete_all(self, email: str):
        with self.db_session() as db:
            db.query(S_AccountCreateToken).filter_by(email=email).delete()
