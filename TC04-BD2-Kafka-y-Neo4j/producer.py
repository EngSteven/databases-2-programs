from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

"""
Los rangos de los id escogidos aleatoriamente deben ser definidos segun la cantidad de 
datos que haya en la base de neo4j
"""

def send_purchase_event():
    event = {
        'user_id': random.randint(1, 100),
        'product_id': random.randint(1, 1000),
        'quantity': random.randint(1, 5),
        'timestamp': time.time()
    }
    producer.send('purchases', event)

def send_user_connection_event():
    event = {
        'follower_id': random.randint(1, 100),
        'followed_id': random.randint(1, 100),
        'timestamp': time.time()
    }
    producer.send('user_connections', event)

def send_product_interaction_event():
    event = {
        'user_id': random.randint(1, 100),
        'product_id': random.randint(1, 1000),
        'interaction': random.choice(['review', 'rating']),
        'timestamp': time.time()
    }
    producer.send('product_interactions', event)

# Enviar eventos aleatorios
while True:
    send_purchase_event()
    send_user_connection_event()
    send_product_interaction_event()
    time.sleep(5)
