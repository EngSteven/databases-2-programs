import psycopg2
import os
from fastapi import HTTPException
#from passlib.context import CryptContext
from models.schemas import *

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
    
    def login(self, login: Login):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT login(%s,%s)', (login.username, login.password))
            
            # Obtener el resultado, por ejemplo, el ID del usuario registrado
            status = cur.fetchone()[0]
                        
            self.connection.commit()
            cur.close()

            if status == 1:
                return "Login exitoso"
            else:
                return "Login fallido"

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error realizar el login: {e.pgerror}")

    def registrar_usuario(self, user: CrearUsuario):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT registrar_usuario(%s,%s,%s)', (user.username, user.password, user.role.value))
            
            # Obtener el resultado, por ejemplo, el ID del usuario registrado
            user_id = cur.fetchone()[0]
                        
            self.connection.commit()
            cur.close()

            if user_id != -1:
                return {"id": user_id, "username": user.username, "role": user.role}
            else:
                return "El nombre de usuario ingresado ya existe"

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar el usuario: {e.pgerror}")


    def obtener_usuarios(self):
        try:
            cur = self.connection.cursor()

            # Llamada al procedimiento almacenado para registrar al usuario
            cur.execute('SELECT obtener_usuarios()')
            
            # Obtener el resultado, por ejemplo, el ID del usuario registrado
            data = cur.fetchall()
                        
            self.connection.commit()
            cur.close()

            if data != None:
                return data
            else:
                return "No se ha podido obtener los datos"

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al registrar obtener los usuarios: {e.pgerror}")
    

    def eliminar_usuario_por_id(self, user_id: UserId):
        try:
            status = 0
            cur = self.connection.cursor()

            # Llamada a la funcion de la base de datos para eliminar al usuario
            cur.execute("SELECT eliminar_usuario_por_id(%s);", (user_id.id,))
            status = cur.fetchone()[0]
            self.connection.commit()
            cur.close()
            
            if status == 1:
                return "Usuario eliminado correctamente"
            else: 
                return "El id del usuario ingresado no existe"
                
        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario: {e.pgerror}")

        
    def eliminar_usuario(self, username: UserName):
        try:
            status = 0
            cur = self.connection.cursor()

            # Llamada a la funcion de la base de datos para eliminar al usuario
            cur.execute("SELECT eliminar_usuario(%s);", (username.username,))
            status = cur.fetchone()[0]
            self.connection.commit()
            cur.close()
            
            if status == 1:
                return "Usuario eliminado correctamente"
            else: 
                return "El nombre de usuario ingresado no existe"
                
        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario: {e.pgerror}")
        
    def actualizar_usuario_por_id(self, user: User):
        try:
            status = 0
            cur = self.connection.cursor()

            # Llamada a la funcion de la base de datos para actualizar al usuario
            cur.execute("SELECT actualizar_usuario_por_id(%s, %s, %s, %s);", (user.id, user.username, user.password, user.role.value))
            status = cur.fetchone()[0]
            self.connection.commit()
            cur.close()
            
            if status == 1:
                return "Usuario actualizado correctamente"
            else: 
                return "El id del usuario ingresado no existe"
                
        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {e.pgerror}")

    def actualizar_usuario(self, user: CrearUsuario):
        try:
            status = 0
            cur = self.connection.cursor()

            # Llamada a la funcion de la base de datos para actualizar al usuario
            cur.execute("SELECT actualizar_usuario(%s, %s, %s);", (user.username, user.password, user.role.value))
            status = cur.fetchone()[0]
            self.connection.commit()
            cur.close()
            
            if status == 1:
                return "Usuario actualizado correctamente"
            else: 
                return "El nombre de usuario ingresado no existe"
                
        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {e.pgerror}")
        
    
        
    

