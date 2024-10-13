import bcrypt
from darwin.models.backend_models import (
    Account as BE_Account,
    AccountPermission,
    AccountStatus,
    AccountId,
)
from darwin.models.midtier_models import Account as MT_Account, AccountCreateP2
from uuid import uuid4
from bcrypt import hashpw, gensalt

"""
AccountCreateP2_2_BE should be the only path from a MT to a BE account model. This is to ensure the password is always hashed
"""


def BE_2_MT(account: BE_Account) -> MT_Account:
    return MT_Account(
        id=account.id,
        email=account.email,
        name=account.name,
        status=account.status,
        permission=account.permission,
    )


def AccountCreateP2_2_BE(email: str, account_create: AccountCreateP2) -> BE_Account:
    return BE_Account(
        id=AccountId(str(uuid4())),
        email=email,
        name=account_create.name,
        hashed_password=hashpw(account_create.password.encode(), gensalt()).decode(),
        status=AccountStatus.REGISTERED,
        permission=AccountPermission.MEMBER,
    )
