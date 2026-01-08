from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from database import db, Base
from routings.system import router as system_router

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db.engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS data"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS metadata"))

        await conn.run_sync(Base.metadata.create_all)

app.include_router(system_router)