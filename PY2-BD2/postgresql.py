import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# configuración de la conexión a PostgreSQL
POSTGRESQL_URL = "postgresql://user:password@localhost:5432/database"

# función para crear la conexión a PostgreSQL
def create_postgresql_engine():
    """Crea y retorna un motor de conexión a PostgreSQL."""
    return create_engine(POSTGRESQL_URL)

# función para obtener datos desde PostgreSQL
def fetch_data(query, engine):
    """
    Ejecuta una consulta SQL y retorna los resultados como un DataFrame de pandas.
    :param query: Consulta SQL.
    :param engine: Motor de conexión a PostgreSQL.
    """
    return pd.read_sql(query, engine)

# función para generar un gráfico de barras
def create_bar_chart(x, y, title, xlabel, ylabel, filename, color="skyblue"):
    """
    Genera un gráfico de barras y lo guarda como imagen.
    :param x: Datos para el eje x.
    :param y: Datos para el eje y.
    :param title: Título del gráfico.
    :param xlabel: Etiqueta del eje x.
    :param ylabel: Etiqueta del eje y.
    :param filename: Nombre del archivo de salida.
    :param color: Color de las barras.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# función para procesar y generar gráficos
def generate_total_spent_chart(engine):
    """Genera el gráfico de gasto total por cliente."""
    query = "SELECT * FROM total_spent_per_customer"
    data = fetch_data(query, engine)
    create_bar_chart(
        x=data["customer_id"],
        y=data["total_spent"],
        title="Gasto Total por Cliente",
        xlabel="ID Cliente",
        ylabel="Gasto Total",
        filename="gasto_total_por_cliente.png",
        color="skyblue"
    )

def generate_product_purchase_chart(engine):
    """Genera el gráfico de productos más comprados."""
    query = "SELECT * FROM product_purchase_count"
    data = fetch_data(query, engine).sort_values(by="purchase_count", ascending=False)
    create_bar_chart(
        x=data["product_id"],
        y=data["purchase_count"],
        title="Productos Más Comprados",
        xlabel="ID Producto",
        ylabel="Cantidad Comprada",
        filename="productos_mas_comprados.png",
        color="orange"
    )

def generate_average_spent_chart(engine):
    """Genera el gráfico de gasto promedio por cliente."""
    query = "SELECT * FROM average_spent_per_customer"
    data = fetch_data(query, engine)
    create_bar_chart(
        x=data["customer_id"],
        y=data["average_spent"],
        title="Gasto Promedio por Cliente",
        xlabel="ID Cliente",
        ylabel="Gasto Promedio",
        filename="gasto_promedio_por_cliente.png",
        color="green"
    )

# función principal
def main():
    """Función principal que ejecuta todo el flujo."""
    # crear conexión a PostgreSQL
    engine = create_postgresql_engine()

    # generar gráficos
    print("Generando gráficos...\n")
    generate_total_spent_chart(engine)
    generate_product_purchase_chart(engine)
    generate_average_spent_chart(engine)


