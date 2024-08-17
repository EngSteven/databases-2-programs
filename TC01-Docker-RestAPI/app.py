import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from models.task import Task
from models.user import User

app = FastAPI()


@app.get("/")
async def get_version():
    return {"version": "0.1.0"}


@app.post("/task")
async def create_task(task: Task):
    print(task)
    return task

@app.post("/register")
async def register_user(user: User):
    user.userName = input("Inserte el nombre de usuario: ")
    user.password= input("Inserte la contraseña: ")
    return user


@app.get("/usuarios")
async def ver_usuarios(user: User):
    return user

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")
