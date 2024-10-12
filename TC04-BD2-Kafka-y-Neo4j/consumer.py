from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'purchases', 'user_connections', 'product_interactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    print(f"Topic: {message.topic}, Data: {message.value}")
