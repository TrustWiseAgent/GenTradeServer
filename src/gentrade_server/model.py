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

class Asset(BaseModel):
    """
    Asset Model_
    """
    name: str = Field(...)
    type: str = Field(...)
    market: str = Field(...)
    quote: str = Field(...)
    cik: int = Field(None, description="only for US stock")
    symbol: str = Field(None, description="only for crypto")
    base: str = Field(None, description="only for crypto")

class OHLCV(BaseModel):
    """
    OHLCV model
    """
    time: int = Field(..., description="UTC timestamp in seconds")
    open: float = Field(...)
    high: float = Field(...)
    low: float = Field(...)
    close: float = Field(...)
    vol: float = Field(...)
