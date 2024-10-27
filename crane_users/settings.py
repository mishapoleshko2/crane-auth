from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field

class AppSettings(BaseSettings):
	model_config = SettingsConfigDict(env_prefix='crane_users_', extra='ignore')
	db_url: PostgresDsn = Field(default=...)

	class Congfig:
		env_file = '.env'
		env_file_encoding = 'utf-8'


settings = AppSettings()
