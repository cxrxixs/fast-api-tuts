import os
from pathlib import Path

from dotenv import load_dotenv
from environs import Env

BASE_DIR = Path(__file__).resolve().parent


dotenv_file = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dotenv_file)


env = Env()
env.read_env()


class Settings:
    # PROJECT
    PROJECT_NAME: str = "FastAPI Tutorial"
    PROJECT_VERSION: str = "0.0.1"

    DEBUG: bool = env.bool("DEBUG", False)
    LOG_LEVEL: str = env("LOG_LEVEL", "warning")

    # DATABASE
    POSTGRES_USER: str = env("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = env("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_PORT: str = env("POSTGRES_PORT", "5432")
    POSTGRES_DB_NAME: str = env("POSTGRES_DB_NAME", "postgres")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
    SQLALCHEMY_ECHO: bool = env.bool("SQLALCHEMY_ECHO", False)


settings = Settings()
