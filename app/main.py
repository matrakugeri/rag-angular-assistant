from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.db import engine, Base
from app.routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Automatically create database tables defined in models
    Base.metadata.create_all(bind=engine)

    # 2. Test database connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("Database connected")

    yield

    # 3. Clean up database engine connection pool on shutdown
    engine.dispose()

    print("Database disconnected")


app = FastAPI(
    title="Angular RAG Assistant API",
    lifespan=lifespan
)

# 4. Configure CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Include API routes
app.include_router(chat_router, prefix="/api")