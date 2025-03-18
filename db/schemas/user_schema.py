from pydantic import BaseModel, ConfigDict

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    user_name: str
    name: str
    email: str
    password: str  # Required for creation


# Schema for returning user details (response payload).
# Password is excluded for security
class UserResponse(BaseModel):
    id: int  # System-generated
    user_name: str
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


# Schema for user login
class UserLogin(BaseModel):
    user_name: str
    password: str
