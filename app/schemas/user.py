from pydantic import BaseModel, EmailStr
from uuid import UUID

# request
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# response
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
