import logging
import sys
import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator

from app.api import notes, ping, coin
from app.db import engine, metadata, database

# Configure logging at application startup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

print("=== Environment Variables ===")
print(f"PG_DATABASE_HOST: {os.getenv('PG_DATABASE_HOST')}")
print(f"PG_DATABASE_USER: {os.getenv('PG_DATABASE_USER')}")
print(f"PG_DATABASE_DB: {os.getenv('PG_DATABASE_DB')}")
print("==========================")
logger.debug(f"PG_DATABASE_HOST from env: {os.getenv('PG_DATABASE_HOST')}")
logger.debug(f"PG_DATABASE_USER from env: {os.getenv('PG_DATABASE_USER')}")
logger.debug(f"PG_DATABASE_DB from env: {os.getenv('PG_DATABASE_DB')}")

# os.environ["PG_DATABASE_HOST"] = "db"
# os.environ["PG_DATABASE_USER"] = "hello_fastapi"
# os.environ["PG_DATABASE_DB"] = "coin_flipping_db"
# os.environ["PG_DATABASE_PASSWORD"] = "hello_fastapi_password"
metadata.create_all(engine)

app = FastAPI()

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(coin.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]


# @app.get("/ping")
# async def pong():
#     # some async operation could happen here
#     # example: `notes = await get_all_notes()`
#     return {"ping": "pong!"}

@app.on_event("startup")
async def startup():
    # Add debug prints
    logger.debug(f"PG_DATABASE_HOST from env: {os.getenv('PG_DATABASE_HOST')}")
    logger.debug(f"PG_DATABASE_USER from env: {os.getenv('PG_DATABASE_USER')}")
    logger.debug(f"PG_DATABASE_DB from env: {os.getenv('PG_DATABASE_DB')}")
    print("Starting up...")
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    print("Shutting down...")
    await database.disconnect()

