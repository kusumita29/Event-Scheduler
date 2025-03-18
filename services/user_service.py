from typing import List

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user_model import User
from db.schemas.user_schema import UserCreate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

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
    async def update_user(
        user_id: int, updated_user: UserCreate, db: AsyncSession
    ) -> UserResponse:
        """Update an existing user in the database."""
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if email is already taken by another user
        existing_email = await db.execute(
            select(User).where(User.email == updated_user.email, User.id != user_id)
        )

        if existing_email.scalars().first():
            raise HTTPException(
                status_code=400, detail="A user with this email already exists."
            )

        # Checks if username is already taken
        existing_username = await db.execute(
            select(User).where(
                User.user_name == updated_user.user_name, User.id != user_id
            )
        )

        if existing_username.scalars().first():
            raise HTTPException(
                status_code=400, detail="This username is already taken."
            )

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
