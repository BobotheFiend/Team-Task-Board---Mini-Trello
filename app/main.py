from fastapi import FastAPI

from app.config.settings import create_db_and_tables
from app.controllers.auth_controller import router as auth_router
from app.controllers import task_controller

app = FastAPI(title="Team-Task-Board Mini-Trello")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(auth_router)
app.include_router(task_controller.router)