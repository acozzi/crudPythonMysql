import mysql.connector
from sys import exc_info
from json import dumps, load
import shelve

class Database():
    def __init__(self):
        self.conector = mysql.connector
        self.micursor = None
        #self.configData = {}
        # Abrir el archivo de configuración y lo cargo en configData
        self.configData = shelve.open('config', 'r')
        try:
            self.conector = mysql.connector.connect(
                host=self.__getConfigData('host'),
                user=self.__getConfigData('user'),
                password=self.__getConfigData('password')
            )
            self.micursor = self.conector.cursor()
            self.conectarBase(self.__getConfigData('name'))
            self.configData.close()
            if not self.isConnected():
                self.createDB()
                self.createTable()
        except:
            print("Error al conectar a la base. Compruebe que el servidor esta funcionando y que los datos de acceso sean los validos.", exc_info()[1])    
    def __getConfigData(self, key):
        return str(self.configData[key])      
    def conectarBase(self, nombreBase):
            use = f"USE {nombreBase}"
            self.micursor.execute(use)   
    def getConector(self):
        return self.conector
    def getDbName(self):
        try:
            return self.conector.database
        except:
            return ("Error al obtener el nombre de la base " + str(exc_info()[1]))
    def setDbName(self, nombre):
        self.configData = shelve.open('config','w')
        self.configData['name'] = nombre
        self.configData.close()
    def readData(self):
        try:
            selectQuery = "SELECT * FROM producto"
            self.micursor.execute(selectQuery)
            return self.micursor.fetchall()
        except:
            return exc_info()[1]
    def insertData(self, data): #data = registro: tupla con 2 valores
        sqlInsert = """INSERT INTO producto (titulo,descripcion) VALUES (%s,%s)"""
        self.micursor.execute(sqlInsert, data)
        self.conector.commit()
        if self.micursor.rowcount != 0:
            return f'El registro {data[0]} ha sido creado.'
        else:
            return f'Error al crear el registro {data[0]}.'
    def updateData(self, data): #data = tit des id
        sql = """UPDATE producto SET titulo = %s, descripcion = %s WHERE producto.id = %s"""
        self.micursor.execute(sql, data)
        self.conector.commit()
        if self.micursor.rowcount != 0:
            return f'El registro {data[0]} ha sido actualizado.'
        else:
            return f'Error al actualizar el registro {id[0]}.'
    def deleteData(self, id):
        sql = """DELETE FROM producto WHERE producto.id = %s"""
        self.micursor.execute(sql, id)
        self.conector.commit()
        if self.micursor.rowcount != 0:
            return f'El registro {id[0]} ha sido eliminado.'
        else:
            return f'Error al borrar el registro {id[0]}.'
    def createTable(self):
        try:
            self.micursor.execute("CREATE TABLE producto (id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, titulo VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, descripcion TEXT COLLATE utf8_spanish2_ci NOT NULL)")
            return "Se ha creado la tabla"
        except:
            return exc_info()[1]
    def createDB(self):
        try:
            self.configData = shelve.open('config', 'r')
            nombre = self.__getConfigData('name')
            self.configData.close()
            baseSQL = f"CREATE DATABASE {nombre}"
            self.micursor.execute(baseSQL)
            self.conectarBase(nombre)
            mensaje = f"Se ha creado la base {self.getDbName()}"
            return mensaje
        except:
            return exc_info()[1]
    def isConnected(self):
        return self.conector.is_connected()
if __name__ == '__main__':
    #db = Database()
    pass
    