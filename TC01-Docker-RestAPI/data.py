import psycopg2
import os
from fastapi import *
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
    
    def obtener_usuario(self, username: str):
        cur = self.connection.cursor()
        # Supongamos que tienes una tabla llamada 'usuarios'
        cur.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            return {
                "username": user[0],
                "password": user[1],  # La contraseña hasheada
                "role": user[2]
            }
        return None

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
        
    
    def save_file(self, file: UploadFile):
        try:
            cur = self.connection.cursor()

            # Leer el contenido del archivo
            file_content = file.file.read()

            # Insertar el archivo en la base de datos
            cur.execute("""
                INSERT INTO files (filename, file_type, file_data)
                VALUES (%s, %s, %s)
            """, (file.filename, file.content_type, psycopg2.Binary(file_content)))

            self.connection.commit()
            cur.close()
            return "Archivo guardado exitosamente"

        except psycopg2.Error as e:
            self.connection.rollback()
            raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e.pgerror}")

        finally:
            file.file.close()  # Cerrar el archivo después de leerlo
        
    