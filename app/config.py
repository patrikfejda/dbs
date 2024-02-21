from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    NAME: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int

settings = Settings()
