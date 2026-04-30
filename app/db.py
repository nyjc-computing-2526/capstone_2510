import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="xxx", #to be filled in
        password="xxx",
        database="capstone"
    )

CREATE DATABASE capstone;

USE capstone;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);
