"""
Configure
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings
    """
    OPENAI_API_KEY: str = ""
    OPENAI_API_URL: str = ""
    OPENAI_API_MODEL: str = "gpt-3.5-turbo"

settings = Settings()
