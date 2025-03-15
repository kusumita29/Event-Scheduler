from typing import List
from fastapi import APIRouter, Depends

from db.database import get_db
from db.schemas.user_schema import UserCreate, UserResponse
from services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    return await UserService.create_user(user, db)

@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)) -> List[UserResponse]:
    return await UserService.get_all_users(db)

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    return await UserService.get_user(id, db)

@router.put("/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    return await UserService.update_user(id, user, db)

@router.delete("/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    return await UserService.delete_user(id, db)