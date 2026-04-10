from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class UserInProject(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class TaskInProject(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    deadline: Optional[date]

    class Config:
        from_attributes = True


class TeamInProject(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: Optional[int]

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ProjectRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    owner_id: int
    deadline: Optional[date]
    owner: Optional[UserInProject]
    teams: List[TeamInProject] = []
    tasks: List[TaskInProject] = []
    members: List[UserInProject] = []

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[date] = None
