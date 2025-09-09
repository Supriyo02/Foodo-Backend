from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    ROUTER_PREFIX: str = "/api/v1"
    TOKEN_SECRET_KEY: str
    TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    model_config=SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()