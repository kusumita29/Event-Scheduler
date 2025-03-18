from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.database import get_db
from db.enums import UserRole
from db.models.user_model import User
from db.schemas.token_schema import TokenResponse
from db.schemas.user_schema import UserCreate, UserLogin, UserResponse
from jwt_utils import create_access_token, decode_access_token, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    async def register_user(user: UserCreate, db: AsyncSession) -> UserResponse:
        """Creates a user and stores it in the database."""
        hashed_password = pwd_context.hash(user.password)
        new_user = User(
            user_name=user.user_name,
            name=user.name,
            email=user.email,
            password=hashed_password,
            role=UserRole.USER,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return UserResponse.model_validate(new_user)

    @staticmethod
    async def authenticate_user(
        user_data: UserLogin, db: AsyncSession
    ) -> TokenResponse:
        """Authenticate user and return JWT token"""
        result = await db.execute(
            select(User).where(User.user_name == user_data.user_name)
        )
        user = result.scalars().first()

        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_access_token(
            {"sub": user.user_name}
        )  # Use username as JWT subject
        return TokenResponse(access_token=token, token_type="bearer")

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
    ) -> User:
        """Get user from JWT token"""

        payload = decode_access_token(token)

        if "error" in payload:
            raise HTTPException(status_code=401, detail=payload["error"])

        user_name = payload.get("sub")
        if not user_name:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        result = await db.execute(select(User).where(User.user_name == user_name))
        user = result.scalar()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
