from lib2to3.pytree import Base
from re import A
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()