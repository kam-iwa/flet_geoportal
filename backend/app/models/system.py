from datetime import datetime
from database import Base
from pydantic import BaseModel

class TokenSchema(BaseModel):
    id: int
    valid_from: datetime
    valid_to: datetime