from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.core.security import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_teacher_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = verify_token(token)
    user_id = payload.get("sub")
    role = payload.get("role")

    if not user_id or role != "teacher":
        raise HTTPException( status_code=403, detail="Доступ разрешён только преподавателям")
    return int(user_id)
