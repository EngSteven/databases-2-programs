import uvicorn
from fastapi import FastAPI
from models.schemas import CrearUsuario
from data import Database

app = FastAPI()



@app.get("/")
async def ver_version():
    return {"version": "0.0.1"}

@app.post("/register")
async def reg_user(user: CrearUsuario):
    db = Database()
    res = db.registrar_usuario(user)
    print(res)
    return res

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")