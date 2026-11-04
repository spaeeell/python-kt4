from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from dependencies import require_role
from models import User, UserRole
from schemas import UserRoleUpdate

router = APIRouter(prefix="/admin")


@router.get("/stats")
def get_stats(current_user: User = Depends(require_role(UserRole.ADMIN))):
    return {"message": "Секретная статистика админа", "admin_email": current_user.email}

@router.patch("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    data: UserRoleUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    user.role = data.role
    session.commit()
    session.refresh(user)
    
    return {
    "id": user.id,
    "email": user.email,
    "role": user.role
    }