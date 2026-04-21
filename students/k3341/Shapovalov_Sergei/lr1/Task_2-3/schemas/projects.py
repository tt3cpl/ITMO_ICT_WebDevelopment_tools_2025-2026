from pydantic import BaseModel, field_validator
from typing import Optional, List, Union
from datetime import date, datetime


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
    deadline: Optional[Union[date, str]] = None
    tasks: Optional[List[int]] = None
    teams: Optional[List[int]] = None
    
    @field_validator('deadline', mode='before')
    @classmethod
    def parse_deadline(cls, v):
        if v is None:
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S', '%d-%m-%Y']
            for fmt in formats:
                try:
                    return datetime.strptime(v, fmt).date()
                except ValueError:
                    continue
            raise ValueError(f'Unable to parse date: {v}')
        raise ValueError(f'Invalid date type: {type(v)}')
