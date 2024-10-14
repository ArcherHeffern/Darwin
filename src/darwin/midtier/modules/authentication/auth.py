from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from darwin.backend import Backend
from fastapi.security import OAuth2PasswordBearer
from darwin.models.backend_models import AccountStatus, AuthTokenId
from darwin.models.midtier_models import Account, AccountStatus, AuthTokenId
from darwin.midtier.services.account import AccountService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account/login")
token_dal = Backend.auth_token_dal
account_dal = Backend.account_dal


def get_auth_level(
    token: Annotated[AuthTokenId, Depends(oauth2_scheme)]
) -> Optional[Account]:
    """
    Returns None if no token was provided
    Returns Account if all validations pass
    Raises HTTPException on all other paths
    """
    if token is None:
        return None
    BE_token = token_dal.get(token)
    if BE_token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No such auth token")
    if BE_token.expired():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Auth token expired")
    account = AccountService.get_by_id(BE_token.account_f)
    if not account:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Account for token does not exist: How did we get here?",
        )
    if account.status != AccountStatus.REGISTERED:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Account is not active")
    return account


# Will have to check if the user actually owns a resource within the function calls
