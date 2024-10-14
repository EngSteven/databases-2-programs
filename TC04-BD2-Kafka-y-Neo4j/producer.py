from kafka import KafkaProducer
from database import Database
import json
import time
import datetime
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

db = Database()
CANT_USERS = 100
CANT_PRODUCTS = 1000
i = 1

"""
Los rangos de los id escogidos aleatoriamente deben ser definidos segun la cantidad de 
datos que haya en la base de neo4j
"""

def send_purchase_event(id):
    user_id = random.randint(1, CANT_USERS)
    product = random.randint(1, CANT_PRODUCTS)
    quantity = random.randint(1, 5)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    event = {
        'user_id': user_id,
        'product_id': product,
        'quantity': quantity,
        'timestamp': timestamp
    }
    producer.send('purchases', event)
    db.purchased(user_id, product, quantity, timestamp, id)

def send_user_connection_event():
    user_id = random.randint(1, CANT_USERS)
    user_id_2 = random.randint(1, CANT_USERS)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    event = {
        'follower_id': user_id,
        'followed_id': user_id_2,
        'timestamp': timestamp
    }
    producer.send('user_connections', event)
    db.follows(user_id, user_id_2)

def send_product_interaction_event():
    user_id = random.randint(1, CANT_USERS)
    product = random.randint(1, CANT_PRODUCTS)
    interaction = random.randint(1, 5)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    event = {
        'user_id': user_id,
        'product_id': product,
        'interaction': interaction,
        'timestamp': timestamp
    }
    producer.send('product_interactions', event)
    db.reviewed(user_id, product)


#Crear usuarios y productos si no se han creado
if db.cantidad_usuarios() == 0 and db.cantidad_productos() == 0:
    db.generar_usuarios(CANT_USERS)
    db.generar_productos(CANT_PRODUCTS)

# Enviar eventos aleatorios
while True:
    send_purchase_event(i)
    send_user_connection_event()
    send_product_interaction_event()
    time.sleep(1)
    i += 1

#Querys solicitadas
db.mas_comprados_por_categoria()
print("\n")
db.mas_influyente()
print("\n")
db.mejor_calificados()
print("\n")
db.comunidades()

