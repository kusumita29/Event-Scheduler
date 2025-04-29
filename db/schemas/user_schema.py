from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from db.enums import UserRole


class UserCreate(BaseModel):
    user_name: str
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        schema_extra = {"example": {"name": "New Name"}}


# Schema for returning user details (response payload).
# Password is excluded for security
class UserResponse(BaseModel):
    id: int  # System-generated
    user_name: str
    name: str
    email: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


# Schema for user login
class UserLogin(BaseModel):
    user_name: str
    password: str
