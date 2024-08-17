import psycopg2
import os
from fastapi import HTTPException
#from passlib.context import CryptContext
from models.schemas import CrearUsuario

#pwd_context = CryptContext(schemes=["bycrypt"], deprecated="auto")


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            database=os.environ.get("DB_DB"),
        )

    #def password_hash(self, password):
        #return pwd_context.hash(password)
    
    def registrar_usuario(self, user: CrearUsuario):
        id_user = 0
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('CALL registrar_usuario(%s,%s,%s,%s)', (user.username, user.password, user.role.value, id_user))
            
            # Obtener el resultado, por ejemplo, el ID del usuario registrado
            result = cur.fetchone()
            if result is None:
                raise HTTPException(status_code=400, detail="Error en el registro del usuario")
            
            user_id = result[0]  # Asumiendo que el SP devuelve el ID del usuario registrado

            self.connection.commit()
            cur.close()

            return {"id": user_id, "username": user.username, "role": user.role}

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar el usuario: {e.pgerror}")