
from sqlalchemy import select

from database import SessionLocal
from models import User, UserRole


with SessionLocal() as session:
    user = session.scalar(
        select(User).where(
            User.email == "admin@example.com"
        )
    )

    if user:
        user.role = UserRole.ADMIN.value
        session.commit()
        print("Администратор создан!")
    else:
        print("Пользователь не найден!")
