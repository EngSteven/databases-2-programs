import uvicorn
from fastapi import FastAPI
from models.schemas import *
from data import Database

app = FastAPI()
db = Database()


@app.get("/")
async def ver_version():
    return {"version": "0.0.1"}

@app.post("/login")
async def login(login: Login):
    res = db.login(login)
    print(res)
    return res

@app.post("/register")
async def reg_user(user: CrearUsuario):
    res = db.registrar_usuario(user)
    print(res)
    return res

@app.delete("/delete")
async def elim_user(username: UserName):
    res = db.eliminar_usuario(username)
    print(res)
    return res

@app.put("/update")
async def actu_user(user: CrearUsuario):
    res = db.actualizar_usuario(user)
    print(res)
    return res

@app.delete("/id/delete")
async def elim_user_por_id(user_id: UserId):
    res = db.eliminar_usuario_por_id(user_id)
    print(res)
    return res

@app.put("/id/update")
async def actu_user_por_id(user: User):
    res = db.actualizar_usuario_por_id(user)
    print(res)
    return res

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")