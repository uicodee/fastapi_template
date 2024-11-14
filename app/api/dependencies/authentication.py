from datetime import timedelta, datetime

import pytz
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from app import dto
from app.api.dependencies.database import dao_provider
from app.config import Settings
from app.infrastructure.database.dao.holder import HolderDao

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_user(token: str = Depends(oauth2_scheme)) -> dto.User:
    raise NotImplementedError


class AuthProvider:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.api.secret
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(days=3)
        self.refresh_token_expire = timedelta(days=30)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def authenticate_user(
        self, email: str, password: str, dao: HolderDao
    ) -> dto.User:
        http_status_401 = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        user = await dao.user.get_user(email=email, with_password=True)
        if user is None:
            raise http_status_401
        if not self.verify_password(password, user.password):
            raise http_status_401
        return user

    def create_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=pytz.timezone("Asia/Tashkent")) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_user_tokens(self, user: dto.User) -> dto.Token:
        access_token = self.create_token(
            data={"sub": user.email},
            expires_delta=self.access_token_expire,
        )
        refresh_token = self.create_token(
            data={"sub": user.email}, expires_delta=self.refresh_token_expire
        )
        return dto.Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        dao: HolderDao = Depends(dao_provider),
    ) -> dto.User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await dao.user.get_user(email=email)
        if user is None:
            raise credentials_exception
        return user

    async def refresh_access_token(
        self, refresh_token: str, dao: HolderDao = Depends(dao_provider)
    ) -> dto.Token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                refresh_token, self.secret_key, algorithms=[self.algorithm]
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = await dao.user.get_user(email=email)
        if user is None:
            raise credentials_exception

        return self.create_user_tokens(user=user)
