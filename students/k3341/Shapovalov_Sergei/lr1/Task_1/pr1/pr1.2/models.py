from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class ExperienceLevel(Enum):
    junior = "junior"
    middle = "middle"
    senior = "senior"


class Skill(BaseModel):
    id: int
    name: str
    level: ExperienceLevel


class Profile(BaseModel):
    id: int
    bio: str
    experience_years: int
    location: str


class User(BaseModel):
    id: int
    username: str
    email: str
    profile: Profile
    skills: Optional[List[Skill]] = []
