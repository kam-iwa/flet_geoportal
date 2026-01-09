import base64
import os

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from sqlalchemy import Column, String, Integer

from database import Base


class UserTable(Base): 
    __tablename__ = "user"
    __table_args__ = {"schema": "metadata"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)


def hash_password(password: str) -> str:
    kdf = Scrypt( salt=os.getenv("SECRET_KEY").encode(), length=32, n=1024, r=1, p=1)
    password_hash = base64.b64encode(kdf.derive(password.encode("UTF-8"))).decode("UTF-8")

    return password_hash