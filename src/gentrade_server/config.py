"""
Configure
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings
    """
    ntp_server: str = "ntp.ntsc.ac.cn"

settings = Settings()
