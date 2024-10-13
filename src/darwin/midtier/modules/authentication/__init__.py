from typing import Annotated
from fastapi import Depends
from darwin.midtier.modules.authentication.auth import get_auth_level
from darwin.models.midtier_models import Account

ACCOUNT = Annotated[Account, Depends(get_auth_level)]
