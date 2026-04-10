from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from models import Warrior, Profession, Skill, WarriorUpdate
from typing import List, TypedDict
from connection import get_session, init_db
from models import WarriorDefault, Profession, Skill, Warrior, ProfessionDefault, SkillDefault, WarriorSkillsProfessions, WarriorCreate

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/warriors_list")
def warriors_list(session=Depends(get_session)) -> List[WarriorSkillsProfessions]:
    return session.exec(select(Warrior)).all()


@app.get("/warrior/{warrior_id}", response_model=WarriorSkillsProfessions)
def warriors_get(warrior_id: int, session=Depends(get_session)) -> Warrior:
    warrior = session.get(Warrior, warrior_id)
    return warrior


@app.post("/warrior")
def warriors_create(warrior: WarriorCreate, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Warrior}):
    db_warrior = Warrior(
        race=warrior.race,
        name=warrior.name,
        level=warrior.level,
        profession_id=warrior.profession_id,
    )
    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    skills = session.exec(
        select(Skill).where(Skill.id.in_(warrior.skills_ids))
    ).all()

    db_warrior.skills = skills

    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    return db_warrior


@app.patch("/warrior/{warrior_id}")
def warrior_update(warrior_id: int, warrior: WarriorUpdate, session=Depends(get_session)) -> WarriorUpdate:

    db_warrior = session.get(Warrior, warrior_id)

    if not db_warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    warrior_data = warrior.model_dump(exclude_unset=True)

    for key, value in warrior_data.items():
        if key != "skills":
            setattr(db_warrior, key, value)
    
    if "skills" in warrior_data:
        db_warrior.skills = session.exec(
            select(Skill).where(Skill.id.in_(warrior_data["skills"]))
        ).all()
        
    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)

    return db_warrior


@app.get("/professions_list")
def professions_list(session=Depends(get_session)) -> List[Profession]:
    return session.exec(select(Profession)).all()


@app.get("/profession/{profession_id}")
def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
    return session.get(Profession, profession_id)


@app.post("/profession")
def profession_create(prof: ProfessionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Profession}):
    prof = Profession.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}


@app.get("/skills_list")
def skills_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@app.get("/skill/{skill_id}")
def skill_get(skill_id: int, session=Depends(get_session)) -> Skill:
    return session.get(Skill, skill_id)


@app.post("/skill")
def skill_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Skill}):
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}


@app.delete("/skill/delete{skill_id}")
def skill_delete(skill_id: int, session=Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}
