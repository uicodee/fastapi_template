from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from app import dto
from app.api import schems
from app.api.dependencies import dao_provider, AuthProvider, get_settings
from app.config import Settings
from app.infrastructure.database.dao.holder import HolderDao

router = APIRouter()


@router.post(
    path="/login",
    description="Login user",
    response_model=dto.Token
)
async def login_user(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        dao: HolderDao = Depends(dao_provider),
        settings: Settings = Depends(get_settings),
) -> dto.Token:
    auth = AuthProvider(settings=settings)
    user = await auth.authenticate_user(
        form_data.username,
        form_data.password,
        dao
    )
    token = auth.create_user_token(
        user=user
    )
    response.set_cookie(key="accessToken", value=token.access_token, httponly=True)
    return token


@router.post(
    path="/register",
    description="Register user",
    response_model=dto.User
)
async def register_user(
        user: schems.RegisterUser,
        dao: HolderDao = Depends(dao_provider),
        settings: Settings = Depends(get_settings),
) -> dto.User:
    current_user = await dao.user.get_user(email=user.email)
    if current_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )
    auth = AuthProvider(settings=settings)
    user = await dao.user.add_user(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=auth.get_password_hash(password=user.password)
    )
    return user
