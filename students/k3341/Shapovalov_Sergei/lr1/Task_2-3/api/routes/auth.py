from fastapi import APIRouter, Depends
from connection import get_session
from schemas.auth import RegisterRequest, LoginRequest, ChangePasswordRequest, LoginResponse
from services.auth_service import AuthService
from services.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=LoginResponse)
def register(data: RegisterRequest, session=Depends(get_session)):
    return AuthService.register(session, data)


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, session=Depends(get_session)):
    return AuthService.login(session, data)


@router.post("/change-password")
def change_password(data: ChangePasswordRequest, user_id: int = Depends(get_current_user), session=Depends(get_session)):
    return AuthService.change_password(session, user_id, data.old_password, data.new_password)
