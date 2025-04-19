from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
import jwt
from jwt.exceptions import InvalidTokenError
from loguru import logger

from config import settings
from dependencies import GetDBDep, OAuth2FormDataDep
from services import auth_service
from schemas.token_schema import Token, TokenData


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/token")
async def login_for_access_token(db: GetDBDep, form_data: OAuth2FormDataDep) -> Token:
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    logger.debug(f"{user = }")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
