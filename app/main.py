from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.config.settings import create_db_and_tables
from app.controllers.auth_controller import router as auth_router
from app.controllers import task_controller
from app.controllers.team_controller import router as team_router

app = FastAPI(title="Team-Task-Board Mini-Trello")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)
app.include_router(task_controller.router)
app.include_router(team_router)
