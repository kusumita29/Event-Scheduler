from typing import List
from fastapi import APIRouter

from db.schemas.user_schema import UserCreate, UserResponse
from services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    return UserService.create_user(user)

@router.get("/users/", response_model=List[UserResponse])
def get_users():
    return UserService.get_users()

@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int):
    return UserService.get_user(id)

@router.put("/users/{id}", response_model=UserResponse)
def update_user(id: int, user: UserCreate):
    return UserService.update_user(id, user)

@router.delete("/users/{id}")
def delete_user(id: int):
    return UserService.delete_user(id)