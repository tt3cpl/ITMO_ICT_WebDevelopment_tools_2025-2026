from fastapi import FastAPI
from connection import init_db
from api.routes import auth, projects, tasks, teams, skills, users

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.on_event("startup")
def on_startup():
    init_db()
    
    
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(teams.router)
app.include_router(skills.router)
app.include_router(users.router)