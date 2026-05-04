import os
import psycopg

URL = os.getenv("DB_URL")

def get_db():
    return psycopg.connect(URL)

"""
CREATE DATABASE capstone;

USE capstone;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);
"""