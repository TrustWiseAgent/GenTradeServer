"""
Secure API interface
"""
import logging
from openai import OpenAI
from fastapi import APIRouter, Depends
from ..auth import get_user
from ..config import settings

LOG = logging.getLogger(__name__)

router = APIRouter()

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_API_URL
)

@router.get("/")
async def get_answer(prompt: str, user: dict = Depends(get_user)):
    """
    Prompt to OpenAI and get answer
    """
    completion = client.chat.completions.create(
        model=settings.OPENAI_API_MODEL,
        messages=[
            {"role": "system", "content":
                "You are a Lu Ken's assistant for cryptocurrency market."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    LOG.info(completion)
    LOG.info(user)
    return {'answer': completion.choices[0].message }
