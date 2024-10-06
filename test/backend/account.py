from unittest import TestCase

from darwin.backend import Backend
from darwin.models.backend_models import Account as M_Account
from darwin.models.backend_models import AccountId, AccountPermission, AccountStatus


class AccountTests(TestCase):
    def test_crud(self):
        account = M_Account(
            id=AccountId(1), 
            name="tim",
            email="tim@gmail.com",
            hashed_password="123",
            status=AccountStatus.UNREGISTERED,
            permission=AccountPermission.ADMIN
        )
        Backend.account_dal.create(account)
        Backend.account_dal.get(AccountId(1))