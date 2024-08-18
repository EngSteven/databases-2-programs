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