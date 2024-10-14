from neo4j import GraphDatabase
from faker import Faker


class Database:
    def __init__(self):
        self.URI = "neo4j://localhost:7687"
        self.AUTH = ("neo4j", "TC042024")
        self.fake = Faker(['es_ES', 'es_CO', 'es_MX', 'en_US'])

    def cantidad_usuarios(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(u:User)
                RETURN u
                """,
                database_="neo4j",
            )
        return len(summary.records)
    
    def cantidad_productos(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(p:Product)
                RETURN p
                """,
                database_="neo4j",
            )
        return len(summary.records)

    def insertar_usuario(self, nombre, correo, id):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                "CREATE (:User {name: $name, user_id: $id, email: $email})",
                name=nombre,
                id=id,
                email=correo,
                database_="neo4j",
            ).summary

    def generar_usuarios(self, n):
        for id in range(n):
            self.insertar_usuario(self.fake.first_name(), self.fake.email(), id)
    
    def insertar_producto(self, nombre, categoria, id):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                "CREATE (:Product {name: $name, product_id: $id, category: $categoria})",
                name=nombre,
                id=id,
                categoria=categoria,
                database_="neo4j",
            ).summary

    def generar_productos(self, n):
        categorias = ['Phone', 'Laptop', 'Tablet', 'Headphones', 'Camera', 'Watch', 'Speaker', 'Printer', 'Router', 'TV']
        adjetivos = ['Smart', 'Eco', 'Pro', 'Ultra', 'Mini', 'Max', 'Quick', 'Super', 'Fast', 'Premium']
        for id in range(n):
            self.insertar_producto(self.fake.company() + " " + adjetivos[self.fake.random_int(min=0,max=9)], categorias[self.fake.random_int(min=0,max=9)], id)
        
    def eliminar_usuarios(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH (n:User)
                DELETE n
                """,
                database_="neo4j",
            ).summary
    
    def eliminar_productos(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH (n:Product)
                DELETE n
                """,
                database_="neo4j",
            ).summary
    
    def eliminar_transacciones(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH (n:Transaction)
                DELETE n
                """,
                database_="neo4j",
            ).summary

    def eliminar_seguir(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH (n:User)-[r:FOLLOWS]->(m:User)
                DELETE r
                """,
                database_="neo4j",
            ).summary

    def eliminar_purchased(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(u:User)-[r:PURCHASED]->(v:Transaction)-[w:PURCHASED]->(x:Product)
                DELETE r,w
                """,
                database_="neo4j",
            ).summary

    def eliminar_reviewed(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(u:User)-[r:REVIEWED]->(x:Product)
                DELETE r
                """,
                database_="neo4j",
            ).summary
    
    def eliminar_reviewed(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(u:User)-[r:REVIEWED]->(x:Product)
                DELETE r
                """,
                database_="neo4j",
            ).summary
    
    def purchased(self, user_id, product_id, quantity, timestamp, transaction_id):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                "CREATE (:Transaction {transaction_id: $transaccion_id, quantity: $cantidad, timestamp: date($fecha)})",
                transaccion_id = transaction_id,
                cantidad = quantity,
                fecha = timestamp,
                database_="neo4j",
            ).summary
            summary = driver.execute_query(
                """
                MATCH(u:User {user_id: $id_usuario}), (p:Product {product_id: $id_producto}), (t: Transaction {transaction_id: $id_transaccion})
                CREATE(u)-[:PURCHASED]->(t)
                CREATE(t)-[:PURCHASED]->(p)
                """,
                id_usuario = user_id,
                id_producto = product_id,
                id_transaccion = transaction_id,
                database_="neo4j",
            ).summary

    def follows(self, user_id_1, user_id_2): 
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(u1:User {user_id: $user1}), (u2:User {user_id: $user2})
                CREATE(u1)-[:FOLLOWS]->(u2)
                """,
                user1 = user_id_1,
                user2 = user_id_2,
                database_="neo4j",
            ).summary

    def reviewed(self, user_id, product_id):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(u:User {user_id: $user}), (p:Product {product_id: $product})
                CREATE(u)-[:REVIEWED]->(p)
                """,
                user = user_id,
                product = product_id,
                database_="neo4j",
            ).summary

    def mas_comprados_por_categoria(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH (t:Transaction)-[c:PURCHASED]->(p:Product)
                WHERE t.timestamp >= date() - duration('P30D') 
                RETURN p.category AS Categoria, p.name AS Producto, COUNT(t) AS Cantidad
                ORDER BY Categoria, Cantidad DESC
                """,
                database_="neo4j"
            )
        res = summary.records

        for comunidad in res:
            data = comunidad.data()
            print(f'El producto {data["Producto"]}, de la categoría {data["Categoria"]}, ha sido comprado {data["Cantidad"]} veces')

    def mas_influyente(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(u:User)<-[f:FOLLOWS]-()
                RETURN u.name AS Usuario, COUNT(f) AS Numero_seguidores
                ORDER BY Numero_seguidores desc
                """,
                database_="neo4j"
            )
        res = summary.records

        for comunidad in res:
            data = comunidad.data()
            print(f'El usuario {data["Usuario"]} tiene {data["Numero_seguidores"]} seguidores')

    def mejor_calificados(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH (u:User)-[c:REVIEWED]->(p:Product)
                RETURN p.name AS Producto, COUNT(c) AS Cantidad_calificaciones, COLLECT(u.name) AS Usuarios
                ORDER BY Cantidad_calificaciones DESC
                """,
                database_="neo4j"
            )
        res = summary.records
        
        for comunidad in res:
            data = comunidad.data()
            if data["Cantidad_calificaciones"] == 1:
                cal = "calificación"
            else:
                cal = "calificaciones"
            print(f'El producto {data["Producto"]} tiene {data["Cantidad_calificaciones"]} {cal} de estos usuarios: {data["Usuarios"]}')

    def comunidades(self):
        with GraphDatabase.driver(uri=self.URI, auth=self.AUTH) as driver:
            summary = driver.execute_query(
                """
                MATCH(u:User)-[s:PURCHASED]->(t:Transaction)-[r:PURCHASED]->(p:Product)
                RETURN p.name AS Producto, COLLECT(DISTINCT u.name) AS Comunidad
                """,
                database_="neo4j"
            )
        res = summary.records

        for comunidad in res:
            data = comunidad.data()
            print(f'El producto {data["Producto"]} tiene la comunidad: {data["Comunidad"]}')

    
    