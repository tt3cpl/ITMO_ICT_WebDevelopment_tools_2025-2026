from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import date, datetime


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
    deadline: Optional[Union[date, str]] = None
    description: Optional[str] = None
    
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
