from pydantic import BaseModel
from typing import Optional, List


class SkillInUser(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class ProjectInUser(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str

    class Config:
        from_attributes = True


class TeamInUser(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    bio: Optional[str] = None
    skills: List[SkillInUser] = []
    teams: List[TeamInUser] = []
    owned_projects: List[ProjectInUser] = []
    projects: List[ProjectInUser] = []
    owned_teams: List[TeamInUser] = []

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
