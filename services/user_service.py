from os import stat_result
from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.schemas.user_schema import UserCreate, UserResponse
from passlib.context import CryptContext

from db.models.user_model import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    
    @staticmethod
    async def create_user(user: UserCreate, db: AsyncSession) -> UserResponse:
        """Creates a user and stores it in the database."""
        hashed_password = pwd_context.hash(user.password)
        new_user = User(
            user_name=user.user_name,
            name=user.name,
            email=user.email,
            password=hashed_password,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return UserResponse.model_validate(new_user)


    @staticmethod
    async def get_all_users(db: AsyncSession) -> List[UserResponse]:
        """Fetch all users from the database."""
        result = await db.execute(select(User))
        users = result.scalars().all()
        return [UserResponse.model_validate(user) for user in users]


    @staticmethod
    async def get_user(user_id: int, db: AsyncSession) -> UserResponse:
        """Fetch an user by ID."""
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)


    @staticmethod
    async def update_user(user_id: int, updated_user: UserCreate, db: AsyncSession) -> UserResponse:
        """Update an existing user in the database."""
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.user_name = updated_user.user_name
        user.name = updated_user.name
        user.email = updated_user.email
        user.password = pwd_context.hash(updated_user.password)

        await db.commit()
        await db.refresh(user)

        return UserResponse.model_validate(user)


    @staticmethod
    async def delete_user(user_id: int, db: AsyncSession) -> dict:
        """Delete a user from the database."""
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(user)
        await db.commit()

        return {"message": f"User {user_id} deleted successfully"}