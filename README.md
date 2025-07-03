# Trabajos cortos y Proyecto 2 de bases de datos 2 (Manejo de datos con Spark).

# Autores
- Steven Sequeira 
- Brayton Solano
- Julian Madrigal

# Índice

1. [Introducción](#introducción)
2. [Instrucciones](#instrucciones)
2. [Informe](#informe)

# Introducción

En este proyecto se llevó a cabo una integración de datos utilizando Neo4j, Spark y SQL para analizar patrones de transacción y gasto de clientes. Se utilizó el Customer Transaction Dataset de Kaggle, que contiene información detallada sobre transacciones en una tienda. Neo4j se empleó para almacenar y consultar los datos de manera eficiente, Spark para procesar grandes volúmenes de información, y SQL para estructurar y visualizar los resultados obtenidos. Este enfoque permitió realizar un análisis exhaustivo de los datos, combinando diversas herramientas y técnicas de análisis.

# Instrucciones

## Preparición del entorno
### 1. Debe tener instalado en su máquina java 8 o 11. 
En caso de no tener java instalado siga los siguientes pasos, de lo contrario, puede pasar a la siguiente sección.

#### 1.1 Escoger una de las siguientes versiones de java:

- [java 8](https://www.oracle.com/java/technologies/downloads/#java11?er=221886)

- [java 11](https://www.oracle.com/java/technologies/downloads/#java8)

#### 1.2 Ejecuta el archivo .exe descargado y sigue las instrucciones en pantalla para instalarlo.

#### 1.3 Configurar Variables de Entorno:

- Ve a Configuración avanzada del sistema > Variables de entorno.
- Agrega JAVA_HOME apuntando a la ruta de instalación del JDK (por ejemplo, C:\ProgramFiles\Java\jdk-11).
- En la variable Path, agrega %JAVA_HOME%\bin para que el sistema pueda encontrar los ejecutables de Java.

### 2. Descargar e instalar hadoop
- Copie la carpeta llamada **hadoop** ubicada en este proyecto y peguela en su equipo. La ruta debe quedar así: **C:\hadoop\bin** con un archivo .exe dentro de la carpeta.
- Cree una nueva variable de sistema llamada **HADOOP_HOME** y coloque **C:\hadoop** en el valor de la variable.
- Agregue **C:\hadoop\bin** a la variable de entorno Path.

## Pasos para ejecutar el proyecto.

### 1. Construir el docker-compose 
Desde una terminal que este al mismo nivel que el proyecto ejecute:
``` bash
docker-compose up --build 
```

### 2. Ejecutar los scripts de prueba  
Una vez se construido el contenedor, vaya al notebook **test.ipynb**, seguidamente ejecute cada uno de los bloques de código siguiendo el orden de ejecución del notebook.

# Informe 

## Carga de datos en Neo4j

### 1. Conexión con Neo4j

Se estableció una conexión a la base de datos Neo4j, creada con un servicio de docker, utilizando el protocolo bolt mediante la biblioteca py2neo. 

### 2. Creación de índices
Antes de cargar los datos, se verificó si existían índices en las etiquetas Customer y Product para las propiedades customer_id y product_id, respectivamente.  

En caso de que no existieran, se crearon los índices, usando:

``` bash
CREATE INDEX FOR (n:Label) ON (n.property)
```

### 3. Preparación de datos

Los datos se cargaron desde un archivo Excel utilizando la biblioteca pandas, convirtiendo el contenido en una lista de diccionarios (records). Cada registro representaba una transacción con detalles del cliente, producto, precio y fecha.

### 4. Carga de Datos en Neo4j:
Para insertar los datos, se utilizó una consulta Cypher optimizada con UNWIND. Este comando permite iterar sobre los registros de manera eficiente y crear nodos y relaciones.

``` bash
UNWIND $transactions AS t
MERGE (c:Customer {customer_id: t.customer_id})
MERGE (p:Product {product_id: t.product_id})
CREATE (c)-[:PURCHASED {transaction_amount: t.list_price, transaction_date: t.transaction_date}]->(p)
```

## Análisis de datos con PySpark

### 1. Creación de la sesión de Spark

La función create_spark_session inicializa una sesión Spark configurada con los conectores para Neo4j y PostgreSQL. Esto permite:

- Leer datos de Neo4j utilizando consultas Cypher.
- Guardar resultados procesados en PostgreSQL.


### 2. Extracción de Datos desde Neo4j

La función load_data_from_neo4j ejecuta una consulta Cypher para extraer datos de las relaciones PURCHASED entre clientes y productos.
Consulta utilizada:

``` bash
MATCH (c:Customer)-[r:PURCHASED]->(p:Product)
RETURN c.customer_id AS customer_id, p.product_id AS product_id, r.transaction_amount AS transaction_amount
```

### 3. Cálculos Realizados
- **Gasto Total por Cliente:**
La función calculate_total_spent agrupa las transacciones por customer_id y calcula la suma de los montos de transacción (transaction_amount).

``` bash
return transactions_df.groupBy("customer_id") \
    .sum("transaction_amount") \
    .withColumnRenamed("sum(transaction_amount)", "total_spent")
```

- **Cantidad de Compras por Producto:**
La función calculate_product_purchase_count cuenta el número de veces que cada producto fue comprado agrupando el product_id.

``` bash
return transactions_df.groupBy("product_id") \
    .count() \
    .withColumnRenamed("count", "purchase_count")
```

- **Gasto Promedio por Cliente:**
La función calculate_average_spent calcula el promedio de los montos de transacción por cliente.
``` bash
return transactions_df.groupBy("customer_id") \
    .avg("transaction_amount") \
    .withColumnRenamed("avg(transaction_amount)", "average_spent")
```

- **Frecuencia de Compra por Cliente:**

La función calculate_transaction_count cuenta la cantidad de transacciones realizadas por cada cliente.
``` bash
return transactions_df.groupBy("customer_id") \
    .count() \
    .withColumnRenamed("count", "transaction_count")
```

### 4. Almacenamiento en PostgreSQL

Los resultados procesados se guardan en PostgreSQL mediante la función save_to_postgresql. Cada DataFrame se escribe en una tabla específica utilizando el conector JDBC.

``` bash
df.write \
    .format("jdbc") \
    .option("url", url) \
    .option("dbtable", table_name) \
    .option("user", user) \
    .option("password", password) \
    .option("driver", "org.postgresql.Driver") \
    .save()
```

## Resultados en PostgreSQL

### Gasto total por cliente

![alt text](images/total_spend.png)

### Cantidad de compras por producto

![alt text](images/purchase_count.png)

### Gasto promedio por cliente

![alt text](images/average_spend.png)

### Frecuencia de compra por cliente

![alt text](images/transaction_count.png)

## Visualización de resultados 

![alt text](images/graphics/total_spend.png)
![alt text](images/graphics/purchase_count.png)
![alt text](images/graphics/average_spend.png)
