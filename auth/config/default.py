from os import environ

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic_settings import BaseSettings


class DefaultSettings(BaseSettings):
    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/auth")
    APP_HOST: str = environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8000))

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "auth")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "user")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432")[-4:])
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "hackme")
    DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", 20)
    DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 15)

    SECRET_KEY: str = environ.get("SECRET_KEY", "")
    ALGORITHM: str = environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    )

    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=f"{APP_HOST}:{APP_PORT}{PATH_PREFIX}/user/authentication")

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
