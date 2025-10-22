from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from src.core.security import verify_token


bearer_scheme = HTTPBearer()


async def get_teacher_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
        if not user_id or role != "teacher":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ разрешён только преподавателям")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")