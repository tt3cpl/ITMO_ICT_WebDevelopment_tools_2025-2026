from fastapi import APIRouter, Depends, HTTPException
from connection import get_session
from services.skill_service import SkillService
from schemas.skills import SkillCreate, SkillRead
from models import Skill
from typing import List
from pydantic import BaseModel
from typing import Optional
from models import Skill, User, UserSkillLink


router = APIRouter(prefix="/skills", tags=["Skills"])


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    users: Optional[List[int]] = None


@router.post("/", response_model=SkillRead)
def create_skill(data: SkillCreate, session=Depends(get_session)) -> SkillRead:
    return SkillService.create(session, data)


@router.get("/", response_model=List[SkillRead])
def get_skills(session=Depends(get_session)) -> List[SkillRead]:
    return session.query(Skill).all()


@router.get("/{skill_id}", response_model=SkillRead)
def get_skill(skill_id: int, session=Depends(get_session)) -> SkillRead:
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.put("/{skill_id}", response_model=SkillRead)
def update_skill(skill_id: int, data: SkillUpdate, session=Depends(get_session)) -> SkillRead:
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    if data.name:
        skill.name = data.name
    if data.description is not None:
        skill.description = data.description

    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@router.patch("/{skill_id}", response_model=SkillRead)
def patch_skill(skill_id: int, data: SkillUpdate, session=Depends(get_session)) -> SkillRead:    
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    if data.name:
        skill.name = data.name
    if data.description is not None:
        skill.description = data.description
    
    if data.users is not None:
        session.query(UserSkillLink).filter(UserSkillLink.skill_id == skill_id).delete()
        
        for user_id in data.users:
            user = session.get(User, user_id)
            if user:
                link = UserSkillLink(skill_id=skill_id, user_id=user_id)
                session.add(link)

    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@router.delete("/{skill_id}")
def delete_skill(skill_id: int, session=Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    session.delete(skill)
    session.commit()
    return {"message": "Skill deleted successfully"}
