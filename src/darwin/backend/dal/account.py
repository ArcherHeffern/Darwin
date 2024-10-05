from sqlite3 import Connection
from typing import Optional
from src.darwin.models.backend_models import Account, AccountStatus, StorageException


class AccountDal:
    def __init__(self, c: Connection):
        self.c: Connection = c

    def get_account(self, account_id: int) -> Optional[Account]:
        c = self.c
        try:
            with c:
                account = c.execute(
                    """
                    --sql
                    SELECT * FROM account WHERE id==?;
                    """,
                    (str(account_id)),
                ).fetchone()
                print(account)

        except Exception as e:
            raise StorageException(
                f"Failed to get account of account_id {account_id}: {e}"
            )

    def create_account(self, account: Account):
        """
        Creates account or raises StorageException
        """
        c = self.c
        try:
            with c:
                c.execute(
                    """
                    --sql
                    INSERT INTO account (id, name, email, password, status_f, permission_f) VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (
                        account.id,
                        account.name,
                        account.email,
                        account.password,
                        account.status.value,
                        account.permission.value
                    ),
                )
            return account
        except Exception as e:
            raise StorageException(f"Failed to create account for {account.name}: {e}")
