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

class User:
    def __init__(self, id: int, user_name: str, name: str, email: str, password: str):
        self.id = id
        self.user_name = user_name
        self.name = name
        self.email = email
        self.password = password