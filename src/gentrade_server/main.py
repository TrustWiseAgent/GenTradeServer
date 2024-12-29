"""
The main entry
"""
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .routers import secure, public, agent
from .auth import get_user
from .util import check_server_time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
LOG = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_:FastAPI):
    """
    App lifecycle
    """
    LOG.info("Starting Up...")
    check_server_time()
    yield
    LOG.info("Shutting Down...")

app = FastAPI()
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    public.router,
    prefix="/api/v1/public"
)
app.include_router(
    secure.router,
    prefix="/api/v1/secure",
    dependencies=[Depends(get_user)]
)
app.include_router(
    agent.router,
    prefix="/api/v1/agent",
    dependencies=[Depends(get_user)]
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
