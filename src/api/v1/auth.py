from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.schemas.auth import UserRegister, UserResponse, Token, UserLogin
from src.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register/student", response_model=UserResponse, summary="Регистрация студента")
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    return await auth_service.register(db, user, role_name="student")

@router.post("/register/teacher", response_model=UserResponse, summary="Регистрация преподавателя")
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    return await auth_service.register(db, user, role_name="teacher")

@router.post("/login", response_model=Token, summary="Авторизация")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth_service.login(db, user)
