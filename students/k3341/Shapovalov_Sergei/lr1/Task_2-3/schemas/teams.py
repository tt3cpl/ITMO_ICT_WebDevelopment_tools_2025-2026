from pydantic import BaseModel
from typing import Optional, List


class UserInTeam(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ProjectInTeam(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str

    class Config:
        from_attributes = True


class TeamCreate(BaseModel):
    name: str
    project_id: int
    description: Optional[str] = None


class TeamRead(BaseModel):
    id: int
    name: str
    project_id: int
    owner_id: Optional[int]
    description: Optional[str]
    owner: Optional[UserInTeam]
    members: List[UserInTeam] = []
    project: Optional[ProjectInTeam]

    class Config:
        from_attributes = True


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
