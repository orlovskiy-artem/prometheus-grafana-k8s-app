import os

from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# load_dotenv()
# Database url if none is passed the default one is used
PG_DATABASE_USER = os.getenv("PG_DATABASE_USER")
PG_DATABASE_PASSWORD = os.getenv("PG_DATABASE_PASSWORD")
PG_DATABASE_HOST = os.getenv("PG_DATABASE_HOST")
PG_DATABASE_DB = os.getenv("PG_DATABASE_DB")
DATABASE_URL = os.getenv(
    "PG_DATABASE_URL",
    f"postgresql://{PG_DATABASE_USER}:{PG_DATABASE_PASSWORD}@{PG_DATABASE_HOST}/{PG_DATABASE_DB}"
)
# Add debug prints
logger.debug(f"PG_DATABASE_HOST from env: {os.getenv('PG_DATABASE_HOST')}")
logger.debug(f"PG_DATABASE_USER from env: {os.getenv('PG_DATABASE_USER')}")
logger.debug(f"PG_DATABASE_DB from env: {os.getenv('PG_DATABASE_DB')}")

# SQLAlchemy√˜
engine = create_engine(DATABASE_URL)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("completed", String(8), default="False"),
    Column("created_date", String(50), default=dt.now(tz("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M"))
)
# Databases query builder

database = Database(DATABASE_URL)
