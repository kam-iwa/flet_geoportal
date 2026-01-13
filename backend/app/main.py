import os

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text

from database import db, Base
from routings.layers import router as layers_router
from routings.system import router as system_router
from services.system import hash_password

@asynccontextmanager
async def lifespan(app: FastAPI):
    from services.layers import LayerTable
    from services.system import UserTable

    async with db.engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS data"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS metadata"))

        await conn.run_sync(Base.metadata.create_all, tables=[
            UserTable.__table__,
            LayerTable.__table__
        ])

        admin_login = os.getenv("ADMIN_LOGIN")
        admin_password = os.getenv("ADMIN_PASSWORD")
        admin_hash = hash_password(admin_password)

        await conn.execute(text("""
                                INSERT INTO metadata.user (name, password_hash) 
                                VALUES ( :login, :password ) 
                                ON CONFLICT (name) DO NOTHING
                                """), 
                                {"login": admin_login, "password": admin_hash})
    
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(system_router)
app.include_router(layers_router)