from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.dependencies import SessionDep
from app.core import security
from app.core.config import settings
from app.models.user import (
    Token,
    UserCreate,
    UserPublic,
    UserRegister,
)

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserPublic)
def register(*, session: SessionDep, user_in: UserRegister) -> Any:
    """
    Register new user.
    """
    # Check if user with this email already exists
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )

    # Convert UserRegister to UserCreate
    user_create = UserCreate(
        email=user_in.email,
        password=user_in.password,
        full_name=user_in.full_name,
    )

    # Create new user
    user = crud.create_user(session=session, user_create=user_create)
    return user


@router.post("/login")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 JWT compatible token login, get an access token for future requests
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
