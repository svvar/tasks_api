import os
from contextlib import asynccontextmanager
import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI
from uvicorn.logging import DefaultFormatter, AccessFormatter

from api.routers import auth, tasks
from database import initialize_database


"""
This logging setup may work unexpectedly if using uvicorn workers (multiple processes)
but for demo logging it's ok.
"""

os.makedirs("logs", exist_ok=True)

error_handler = RotatingFileHandler("logs/api.log", maxBytes=10485760, backupCount=3, encoding="utf-8")
error_handler.setFormatter(DefaultFormatter("%(levelprefix)s %(asctime)s - %(message)s", use_colors=False))

access_handler = RotatingFileHandler("logs/api.log", maxBytes=10485760, backupCount=3, encoding="utf-8")
access_handler.setFormatter(AccessFormatter(
    '%(levelprefix)s %(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s', use_colors=False
))

logging.getLogger("uvicorn.error").addHandler(error_handler)
logging.getLogger("uvicorn.access").addHandler(access_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, tags=["auth"])

app.include_router(tasks.router, tags=["tasks"])