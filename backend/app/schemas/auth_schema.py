from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    name: str
    email: str
    is_admin: bool

class TokenData(BaseModel):
    email: Optional[str] = None
