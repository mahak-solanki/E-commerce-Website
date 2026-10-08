"""
Application configuration.
All values here are read from environment variables (see .env.example).
CHANGE_ME values MUST be replaced before real / production use.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # Shop identity
    SHOP_NAME: str = "Annapurna Bhakti Bhandar"
    SHOP_PHONE: str = "CHANGE_ME"
    SHOP_EMAIL: str = "CHANGE_ME"
    SHOP_ADDRESS: str = "CHANGE_ME"
    WHATSAPP_NUMBER: str = "CHANGE_ME"

    # Admin
    ADMIN_EMAIL: str = "admin@change-me.com"
    ADMIN_PASSWORD: str = "ChangeMe@123"

    # Database. Defaults to a local SQLite file so the project runs
    # instantly out of the box. Set DATABASE_URL to a postgres:// URL
    # to use PostgreSQL in production (see README).
    DATABASE_URL: str = "sqlite:///./annapurna.db"

    # Security
    SECRET_KEY: str = "CHANGE_ME_super_secret_key_please_replace"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    CORS_ORIGINS: str = "*"

    # Delivery
    DELIVERY_CHARGE: float = 50.0
    FREE_DELIVERY_ABOVE: float = 999.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
