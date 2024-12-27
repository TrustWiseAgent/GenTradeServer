"""
Authorization module
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from .db import check_api_key, get_user_from_api_key

api_key_header = APIKeyHeader(name="X-API-Key")

def get_user(header: str = Security(api_key_header)):
    """
    Get user from the API key
    """
    if check_api_key(header):
        user = get_user_from_api_key(header)
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
