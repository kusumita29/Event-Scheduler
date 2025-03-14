from typing import List

from fastapi import HTTPException
from db.schemas.user_schema import User, UserCreate, UserResponse
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    user_id_counter = 1
    users_db = []

    @classmethod
    def create_user(cls, user: UserCreate) -> UserResponse:
        hashed_password = pwd_context.hash(user.password)
        new_user = User(
            id=cls.user_id_counter,
            user_name=user.user_name,
            name=user.name,
            email=user.email,
            password=hashed_password,
        )
        cls.users_db.append(new_user)
        cls.user_id_counter += 1
        return UserResponse(id=new_user.id, user_name=new_user.user_name, name=new_user.name, email=new_user.email)

    @classmethod
    def get_users(cls) -> List[UserResponse]:
        return [UserResponse(id=user.id, user_name=user.user_name, name=user.name, email=user.email) for user in cls.users_db]

    @classmethod
    def get_user(cls, id: int) -> UserResponse:
        for user in cls.users_db:
            if user.id == id:
                return UserResponse(id=user.id, user_name=user.user_name, name=user.name, email=user.email)
        raise HTTPException(status_code=404, detail="User not found")

    @classmethod
    def update_user(cls, id: int, updated_user: UserCreate) -> UserResponse:
        for user in cls.users_db:
            if user.id == id:
                user.user_name = updated_user.user_name
                user.name = updated_user.name
                user.email = updated_user.email
                user.password = pwd_context.hash(updated_user.password)
                return UserResponse(id=user.id, user_name=user.user_name, name=user.name, email=user.email)
        raise HTTPException(status_code=404, detail="User not found")

    @classmethod
    def delete_user(cls, id: int) -> dict:
        for user in cls.users_db:
            if user.id == id:
                cls.users_db.remove(user)
                return {"message": f"User {id} deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")