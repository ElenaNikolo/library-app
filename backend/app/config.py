from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Ο φάκελος library-app, όπου βρίσκεται το .env.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    DATABASE_URL: str
    SECRET_KEY: str


settings = Settings()
