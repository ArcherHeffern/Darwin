from typing import Optional
from darwin.backend.dal.dal_I import Dal_I
from darwin.models.backend_models import AccountId, Account as M_Account
from darwin.backend.schemas import Account as S_Account
from sqlalchemy.orm.session import Session


class AccountDal(Dal_I):
    def get(self, account_id: AccountId) -> M_Account:
        with self.db_session() as db:
            db_account = db.query(S_Account).filter(S_Account.id == account_id).one()
            return M_Account.model_validate(db_account)

    def get_all(self) -> list[M_Account]:
        with self.db_session() as db:
            db_accounts = db.query(S_Account).all()
            return [M_Account.model_validate(db_account) for db_account in db_accounts]

    def create(self, account: M_Account):
        db_account = S_Account(
            id=account.id,
            email=account.email,
            name=account.name,
            hashed_password=account.hashed_password,
            status=account.status,
            permission=account.permission,
        )
        with self.db_session() as db:
            db.add(db_account)
            db.commit()
            db.refresh(db_account)
