from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from db.schemas.token_schema import TokenResponse
from db.schemas.user_schema import UserCreate, UserLogin, UserResponse
from services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:

    return await AuthService.register_user(user, db)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
) -> TokenResponse:

    try:
        user_data = UserLogin(user_name=form_data.username, password=form_data.password)
        return await AuthService.authenticate_user(user_data, db)
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code, detail="Invalid username or password"
        )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: UserResponse = Depends(AuthService.get_current_user),
) -> UserResponse:
    return current_user
