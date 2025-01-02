"""
Model
"""
from typing import List

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class HealthCheck(BaseModel):
    """
    Response model to validate and return when performing a health check.
    """

    status: str = Field("OK")

class Settings(BaseSettings):
    """
    Settings
    """

    model_config = SettingsConfigDict(enable_decoding=False)

    """
    Settings
    """
    openai_api_key: str = ""
    openai_api_url: str = ""
    openai_api_model: str = "gpt-3.5-turbo"

    ntp_servers : List[str] = Field(
        "ntp.ntsc.ac.cn,ntp.sjtu.edu.cn,cn.ntp.org.cn,cn.pool.ntp.org,ntp.aliyun.com",
        description="The string list of NTP server splitted via comma")

    @field_validator('ntp_servers', mode='before')
    @classmethod
    def decode_ntp_servers(cls, v: str) -> List[str]:
        """decode function override

        Args:
            v (str): input string

        Returns:
            List[str]: splitted list for all NTP servers
        """
        return v.split(',')

settings = Settings()

class Market(BaseModel):
    """
    Response model to validate and return when performing a health check.
    """

    name: str = Field(...)
    type: str = Field(...)
