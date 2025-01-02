"""
Secure API interface
"""
import logging
from openai import OpenAI
from fastapi import APIRouter, Depends
from ..auth import get_user
from ..model import settings

LOG = logging.getLogger(__name__)

router = APIRouter()

client = OpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_api_url
)

@router.get("/")
async def get_answer(prompt: str, user: dict = Depends(get_user)):
    """
    Prompt to OpenAI and get answer
    """
    completion = client.chat.completions.create(
        model=settings.openai_api_model,
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
