from models import User


class UserService:

    @staticmethod
    def create(session, user_data, hashed_password: str):
        user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


    @staticmethod
    def get(session, user_id: int):
        return session.get(User, user_id)


    @staticmethod
    def get_all(session):
        return session.query(User).all()