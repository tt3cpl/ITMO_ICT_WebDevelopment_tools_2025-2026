from pydantic import BaseModel
from typing import Optional, List


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class SkillInLoginUser(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class TeamInLoginUser(BaseModel):
    id: int
    name: str
    project_id: Optional[int]

    class Config:
        from_attributes = True


class ProjectInLoginUser(BaseModel):
    id: int
    title: str
    status: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: "UserInLogin"

    class Config:
        from_attributes = True


class UserInLogin(BaseModel):
    id: int
    name: str
    email: str
    bio: Optional[str]
    skills: List[SkillInLoginUser] = []
    teams: List[TeamInLoginUser] = []
    owned_projects: List[ProjectInLoginUser] = []
    projects: List[ProjectInLoginUser] = []
    owned_teams: List[TeamInLoginUser] = []

    class Config:
        from_attributes = True
