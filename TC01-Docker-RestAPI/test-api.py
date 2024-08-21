import unittest
from fastapi.testclient import TestClient
from app import app 


"""
PRUEBAS UNITARIAS
    - Hacer pruebas que prueben que el password sea valido


"""


# Crear un cliente de prueba para la API
client = TestClient(app)
new_user = {
    "username": "sebas123",
    "password": "test",
    "role": "editor"
}
new_user_update = {
    "username": "sebas123",
    "password": "test",
    "role": "administrador"
}
nonexisting_user = {
    "username": "sofia506",
    "password": "1324",
    "role": "editor"
}
login_valid_user = {
    "username": "sebas123",
    "password": "test",
}
login_invalid_user = {
    "username": "sebas123",
    "password": "test5454",
}


print("\nPruebas\n")

class TestAPI(unittest.TestCase):   
  
    def test01_register_nonexisting_user(self):
        response = client.post("/register", json=new_user)
        self.assertEqual(response.status_code, 200)

    def test02_register_existing_user(self):
        response = client.post("/register", json=new_user)
        self.assertEqual(response.status_code, 200)

    def test03_read_users(self):
        response = client.get("/read")
        self.assertEqual(response.status_code, 200)

    def test04_update_existing_user(self):
        response = client.put("/update", json=new_user_update)
        self.assertEqual(response.status_code, 200)

    def test05_update_nonexisting_user(self):
        response = client.put("/update", json=nonexisting_user)
        self.assertEqual(response.status_code, 200) 
    
    def test06_successful_login(self):
        response = client.post("/login", json=login_valid_user)
        self.assertEqual(response.status_code, 200)

    def test07_unsuccessful_login(self):
        response = client.post("/login", json=login_invalid_user)
        self.assertEqual(response.status_code, 200)

    def test08_delete_existing_user(self):
        username = new_user["username"]
        response = client.delete("/delete")
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()