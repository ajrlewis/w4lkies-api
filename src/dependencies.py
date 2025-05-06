from typing import Annotated

from fastapi import Depends, BackgroundTasks, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from loguru import logger

from config import settings
from cruds import user_crud
from database import SessionLocal
from models import User
from schemas.token_schema import TokenData


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


GetDBDep = Annotated[SessionLocal, Depends(get_db)]


def get_oauth2_form_data(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return form_data


OAuth2FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends(get_oauth2_form_data)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
GetTokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(db: GetDBDep, token: GetTokenDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = user_crud.get_user_by_name(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


GetCurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(current_user: GetCurrentUserDep):
    if current_user.is_active:
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )


GetCurrentActiveUserDep = Annotated[User, Depends(get_current_active_user)]


async def get_current_admin_user(current_user: GetCurrentActiveUserDep):
    if current_user.is_admin:
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )


GetCurrentAdminUserDep = Annotated[User, Depends(get_current_admin_user)]
