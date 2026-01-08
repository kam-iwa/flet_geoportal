import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

class Database:
    def __init__(self):
        self.postgres_dbname = os.getenv("POSTGRES_DBNAME")
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_pass = os.getenv("POSTGRES_PASS")
        self.postgres_host = os.getenv("POSTGRES_HOST", "localhost")
        self.postgres_port = int(os.getenv("POSTGRES_PORT", "5432"))

        self.database_url = f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_pass}@{self.postgres_host}:{self.postgres_port}/{self.postgres_dbname}"

        self.engine = create_async_engine(self.database_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

db = Database()
engine = db.engine
async_session = db.async_session

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session