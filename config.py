from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import os
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8>', extra='ignore')
    
config = Settings()