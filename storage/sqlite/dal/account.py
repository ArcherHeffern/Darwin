from sqlite3 import Connection
from typing import Optional
from models.backend_models import Account, StorageException


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
                maybe_status_f: Optional[tuple[int]] = c.execute(
                    """
                --sql
                SELECT (id) from account_status WHERE name==?;
                """,
                    (account.status.name,),
                ).fetchone()

                if maybe_status_f is None:
                    raise StorageException(
                        f"account_status enum not found for {account.status.name}"
                    )
                status_f = maybe_status_f[0]
                c.execute(
                    """
                    --sql
                    INSERT INTO account (id, name, email, password, status_f) VALUES (?, ?, ?, ?, ?);
                    """,
                    (
                        account.id,
                        account.name,
                        account.email,
                        account.password,
                        status_f,
                    ),
                )
            return account
        except Exception as e:
            raise StorageException(f"Failed to create account for {account.name}: {e}")
