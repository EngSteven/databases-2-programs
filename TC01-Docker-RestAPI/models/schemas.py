from pydantic import BaseModel
from enum import Enum

class Roles(str, Enum):
    admin = "administrador"
    editor = "editor"
    lector = "lector"

class CrearUsuario(BaseModel):
    username: str
    password: str
    role: Roles

class Token(BaseModel):
    access_token: str
    token_type: str

class UserId(BaseModel):
    id: int

class UserName(BaseModel):
    username: str

class User(BaseModel):
    id: int
    username: str
    password: str
    role: Roles

class Login(BaseModel):
    username: str
    password: str

class UploadFile2(BaseModel):
    filename: str
    content: bytes  # El contenido del archivo se manejará como bytes
    file_type: str

    class Config:
        orm_mode = True