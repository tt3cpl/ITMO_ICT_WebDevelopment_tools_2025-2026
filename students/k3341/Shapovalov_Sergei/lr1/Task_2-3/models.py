from datetime import date
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field, Relationship


class UserSkillLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(
        default=None,
        foreign_key="skill.id",
        primary_key=True,
    )
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        primary_key=True,
    )


class UserTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(
        default=None,
        foreign_key="team.id",
        primary_key=True,
    )
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        primary_key=True,
    )


class UserProjectLink(SQLModel, table=True):
    project_id: Optional[int] = Field(
        default=None,
        foreign_key="project.id",
        primary_key=True,
    )
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        primary_key=True,
    )


class StatusType(str, Enum):
    active = "active"
    inactive = "inactive"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    bio: Optional[str] = ""
    hashed_password: str
    skills: List["Skill"] = Relationship(
        back_populates="users", link_model=UserSkillLink)
    teams: List["Team"] = Relationship(
        back_populates="members", link_model=UserTeamLink)
    owned_projects: List["Project"] = Relationship(back_populates="owner")
    projects: List["Project"] = Relationship(
        back_populates="members", link_model=UserProjectLink)
    owned_teams: List["Team"] = Relationship(back_populates="owner")


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = ""
    users: List["User"] = Relationship(
        back_populates="skills", link_model=UserSkillLink)


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = ""
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="owned_teams")
    members: List["User"] = Relationship(
        back_populates="teams", link_model=UserTeamLink)
    project_id: int = Field(foreign_key="project.id")
    project: Optional["Project"] = Relationship(back_populates="teams")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = ""
    status: StatusType
    deadline: Optional[date] = None
    project_id: int = Field(foreign_key="project.id")
    project: Optional["Project"] = Relationship(back_populates="tasks")


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = ""
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="owned_projects")
    deadline: Optional[date] = None
    status: StatusType
    teams: List["Team"] = Relationship(back_populates="project")
    tasks: List["Task"] = Relationship(back_populates="project")
    members: List["User"] = Relationship(
        back_populates="projects", link_model=UserProjectLink)
