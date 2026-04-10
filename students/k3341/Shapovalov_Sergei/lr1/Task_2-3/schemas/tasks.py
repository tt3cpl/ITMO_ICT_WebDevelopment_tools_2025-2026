from pydantic import BaseModel
from typing import Optional
from datetime import date


class ProjectInTask(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int


class TaskRead(BaseModel):
    id: int
    title: str
    status: str
    deadline: Optional[date]
    project_id: int
    description: Optional[str]
    project: Optional[ProjectInTask]

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None
    deadline: Optional[date] = None
    description: Optional[str] = None
