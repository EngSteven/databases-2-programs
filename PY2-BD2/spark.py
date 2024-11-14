from pyspark.sql import SparkSession
def  create_spark_session():  
    spark = SparkSession.builder \
        .appName("Neo4J_Spark_Project") \
        .config("spark.jars.packages", "org.neo4j:neo4j-connector-apache-spark_2.12:5.3.2_for_spark_3") \
        .config("neo4j.url", "neo4j://localhost:7687") \
        .config("neo4j.authentication.basic.username", "neo4j") \
        .config("neo4j.authentication.basic.password", "12345678") \
        .getOrCreate()
    return spark

# Ejemplo: Leer datos de Neo4J
def load_data_from_neo4j(spark, query):
    transactions_df = spark.read \
        .format("org.neo4j.spark.DataSource") \
        .option("query", query) \
        .load()
    return transactions_df

def calculate_total_spent(transactions_df):
    """
    Calcula el gasto total por cliente.
    """
    return transactions_df.groupBy("customer_id") \
        .sum("transaction_amount") \
        .withColumnRenamed("sum(transaction_amount)", "total_spent")

def calculate_product_purchase_count(transactions_df):
    """
    Calcula la cantidad de veces que cada producto ha sido comprado.
    """
    return transactions_df.groupBy("product_id") \
        .count() \
        .withColumnRenamed("count", "purchase_count")

def calculate_average_spent(transactions_df):
    """
    Calcula el gasto promedio por cliente.
    """
    return transactions_df.groupBy("customer_id") \
        .avg("transaction_amount") \
        .withColumnRenamed("avg(transaction_amount)", "average_spent")

def calculate_transaction_count(transactions_df):
    """
    Calcula la frecuencia de compra (número de transacciones) por cliente.
    """
    return transactions_df.groupBy("customer_id") \
        .count() \
        .withColumnRenamed("count", "transaction_count")

def save_to_postgresql(df, table_name, url="jdbc:postgresql://localhost:5432/db", user="user", password="password"):
    """
    Guarda un DataFrame en una tabla de PostgreSQL.
    """
    df.write \
        .format("jdbc") \
        .option("url", url) \
        .option("dbtable", table_name) \
        .option("user", user) \
        .option("password", password) \
        .save()

def main():
    spark = create_spark_session()
     # definir consultas Cypher
    transaction_query = """
    MATCH (c:Customer)-[r:PURCHASED]->(p:Product)
    RETURN c.customer_id AS customer_id, p.product_id AS product_id, r.transaction_amount AS transaction_amount
    """
    
    # cargar datos desde Neo4j
    transactions_df = load_data_from_neo4j(spark, transaction_query)
    print("Datos extraidos de Neo4j\n")
    transactions_df.show()

    # calcular métricas
    total_spent_per_customer = calculate_total_spent(transactions_df)
    product_purchase_count = calculate_product_purchase_count(transactions_df)
    average_spent_per_customer = calculate_average_spent(transactions_df)
    transaction_count_per_customer = calculate_transaction_count(transactions_df)

    # mostrar resultados
    print("\nResultado del procesamiento de datos en Spark:")
    print("\nTotal Spent per Customer:")
    total_spent_per_customer.show()
    print("\nProduct Purchase Count:")
    product_purchase_count.show()
    print("\nAverage Spent per Customer:")
    average_spent_per_customer.show()
    print("\nTransaction Count per Customer:")
    transaction_count_per_customer.show()

    # guardar resultados en PostgreSQL
    save_to_postgresql(total_spent_per_customer, "Total_Spent_Per_Customer")
    save_to_postgresql(product_purchase_count, "Product_Purchase_Count")
    save_to_postgresql(average_spent_per_customer, "Average_Spend_Per_Customer")
    save_to_postgresql(transaction_count_per_customer, "Transaction_Count_Per_Customer")
