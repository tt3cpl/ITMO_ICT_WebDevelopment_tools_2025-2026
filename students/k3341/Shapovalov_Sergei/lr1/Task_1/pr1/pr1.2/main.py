from fastapi import FastAPI
from models import User, Profile, Skill
from typing import List, TypedDict

app = FastAPI()

@app.get("/")
def hello():
    return "Hello, [username]!"

temp_bd = [
    {
        "id": 1,
        "username": "alex_dev",
        "email": "alex@example.com",
        "profile": {
            "id": 1,
            "bio": "Full-stack разработчик с опытом в веб-приложениях",
            "experience_years": 5,
            "location": "Москва"
        },
        "skills": [
            {
                "id": 1,
                "name": "Python",
                "level": "senior"
            },
            {
                "id": 2,
                "name": "FastAPI",
                "level": "middle"
            }
        ]
    },
    {
        "id": 2,
        "username": "maria_designer",
        "email": "maria@example.com",
        "profile": {
            "id": 2,
            "bio": "UI/UX дизайнер, ищу проекты в области мобильных приложений",
            "experience_years": 3,
            "location": "Санкт-Петербург"
        },
        "skills": [
            {
                "id": 3,
                "name": "Figma",
                "level": "senior"
            },
            {
                "id": 4,
                "name": "Adobe XD",
                "level": "middle"
            }
        ]
    },
    {
        "id": 3,
        "username": "ivan_pm",
        "email": "ivan@example.com",
        "profile": {
            "id": 3,
            "bio": "Project Manager, специализируюсь на Agile методологии",
            "experience_years": 7,
            "location": "Казань"
        },
        "skills": [
            {
                "id": 5,
                "name": "Jira",
                "level": "senior"
            },
            {
                "id": 6,
                "name": "Confluence",
                "level": "middle"
            }
        ]
    }
]


@app.get("/users_list")
def users_list() -> List[User]:
    return temp_bd


@app.get("/user/{user_id}")
def user_get(user_id: int) -> List[User]:
    return [user for user in temp_bd if user.get("id") == user_id]


@app.post("/user")
def user_create(user: User) -> TypedDict('Response', {"status": int, "data": User}):
    user_to_append = user.model_dump()
    temp_bd.append(user_to_append)
    return {"status": 200, "data": user}


@app.delete("/user/delete{user_id}")
def user_delete(user_id: int):
    for i, user in enumerate(temp_bd):
        if user.get("id") == user_id:
            temp_bd.pop(i)
            break
    return {"status": 201, "message": "deleted"}


@app.put("/user{user_id}")
def user_update(user_id: int, user: User) -> List[User]:
    for usr in temp_bd:
        if usr.get("id") == user_id:
            user_to_append = user.model_dump()
            temp_bd.remove(usr)
            temp_bd.append(user_to_append)
    return temp_bd


@app.get("/user/{user_id}/profile")
def profile_get(user_id: int) -> List[Profile]:
    return [user.get("profile") for user in temp_bd if user.get("id") == user_id]


@app.post("/user/{user_id}/profile")
def profile_create(user_id: int, profile: Profile) -> TypedDict('Response', {"status": int, "data": Profile}):
    for user in temp_bd:
        if user.get("id") == user_id:
            user["profile"] = profile.model_dump()
            return {"status": 200, "data": profile}
    return {"status": 404, "message": "User not found"}


@app.put("/user/{user_id}/profile")
def profile_update(user_id: int, profile: Profile) -> TypedDict('Response', {"status": int, "data": Profile}):
    for user in temp_bd:
        if user.get("id") == user_id:
            user["profile"] = profile.model_dump()
            return {"status": 200, "data": profile}
    return {"status": 404, "message": "User not found"}


@app.delete("/user/{user_id}/profile")
def profile_delete(user_id: int):
    for user in temp_bd:
        if user.get("id") == user_id:
            user["profile"] = None
            return {"status": 201, "message": "Profile deleted"}
    return {"status": 404, "message": "User not found"}
