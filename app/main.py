from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from app.database.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("Database connected")

    yield

    engine.dispose()

    print("Database disconnected")


app = FastAPI(lifespan=lifespan)





