from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_session
from limiter import limiter
from models import User
from schemas import UserRegister
from security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(data: UserRegister, session: Session = Depends(get_session)):
    existing = session.execute(
        select(User).where(User.email == data.email)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=409, detail="Email уже занят")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
    )

    session.add(user)
    session.commit()

    return {"id": user.id, "email": user.email}


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.execute(
        select(User).where(User.email == form_data.username)
    ).scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    return {"access_token": create_token(user.id), "token_type": "bearer"}
