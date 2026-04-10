from fastapi import FastAPI
from models import Warrior, Profession, Skill
from typing import List, TypedDict


app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


temp_bd = [
    {

        "id": 1,

        "race": "director",

        "name": "Мартынов Дмитрий",

        "level": 12,

        "profession": {

            "id": 1,

            "title": "Влиятельный человек",

            "description": "Эксперт по всем вопросам"

        },

        "skills":

        [{

            "id": 1,

            "name": "Купле-продажа компрессоров",

            "description": ""


        },

            {

            "id": 2,

            "name": "Оценка имущества",

            "description": ""


        }]
    },
    {

        "id": 2,

        "race": "worker",

        "name": "Андрей Косякин",

        "level": 12,

        "profession": {

            "id": 1,

            "title": "Дельфист-гребец",

            "description": "Уважаемый сотрудник"

        },

        "skills": []
    },
]



@app.get("/warriors_list")
def warriors_list() -> List[Warrior]:
    
    return temp_bd


@app.get("/warrior/{warrior_id}")
def warriors_get(warrior_id: int) -> List[Warrior]:
    
    return [warrior for warrior in temp_bd if warrior.get("id") == warrior_id]


@app.post("/warrior")
def warriors_create(warrior: Warrior) -> TypedDict('Response', {"status": int, "data": Warrior}):
    
    warrior_to_append = warrior.model_dump()
    
    temp_bd.append(warrior_to_append)
    
    return {"status": 200, "data": warrior}


@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    
    for i, warrior in enumerate(temp_bd):
        
        if warrior.get("id") == warrior_id:
            
            temp_bd.pop(i)
            
            break
    
    return {"status": 201, "message": "deleted"}


@app.put("/warrior{warrior_id}")
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    
    for war in temp_bd:
        
        if war.get("id") == warrior_id:
            
            warrior_to_append = warrior.model_dump()
            
            temp_bd.remove(war)
            
            temp_bd.append(warrior_to_append)
    
    return temp_bd



@app.get("/warrior/{warrior_id}/professions_list")
def professions_list(warrior_id: int) -> List[Profession]:
    
    return [warrior.get("profession") for warrior in temp_bd if warrior.get("id") == warrior_id]

@app.get("/warrior/{warrior_id}/profession/{profession_id}")
def profession_get(warrior_id: int, profession_id: int) -> List[Profession]:
    
    return [warrior.get("profession") for warrior in temp_bd if warrior.get("id") == warrior_id and warrior.get("profession").get("id") == profession_id]    

@app.post("/warrior/{warrior_id}/profession")
def profession_create(warrior_id: int, profession: Profession) -> TypedDict('Response', {"status": int, "data": Profession}):
    
    for war in temp_bd:
        
        if war.get("id") == warrior_id:
            
            profession_to_append = profession.model_dump()
            
            war["profession"] = profession_to_append
            
            break
    
    return {"status": 200, "data": profession}

@app.delete("/warrior/{warrior_id}/profession/delete")
def profession_delete(warrior_id: int):
    
    for war in temp_bd:
        
        if war.get("id") == warrior_id:
            
            war["profession"] = None
            
            break
    
    return {"status": 201, "message": "deleted"}

@app.put("/warrior/{warrior_id}/profession")
def profession_update(warrior_id: int, profession: Profession) -> List[Profession]:
    
    for war in temp_bd:
        
        if war.get("id") == warrior_id:
            
            profession_to_append = profession.model_dump()
            
            war["profession"] = profession_to_append
            
            break
    
    return [warrior.get("profession") for warrior in temp_bd if warrior.get("id") == warrior_id]    