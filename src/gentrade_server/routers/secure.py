"""
Secure API interface
"""
from fastapi import APIRouter, Depends
from ..auth import get_user

router = APIRouter()

@router.get("/")
async def get_testroute(user: dict = Depends(get_user)):
    """
    Test secure interface
    """
    return user