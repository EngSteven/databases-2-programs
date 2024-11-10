CREATE DATABASE database;

\c database

CREATE TABLE Total_Spent_Per_Customer (
    customer_id INT PRIMARY KEY,   -- ID único del cliente
    total_spent DECIMAL(10, 2)     -- total gastado por el cliente (con 2 decimales)
);

CREATE TABLE Product_Purchase_Count (
    product_id INT PRIMARY KEY,    -- ID único del producto
    purchase_count INT             -- número de veces que el producto ha sido comprado
);

CREATE TABLE Average_Spend_Per_Customer (
    customer_id INT PRIMARY KEY,   -- ID único del cliente
    average_spent DECIMAL(10, 2)   -- gasto promedio por cliente (con 2 decimales)
);

CREATE TABLE Transaction_Count_Per_Customer (
    customer_id INT PRIMARY KEY,   -- ID único del cliente
    transaction_count INT          -- número de transacciones realizadas por el cliente
);

