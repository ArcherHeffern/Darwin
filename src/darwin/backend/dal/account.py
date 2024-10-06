from typing import Optional
from darwin.models.backend_models import Account


class AccountDal:
    def get_account(self, account_id: int) -> Optional[Account]:
        ...

    def create_account(self, account: Account):
        ...