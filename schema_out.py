# schemas.py
from pydantic import BaseModel


class UserContactResponse(BaseModel):
    name: str
    email: str | None
    phone: str | None
    