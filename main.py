from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI, status
from pydantic import BaseModel
import logging
import os

# set variables from env
DATABASE_URL = os.getenv("DATABASE_URL")
MODE = os.getenv("mode")
LOG_LEVEL = os.getenv("LOG_LEVEL")

# logging config
logging.config.fileConfig('logging.conf', disable_existing_loggers=True)
logger = logging.getLogger(__name__)

if LOG_LEVEL == "debug":
    logger.setLevel(logging.DEBUG)
    logger.debug("Mode is set to: {0}".format(MODE))

# connects to the database and retrieves current state
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# creates store table schema 
stores = sqlalchemy.Table(
    "store",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL, pool_size=3, max_overflow=0)
metadata.create_all(engine)

# data models
class StoreIn(BaseModel): # for post requests
    name: str

class Store(BaseModel): # to db
    id: int
    name: str

app = FastAPI()

# db events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# set endpoints
@app.get("/stores/", response_model=List[Store], status_code = status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):
    query = stores.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@app.post("/stores/", response_model=Store, status_code = status.HTTP_201_CREATED)
async def create_note(store: StoreIn):
    query = stores.insert().values(name=store.name)
    last_record_id = await database.execute(query)
    return {**store.dict(), "id": last_record_id}

