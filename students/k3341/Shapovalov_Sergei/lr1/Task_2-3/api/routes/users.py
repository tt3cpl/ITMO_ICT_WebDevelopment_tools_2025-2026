from fastapi import APIRouter, Depends, HTTPException
from connection import get_session
from services.deps import get_current_user
from services.user_service import UserService
from schemas.users import UserRead, UserUpdate
from models import User
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserRead])
def get_users(session=Depends(get_session)) -> List[UserRead]:
    return UserService.get_all(session)


@router.get("/me", response_model=UserRead)
def get_current_user_info(user_id: int = Depends(get_current_user), session=Depends(get_session)) -> UserRead:
    user = UserService.get(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session=Depends(get_session)) -> UserRead:
    user = UserService.get(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, current_user_id: int = Depends(get_current_user), session=Depends(get_session)) -> UserRead:
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403, detail="Cannot update another user's profile")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name:
        user.name = data.name
    if data.bio is not None:
        user.bio = data.bio

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserRead)
def patch_user(user_id: int, data: UserUpdate, current_user_id: int = Depends(get_current_user), session=Depends(get_session)) -> UserRead:
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403, detail="Cannot update another user's profile")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name:
        user.name = data.name
    if data.bio is not None:
        user.bio = data.bio

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, current_user_id: int = Depends(get_current_user), session=Depends(get_session)):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403, detail="Cannot delete another user")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
