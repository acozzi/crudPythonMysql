import mysql.connector
def conectarBase():
        return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="PYTHON_INTERMEDIO"
        )