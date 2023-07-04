from pydantic import BaseSettings


class DB(BaseSettings):

    host: str
    port: int
    name: str
    user: str
    password: str


class Api(BaseSettings):

    secret: str


class SettingsExtractor(BaseSettings):
    DB__HOST: str
    DB__PORT: int
    DB__NAME: str
    DB__USER: str
    DB__PASSWORD: str

    API__SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    db: DB
    api: Api


def load_config() -> Settings:
    settings = SettingsExtractor()

    return Settings(
        db=DB(
            host=settings.DB__HOST,
            port=settings.DB__PORT,
            name=settings.DB__NAME,
            user=settings.DB__USER,
            password=settings.DB__PASSWORD,
        ),
        api=Api(
            secret=settings.API__SECRET
        )
    )
