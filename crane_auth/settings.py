from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, SecretStr, Field


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="crane_auth_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8`",
    )
    db_url: PostgresDsn = Field(default=...)
    jwt_secret: SecretStr = Field(default=...)
    access_token_ttl: int = Field(default=...)
    refresh_token_ttl: int = Field(default=...)
    jwt_encoding_algorithm: str = Field(default=...)


settings = AppSettings()
