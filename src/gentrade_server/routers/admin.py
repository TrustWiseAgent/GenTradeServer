'''
Admin portal
'''
import logging

from fastapi import APIRouter, Depends
from ..model import settings, Settings
from ..auth import get_user

LOG = logging.getLogger(__name__)

router = APIRouter()

@router.get("/settings")
async def get_settings(user: dict = Depends(get_user)) -> Settings:
    """
    Get server settings
    """
    LOG.info(user)
    return settings
