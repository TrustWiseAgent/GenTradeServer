"""
Public result API interfaces
"""
import logging

import time
import datetime
from dateutil.tz import tzlocal

from fastapi import APIRouter
from pydantic import BaseModel

from ..util import sync_ntp_server
from ..config import settings

LOG = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def get_testroute():
    """
    Test public interface
    """
    return "OK"

class HealthCheck(BaseModel):
    """
    Response model to validate and return when performing a health check.
    """

    status: str = "OK"

@router.get("/health")
async def get_health() -> HealthCheck:
    """
    Check health
    """
    return HealthCheck(status="OK")

@router.get("/settings")
async def get_settings():
    """
    Get server settings
    """
    return {
        'ntp_server': settings.ntp_server
    }

@router.get("/server_time")
async def get_server_time():
    """
    Get server time
    """
    curr_ts = time.time()
    now_utc   = datetime.datetime.fromtimestamp(curr_ts, datetime.UTC)
    tl = tzlocal()

    return {
        'timezone_name': tl.tzname(now_utc),
        'timezone_offset': tl.utcoffset(now_utc).total_seconds(),
        'timestamp_server': int(curr_ts)
    }
