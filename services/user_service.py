from typing import List

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

import jwt_utils
from db.models.user_model import User
from db.schemas.user_schema import UserResponse, UserUpdate


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
        user_id: int, update_user_data: UserUpdate, db: AsyncSession
    ) -> UserResponse:
        """Update an existing user in the database."""

        # Converts Pydantic model to a dictionary (excluding unset fields)
        update_data = update_user_data.model_dump(exclude_unset=True)
        print(update_data)

        # Ensuring we have fields to update
        if not update_data:
            raise HTTPException(
                status_code=400, detail="No fields provided for update."
            )

        # Checking if user is found (scenarios where the user deleted their profile)
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check for unique email
        if "email" in update_data:
            existing_email = await db.execute(
                select(User).where(
                    User.email == update_data["email"], User.id != user_id
                )
            )
            if existing_email.scalars().first():
                raise HTTPException(
                    status_code=400, detail="A user with this email already exists."
                )

        # Check for unique username
        if "user_name" in update_data:
            existing_username = await db.execute(
                select(User).where(
                    User.user_name == update_data["user_name"], User.id != user_id
                )
            )
            if existing_username.scalars().first():
                raise HTTPException(
                    status_code=400, detail="This username is already taken."
                )

        # Hash password if it's being updated
        if "password" in update_data:
            update_data["password"] = jwt_utils.get_password_hash(
                update_data["password"]
            )

        # Perform bulk update using SQLAlchemy's `update()`
        await db.execute(update(User).where(User.id == user_id).values(**update_data))

        await db.commit()
        await db.refresh(user)

        # Fetch the updated user
        updated_user_data = await db.execute(select(User).where(User.id == user_id))
        updated_user_data = updated_user_data.scalars().first()

        return UserResponse.model_validate(updated_user_data)

    @staticmethod
    async def delete_user(user_id: int, db: AsyncSession) -> dict:
        """Delete a user from the database."""
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(user)
        await db.commit()

        return {"message": f"User {user_id} deleted successfully"}
