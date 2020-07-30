from tkinter import *
import mysql.connector
from sys import exc_info
from tkinter.messagebox import *
import tkinter.simpledialog
from json import dumps, load
import json

class Database():
    conector = mysql.connector
    micursor = None
    def __init__(self):
        self.conector = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        self.micursor = self.conector.cursor()
        try:    
            self.conectarBase(self.__getDbName())
        except:
            baseNombre = self.__getDbName()
            mensaje = f"No existe la base {baseNombre}"
            showerror("Error MySQL", mensaje)
            if askyesno("Error MySQL", "¿Desea Crearla?"):
                self.createDB(baseNombre)

    def conectarBase(self, nombreBase):
            use = f"USE {nombreBase}"
            self.micursor.execute(use)
            self.__setDbName(nombreBase)
            
    def getConector(self):
        return self.conector
    def __getDbName(self):
        try:
            buffer = open('config.json', 'r')
            baseNombre = json.load(buffer)
            buffer.close()
            return baseNombre['nombre']
        except:
            showerror("Error al abrir el archivo", error_msg)

    def __setDbName(self, nombre):
        # Guardo el nombre en el archivo
        buffer = open('config.json', 'r')
        baseJson = json.load(buffer)
        buffer.close()
        baseJson['nombre'] = nombre
        buffer = open('config.json', 'w')
        buffer.write(json.dumps(baseJson))
        buffer.close()

    def getDbName(self):
        try:
            return self.conector.database
        except:
            return "Error al obtener el nombre de la base " + str(sys.exc_info()[1])

    def fetchall(self):
        selectQuery = "SELECT * FROM producto"
        self.micursor.execute(selectQuery)
        return self.micursor.fetchall()

    def insertData(self, data): #data = registro: tupla con 2 valores
        sql = """INSERT INTO producto (titulo,descripcion) VALUES (%s,%s)"""
        self.micursor.execute(sql, data)
        self.conector.commit()
        return self.micursor.rowcount
    def updateData(self, data): #data = registro: tupla con 3 valores
        sql = """UPDATE producto SET titulo = %s, descripcion = %s WHERE producto.id = %s"""
        self.micursor.execute(sql, data)
        self.conector.commit()
        return self.micursor.rowcount
    
    def deleteData(self, data):
        sql = """DELETE FROM producto WHERE producto.id = %s"""
        self.micursor.execute(sql, data)
        self.conector.commit()
        return self.micursor.rowcount

    def createTable(self):
        try:
            self.micursor.execute("CREATE TABLE producto (id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, titulo VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, descripcion TEXT COLLATE utf8_spanish2_ci NOT NULL)")
            return "Se ha creado la tabla"
        except:
            return sys.exc_info()[1]
    def createDB(self, nombre):
        try:
            baseSQL = f"CREATE DATABASE {nombre}"
            self.micursor.execute(baseSQL)
            self.createTable()
            self.conectarBase(nombre)
            mensaje = f"Se ha creado la base {self.getDbName()}"
            return mensaje
            
        except:
            return sys.exc_info()[1]
