"""
The main entry
"""
import sys
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .routers import public, agent, admin
from .auth import get_user
from .util import check_server_time
from .model import settings
from .datahub import DataHub

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
LOG = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_:FastAPI):
    """
    App lifecycle
    """
    LOG.info("Starting Up...")
    LOG.info(settings)
    DataHub.inst().init()
    check_server_time()
    yield
    LOG.info("Shutting Down...")

def receive_signal(number, _):
    """
    Quit on Control + C
    """
    LOG.info('Received Signal: %d', number)
    sys.exit()

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
    agent.router,
    prefix="/api/v1/agent",
    dependencies=[Depends(get_user)]
)

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    dependencies=[Depends(get_user)]
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
