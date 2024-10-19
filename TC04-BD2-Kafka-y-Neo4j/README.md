# Mensajería con Kafka y Neo4J

## Autores
- Steven Sequeira 
- Brayton Solano
- Julian Madrigal

## Instrucciones

### 1. Construir el docker-compose 
Desde una terminal que este al mismo nivel que el proyecto ejecute:
``` bash
docker-compose up --build 
```

### 2. Correr el productor 
Desde una terminal que este al mismo nivel que el proyecto ejecute:
``` bash
python producer.py
```

### 3. Correr el consumidor
Desde una terminal que este al mismo nivel que el proyecto ejecute: 
``` bash
python consumer.py
```

### 4. Llamar a las consultas de prueba
Desde el archivo <test.ipynb> ejecute cada uno de las pruebas. 