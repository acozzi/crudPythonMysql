import mysql.connector
def conectarBase(baseNombre):
        return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database=baseNombre
        )