from pathlib import Path
from models.backend_models import Account, AccountId, AccountStatus

from storage.sqlite.dal import SQLiteStorage


if __name__ == "__main__":
    service = SQLiteStorage.connect(Path("./db"))
    account = Account(
        AccountId(1), "tim", "tim@gmail.com", "123", AccountStatus.UNREGISTERED
    )
    service.account_dal.create_account(account)
    service.account_dal.get_account(AccountId(1))
