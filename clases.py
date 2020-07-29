from tkinter import *
from tkinter import ttk
import mysql.connector
from re import compile
import sys
from tkinter.messagebox import *
import tkinter.simpledialog
import json

class Database():
    conector = mysql.connector
    micursor = None
    def __init__(self):
        try:
            self.conector = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database=self.__getDbName()
            )
            self.micursor = self.conector.cursor()
        except:
            mensaje = f"Error al conectar a la Base de Datos {self.__getDbName()}"
            showerror("Error MySQL", mensaje)
            if askyesno("Error MySQL", "¿Desea Crearla?"):
                createDB(self.__getDbName())
            

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
            use = f"USE {nombre}"
            self.micursor.execute(use)
            self.__setDbName(nombre)
            mensaje = f"Se ha creado la base {self.getDbName()}"
            return mensaje
            
        except:
            return sys.exc_info()[1]


class Crud():
    #Variables
    master = Tk()

    idInteger = IntVar()
    tituloString = StringVar()
    descripcionString = StringVar()
    mostrarString = StringVar()

    verDatos = ttk.Treeview()
    conectorSQL = Database()
    
    def __init__(self):
        self.widgetSetup()
        self.iniciarEtiquetas()
        self.iniciarEntradas()
        self.iniciarTreeView()
        self.iniciarBotones()
        self.read()

    def widgetSetup(self):
        self.master.resizable(0, 0)
        self.master.iconbitmap('logo.ico')
        self.master.title("Ejercicio POO")

    def crearEtiqueta(self, texto, fuente, fila, columna, color):
        etiqueta = Label(self.master, text=texto, font=fuente)
        etiqueta.grid(row=fila, column=columna,sticky=W, padx=10)
        etiqueta.configure(bg=color)
        return etiqueta

    def iniciarEtiquetas(self):
        self.ingrese = Label(self.master, text="Ingrese sus datos", font="Arial 12", width=45)
        self.ingrese.grid(row=0, column=0, sticky=N, columnspan=5, pady=10)
        self.ingrese.configure(bg="#9a32cd")
        self.tituloLabel = self.crearEtiqueta("Título", "Arial 12", 1, 0, "#f2f2f2")
        self.descripcionLabel = self.crearEtiqueta("Descripción", "Arial 12", 2, 0, "#f2f2f2")
        self.mostrarString.set('Mostrando Registros Existentes en ' + self.conectorSQL.getDbName())
        self.tituloTree = Label(text=self.mostrarString.get(), font="Arial 10", bg="#d9d9d9")
        self.tituloTree.grid(row=3, column=0, sticky=N, columnspan=4,pady=10)

    def crearEntrada(self, master, valueForm, ancho, fila, columna):
        return Entry(self.master, width=ancho, textvariable=valueForm).grid(row=fila, column=columna, pady=10)
    
    def iniciarEntradas(self):
        tituloEntry = self.crearEntrada(self.master, self.tituloString, 30, 1, 1)
        descripcionEntry = self.crearEntrada(self.master, self.descripcionString, 30, 2, 1)

    def iniciarTreeView(self):
        self.verDatos.configure(height=10, columns=3)
        self.verDatos["columns"] = ("idbase","titulo", "descripcion")
        self.verDatos.column("#0", width=80, minwidth=20, anchor=E)
        self.verDatos.column("idbase", width=60, minwidth=20, anchor=W)
        self.verDatos.column("titulo", width=150, minwidth=150, anchor=W)
        self.verDatos.column("descripcion", width=150, minwidth=150, anchor=W)
        self.verDatos.heading("#0", text="index", anchor=CENTER)
        self.verDatos.heading("idbase", text="id", anchor=CENTER)
        self.verDatos.heading("titulo", text="Título", anchor=CENTER)
        self.verDatos.heading("descripcion", text="Descripción", anchor=CENTER)
        self.verDatos.grid(column=0, row=4, columnspan=3, rowspan=2, padx=20, pady=15)
        self.verDatos.bind("<<TreeviewSelect>>", self.selectTree)
    
    def iniciarBotones(self):
        alta = Button(self.master, text="Alta", font="Arial 10", command= self.create)
        alta.grid(row=6, column=0, pady=15)
        modificar = Button(self.master,text="Modificar", font="Arial 10",command= self.update, width="8")
        modificar.grid(row=1, column=2, rowspan=1)
        borrar = Button(self.master,text="Borrar", font="Arial 10",command= self.delete, width="8")
        borrar.grid(row=2, column=2,rowspan=1)
        crearTabla = Button(self.master,text="Crear Tabla", font="Arial 10",command=self.crearTabla, width="8")
        crearTabla.grid(row=6, column=1)
        crearBD = Button(self.master,text="Crear BD", font="Arial 10",command= self.crearBD, width="8")
        crearBD.grid(row=6, column=2)
    
    def reset(self):
        self.descripcionString.set("")
        self.tituloString.set("")

    def resetTree(self):
        for fila in self.verDatos.get_children():
            self.verDatos.delete(fila)
    
    def updateTree(self):
        self.reset()
        self.resetTree() 
        self.read()

    def selectTree(self, event):
        item = self.verDatos.selection()
        self.idInteger.set(self.verDatos.item(item)['values'][0]) 
        self.tituloString.set(self.verDatos.item(item)['values'][1])   
        self.descripcionString.set(self.verDatos.item(item)['values'][2])
        
    def create(self):
        data = (self.tituloString.get(), self.descripcionString.get())
        if self.validarRE(data[0]):
            if askyesno('Confirma', '¿Desea confirmar el Alta?'):
                rows = self.conectorSQL.insertData(data)
                mensaje = "Se cargó " + str(rows) + " registro."
                showinfo('Resultado', mensaje)
                self.updateTree()
                
        else:
            error_msg = data[0] + " no es válido."
            showerror("Error en el ingreso", error_msg)
             
    def read(self):
        datos = self.conectorSQL.fetchall()
        for i in range(len(datos)):
            self.verDatos.insert('', i+1, text = i+1, values = (datos[i][0], datos[i][1], datos[i][2]))

    def update(self):
        data = (self.tituloString.get(),self.descripcionString.get(),self.idInteger.get())
        if self.validarRE(data[0]):
            if askyesno('Confirma', '¿Desea confirmar la modificación?'):
                rows = self.conectorSQL.updateData(data)
                mensaje = "Se actualizó " + str(rows) + " registro."
                showinfo('Resultado', mensaje)
                self.updateTree()
        else:
            error_msg = data[0] + " no es válido."
            showerror("Error en el ingreso", error_msg)
    
    def delete(self):
        data = (self.idInteger.get(),)
        if askyesno('Confirma', '¿Desea eliminar el registro?'):
            rows = self.conectorSQL.deleteData(data)
            mensaje = "Se eliminó " + str(rows) + " registro."
            showinfo('Resultado', mensaje)
            self.updateTree()
        
    def crearTabla(self):
        mensaje = self.conectorSQL.createTable()
        showinfo('Resultado', mensaje)

    def crearBD(self):
        mensaje = "Usted ya se encuentra conectado a la base " + self.conectorSQL.getDbName() + ", ¿Desea Crear una nueva?"
        if askyesno("Atención", mensaje):
            nombre = tkinter.simpledialog.askstring("Elija el Nombre de la Base", prompt="Nombre")
            resultado = self.conectorSQL.createDB(nombre)
            showinfo('Resultado', resultado)
            self.crearTabla()
            print(self.conectorSQL.getDbName())
            self.mostrarString.set('Mostrando Registros Existentes en ' + self.conectorSQL.getDbName())
            self.tituloTree.configure(text=self.mostrarString.get())
            self.updateTree()
            
    def validarRE(self, datoAValidar):
        patron = compile("^[A-Za-z]+(?:[ _-][A-Za-z]+)*$")  
        return patron.match(datoAValidar)




test = Crud()


mainloop()