# Internals
from app.core.config import DATABASE_URL

# API and database
from fastapi import FastAPI
from databases import Database

# Logging
from logging import getLogger
logger = getLogger(__name__)


async def connect_to_db(app: FastAPI) -> None:
    database = Database(DATABASE_URL, min_size=2, max_size=10)
    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        logger.warn("--Database Connection Error--")
        logger.warn(e)
        logger.warn("--Database Connection Error--")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--Database Connection Error--")
        logger.warn(e)
        logger.warn("--Database Connection Error--")
