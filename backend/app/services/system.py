import base64
from typing import Optional
from fastapi import Header
import jwt
import os

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, text
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base


def hash_password(password: str) -> str:
    kdf = Scrypt( salt=os.getenv("SECRET_KEY").encode(), length=32, n=1024, r=1, p=1)
    password_hash = base64.b64encode(kdf.derive(password.encode("UTF-8"))).decode("UTF-8")

    return password_hash

async def get_token(x_access_token: Optional[str] = Header(None, alias="X-Access-Token")):
    return await UserService().verify_token(x_access_token)


class UserTable(Base): 
    __tablename__ = "user"
    __table_args__ = {"schema": "metadata"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


class UserService:
    async def authenticate(self, db: AsyncSession, login: str, password: str) -> dict | None:
        password_hash = hash_password(password)
        user_query = await db.execute(text("""
                            SELECT u.id, u.name, u.password_hash 
                            FROM metadata.user as u
                            WHERE u.name = :login and u.password_hash = :password
                            """), {"login": login, "password": password_hash})
        user = user_query.fetchone()
        
        return {"id": user[0], "name": user[1]} if user else None
    
    async def create_token(self, data: dict) -> str:
        token_data = data.copy()
        token_data.update({"exp": datetime.now() + timedelta(minutes=60), "iat": datetime.now()})
        encoded_jwt = jwt.encode(token_data, os.getenv("SECRET_KEY"), algorithm="HS256")
        return encoded_jwt
    
    async def verify_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(
                token,
                os.getenv("SECRET_KEY"),
                algorithms=["HS256"]
            )
            return payload
        except jwt.InvalidTokenError:
            return None