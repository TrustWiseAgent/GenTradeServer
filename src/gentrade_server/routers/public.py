"""
Public result API interfaces
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_testroute():
    """
    Test public interface
    """
    return "OK"
