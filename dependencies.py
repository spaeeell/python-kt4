
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import get_session
from models import User, UserRole
from security import oauth2_scheme, SECRET_KEY


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    error = HTTPException(
        status_code=401,
        detail="Неверный или просроченный токен",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        user_id = int(payload["sub"])

    except (JWTError, KeyError, TypeError, ValueError):
        raise error

    user = session.get(User, user_id)

    if user is None:
        raise error

    return user


def require_role(*allowed_roles: UserRole):

    def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Недостаточно прав"
            )

        return current_user

    return role_checker
