from pydantic import BaseModel
from typing import Optional, List


class UserInSkill(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class SkillCreate(BaseModel):
    name: str
    description: Optional[str] = None


class SkillRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    users: List[UserInSkill] = []

    class Config:
        from_attributes = True
