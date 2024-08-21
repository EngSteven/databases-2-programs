import uvicorn
from fastapi import FastAPI, HTTPException,File, UploadFile, Depends
from models.schemas import *
from passlib.context import CryptContext
from data import Database
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
import json
from PIL import Image
import io


app = FastAPI()
db = Database()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "TEC"
ALGORITHM = "HS256"


@app.get("/")
async def ver_version():
    return {"version": "0.0.1"}
"""
@app.post("/login")
async def login(login: Login):

    res = db.login(login)
    print(res)
    return res

"""

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.obtener_usuario(form_data.username)

    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Error al iniciar sesión")
    
    token_data = {"sub": user["username"], "role": user["role"]}
    token = create_jwt(token_data)
    return {"access_token": token, "token_type": "bearer"}

def create_jwt(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

@app.post("/register")
async def reg_user(user: CrearUsuario):
    hashed_password = pwd_context.hash(user.password)
    user_data = CrearUsuario(
        username = user.username,
        password = hashed_password,
        role = user.role
    )
    res = db.registrar_usuario(user_data)
    print(res)
    return res

@app.get("/read")
async def get_users():
    res = db.obtener_usuarios()
    print(res)
    return res

@app.delete("/delete")
async def del_user(username: UserName):
    res = db.eliminar_usuario(username)
    print(res)
    return res

@app.put("/update")
async def upd_user(user: CrearUsuario):
    res = db.actualizar_usuario(user)
    print(res)
    return res

@app.delete("/id/delete")
async def del_user_por_id(user_id: UserId):
    res = db.eliminar_usuario_por_id(user_id)
    print(res)
    return res

@app.put("/id/update")
async def upd_user_por_id(user: User):
    res = db.actualizar_usuario_por_id(user)
    print(res)
    return res

@app.post("/posts")
async def upload_file(file: UploadFile = File(...), db: Database = Depends()):
    result = db.save_file(file)
    return {"message": result}

"""@app.post("/posts")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Obtén el tipo de contenido del archivo
        content_type = file.content_type
        
        # Procesamiento según el tipo de archivo
        if content_type.startswith('image/'):
            # Procesar imagen
            image = Image.open(io.BytesIO(await file.read()))
            return {"filename": file.filename, "type": "image", "format": image.format, "size": image.size}
        
        elif content_type.startswith('video/'):
            # Procesar video (por ejemplo, podrías guardar el video)
            video_bytes = await file.read()
            # Puedes agregar más lógica de procesamiento si es necesario

            return {"filename": file.filename, "type": "video", "size": len(video_bytes)}

        elif content_type.startswith('text/'):
            # Procesar archivo de texto
            text = (await file.read()).decode("utf-8")
            #result = db.save_file(file)
            return {"filename": file.filename, "type": "text", "content": text}

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")"""
    

"""@app.post("/posts")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    file_data = UploadFile(
        filename=file.filename,
        content=content,
        file_type=file.content_type
    )
    result = db.save_file(file_data)
    return JSONResponse(content=result)"""

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")