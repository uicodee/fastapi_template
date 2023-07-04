from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from app.api.dependencies.authentication import AuthProvider, get_user
from app.api.dependencies.database import DbProvider, dao_provider
from app.api.dependencies.settings import get_settings
from app.config import Settings, load_config


def setup(
        app: FastAPI,
        pool: sessionmaker,
        settings: Settings,
):
    db_provider = DbProvider(pool=pool)
    auth_provider = AuthProvider(settings=settings)
    app.dependency_overrides[get_user] = auth_provider.get_current_user
    app.dependency_overrides[dao_provider] = db_provider.dao
    app.dependency_overrides[AuthProvider] = lambda: auth_provider
    app.dependency_overrides[get_settings] = load_config
