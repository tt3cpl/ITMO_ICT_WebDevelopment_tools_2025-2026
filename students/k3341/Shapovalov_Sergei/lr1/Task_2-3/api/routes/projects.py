from fastapi import APIRouter, Depends, HTTPException
from connection import get_session
from services.deps import get_current_user
from services.project_service import ProjectService
from schemas.projects import ProjectCreate, ProjectRead, ProjectUpdate
from typing import List
from models import Project, Task, Team, UserProjectLink, UserTeamLink


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead)
def create_project(data: ProjectCreate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> ProjectRead:
    return ProjectService.create(session, data, user_id)


@router.get("/", response_model=List[ProjectRead])
def get_projects(session=Depends(get_session)) -> List[ProjectRead]:
    return ProjectService.get_all(session)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session=Depends(get_session)) -> ProjectRead:
    project = ProjectService.get_by_id(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, data: ProjectUpdate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> ProjectRead:
    result = ProjectService.update(session, project_id, data, user_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=403, detail=result["error"])
    return result


@router.patch("/{project_id}", response_model=ProjectRead)
def patch_project(project_id: int, data: ProjectUpdate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> ProjectRead:
    
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Only project owner can update project")
    if data.title:
        project.title = data.title
    if data.description is not None:
        project.description = data.description
    if data.status:
        project.status = data.status
    if data.deadline:
        project.deadline = data.deadline
    
    if data.tasks is not None:
        project.tasks.clear()
        for task_id in data.tasks:
            task = session.get(Task, task_id)
            if task and task.project_id == project_id:
                project.tasks.append(task)
    
    if data.teams is not None:
        project.teams.clear()
        for team_id in data.teams:
            team = session.get(Team, team_id)
            if team and team.project_id == project_id:
                project.teams.append(team)
    
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, user_id: int = Depends(get_current_user), session=Depends(get_session)):
    return ProjectService.delete(session, project_id, user_id)


@router.post("/{project_id}/join")
def join_project(project_id: int, user_id: int = Depends(get_current_user), session=Depends(get_session)):
    return ProjectService.add_member(session, project_id, user_id)
