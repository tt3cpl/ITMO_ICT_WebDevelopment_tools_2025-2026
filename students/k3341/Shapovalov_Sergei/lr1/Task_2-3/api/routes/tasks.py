from fastapi import APIRouter, Depends, HTTPException
from connection import get_session
from services.deps import get_current_user
from services.task_service import TaskService
from schemas.tasks import TaskCreate, TaskRead, TaskUpdate
from models import Task
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead)
def create_task(data: TaskCreate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> TaskRead:
    result = TaskService.create(session, data, user_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=403, detail=result["error"])
    return result


@router.get("/", response_model=List[TaskRead])
def get_tasks(session=Depends(get_session)) -> List[TaskRead]:
    return session.query(Task).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, session=Depends(get_session)) -> TaskRead:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> TaskRead:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    from models import Project
    project = session.get(Project, task.project_id)
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Only project owner can update tasks")

    if data.title:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.status:
        task.status = data.status
    if data.deadline:
        task.deadline = data.deadline

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def patch_task(task_id: int, data: TaskUpdate, user_id: int = Depends(get_current_user), session=Depends(get_session)) -> TaskRead:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    from models import Project
    project = session.get(Project, task.project_id)
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="Only project owner can update tasks")

    if data.title:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.status:
        task.status = data.status
    if data.deadline:
        task.deadline = data.deadline

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user), session=Depends(get_session)):
    result = TaskService.delete(session, task_id, user_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
