from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.models.user_model import User
from db.schemas.user_schema import UserResponse, UserUpdate
from services.auth_service import AuthService
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
) -> List[UserResponse]:
    return await UserService.get_all_users(db)


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    return await UserService.get_user(id, db)


@router.patch("/{id}", response_model=UserResponse)
async def update_user(
    id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
) -> UserResponse:

    if current_user.id != id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403, detail="You can only update your own account."
        )

    return await UserService.update_user(id, user, db)


@router.delete("/{id}")
async def delete_user(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):

    if current_user.id != id and current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403, detail="You can only delete your own account."
        )

    return await UserService.delete_user(id, db)
