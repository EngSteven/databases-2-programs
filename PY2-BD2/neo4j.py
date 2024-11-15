import pandas as pd
from py2neo import Graph

# Constantes para la configuración y credenciales
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"

def connect_to_neo4j(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD):
    """
    Establece la conexión con la base de datos Neo4J.
    """
    return Graph(uri, auth=(user, password))

def create_index_if_not_exists(graph, label, property_name):
    """
    Crea un índice en una etiqueta y propiedad específica si aún no existe.
    """
    # usar SHOW INDEXES para buscar un índice existente
    index_query = f"""
    SHOW INDEXES YIELD entityType, labelsOrTypes, properties, state
    WHERE entityType = 'NODE' AND '{label}' IN labelsOrTypes AND '{property_name}' IN properties AND state = 'ONLINE'
    RETURN count(*) > 0 AS indexExists
    """
    index_exists = graph.run(index_query).evaluate()
    
    # crear el índice si no existe
    if not index_exists:
        graph.run(f"CREATE INDEX FOR (n:{label}) ON (n.{property_name})")

def load_data_to_neo4j(graph, file_path):
    df = pd.read_excel(file_path)

    # crear índices si no existen
    create_index_if_not_exists(graph, "Customer", "customer_id")
    create_index_if_not_exists(graph, "Product", "product_id")

    # convertir el DataFrame a una lista de diccionarios
    transactions = df.to_dict(orient="records")

    # crear nodos y relaciones usando UNWIND para cargar en un solo paso
    query = """
    UNWIND $transactions AS t
    MERGE (c:Customer {customer_id: t.customer_id})
    MERGE (p:Product {product_id: t.product_id})
    CREATE (c)-[:PURCHASED {transaction_amount: t.list_price, transaction_date: t.transaction_date}]->(p)
    """

    graph.run(query, transactions=transactions)

def main(file_path):
    graph = connect_to_neo4j()
    load_data_to_neo4j(graph, file_path)
