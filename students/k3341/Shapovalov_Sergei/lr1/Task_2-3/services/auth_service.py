from models import User
from services.security import create_access_token, hash_password, verify_password


class AuthService:

    @staticmethod
    def register(session, data):
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        token = create_access_token({"user_id": user.id})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

    @staticmethod
    def login(session, data):
        user = session.query(User).filter(User.email == data.email).first()

        if not user:
            return {"error": "user not found"}

        if not verify_password(data.password, user.hashed_password):
            return {"error": "wrong password"}

        token = create_access_token({"user_id": user.id})

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

    @staticmethod
    def change_password(session, user_id: int, old_password: str, new_password: str):
        user = session.get(User, user_id)

        if not user:
            return {"error": "user not found"}

        if not verify_password(old_password, user.hashed_password):
            return {"error": "incorrect password"}

        user.hashed_password = hash_password(new_password)
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "password changed successfully"}
