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

class User(BaseModel):
    id: int
    username: str
    role: Roles