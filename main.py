from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from dependencies import get_current_user
from limiter import limiter
from models import User
from routes.auth import router as auth_router
from routes.admin import router as admin_router
from dependencies import require_role, UserRole

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://newlxp.ru", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(admin_router)


@app.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }


@app.get("/moderate")
def moderate_page(current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.MODERATOR))):
    return {
        "message": "Страница модератора",
        "user_email": current_user.email    
    }