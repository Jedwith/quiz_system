from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Role, User
from src.core.security import get_password_hash, verify_password, create_access_token
from src.schemas.auth import UserRegister, UserLogin, UserResponse, Token
from sqlalchemy import select

async def register(db: AsyncSession, user_data: UserRegister, role_name: str):
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким email уже существует")

    role_result = await db.execute(select(Role).where(Role.name == role_name))
    role = role_result.scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Указанная роль не существует")

    hashed_password = get_password_hash(user_data.password)

    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hashed_password,
        role_id=role.id
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserResponse(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        role=role.name
    )

async def login(db: AsyncSession, user_data: UserLogin):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    # Получаем роль пользователя
    role_result = await db.execute(select(Role).where(Role.id == user.role_id))
    role = role_result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Роль пользователя не найдена"
        )

    access_token = create_access_token(data={"sub": str(user.id), "role": role.name})
    return Token(access_token=access_token, token_type="bearer")
