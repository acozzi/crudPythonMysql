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
    def __init__(self):
        self.conector = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database=self.getDbName()
        )

    def getConector(self):
        return self.conector
    
    def getDbName(self):
        try:
            buffer = open('nombreBD.json', 'r')
            baseNombre = json.load(buffer)
            buffer.close()
            return baseNombre['nombre']
        except:
            showerror ("Error al abrir el archivo", error_msg)

class Crud():
    #Variables
    master = Tk()
    idInteger = IntVar()
    tituloString = StringVar()
    descripcionString = StringVar()
    mostrarString = StringVar()
    verDatos = ttk.Treeview(height=10, columns=3)
    conectorSQL = Database()
    
    def __init__(self):
        self.widgetSetup()
        self.iniciarEtiquetas()
        self.iniciarEntradas()
        self.iniciarTreeView()
        self.iniciarBotones()
        

    def widgetSetup(self):
        self.master.resizable(0, 0)
        self.master.iconbitmap('logo.ico')
        self.master.title("Ejercicio POO")

    def crearEtiqueta(self, widget, texto, fuente, fila, columna, color):
        etiqueta = Label(widget, text=texto, font=fuente)
        etiqueta.grid(row=fila, column=columna,sticky=W, padx=10)
        etiqueta.configure(bg=color)
        return etiqueta

    def iniciarEtiquetas(self):
        ingrese = Label(self.master, text="Ingrese sus datos", font="Arial 12", width=45)
        ingrese.grid(row=0, column=0, sticky=N, columnspan=5, pady=10)
        ingrese.configure(bg="#9a32cd")
        tituloLabel = self.crearEtiqueta(self.master, "Título", "Arial 12", 1, 0, "#f2f2f2")
        descripcionLabel = self.crearEtiqueta(self.master, "Descripción", "Arial 12", 2, 0, "#f2f2f2")
    
    def crearEntrada(self, master, valueForm, ancho, fila, columna):
        return Entry(self.master, width=ancho, textvariable=valueForm).grid(row=fila, column=columna, pady=10)
    
    def iniciarEntradas(self):
        tituloEntry = self.crearEntrada(self.master, self.tituloString, 30, 1, 1)
        descripcionEntry = self.crearEntrada(self.master, self.descripcionString, 30, 2, 1)

    def iniciarTreeView(self):
        pass

    def iniciarBotones(self):
        alta = Button(self.master, text="Alta", font="Arial 10", command= self.create)
        alta.grid(row=6, column=0, pady=15)

        modificar = Button(self.master,text="Modificar", font="Arial 10",command= lambda: self.update(self.verDatos,self.idInteger.get(),self.tituloString.get(), descripcionString.get()), width="8")
        modificar.grid(row=1, column=2, rowspan=1)

        borrar = Button(self.master,text="Borrar", font="Arial 10",command= lambda: self.delete(self.verDatos, self.idInteger.get(), self.tituloString.get(), self.descripcionString.get()) , width="8")
        borrar.grid(row=2, column=2,rowspan=1)

        crearTabla = Button(self.master,text="Crear Tabla", font="Arial 10",command=self.crearTabla, width="8")
        crearTabla.grid(row=6, column=1)

        crearBD = Button(self.master,text="Crear BD", font="Arial 10",command= lambda: self.crearBD(self.mostrarString, self.tituloTree), width="8")
        crearBD.grid(row=6, column=2)
    
    def reset(self):
        self.descripcionString.set("")
        self.tituloString.set("")

    def create(self):
        try:
            db = self.conectorSQL.getConector()
            micursor = db.cursor()
            if self.validarRE(self.tituloString.get()):
                registro = (self.tituloString.get(), self.descripcionString.get())
                sql = "INSERT INTO producto (titulo,descripcion) VALUES (%s,%s)"
                if askyesno ('Confirma','¿Desea confirmar el Alta?'):
                    try:
                        micursor.execute(sql,registro)
                        db.commit()
                        mensaje = "Se cargó " + str(micursor.rowcount) + " registro correctamente: " + str(registro[0])
                        showinfo('Alta Confirmada', mensaje)
                        self.reset()
                        #resetTree(tabla) # Borra la tabla
                        #query(tabla)    # Completa la tabla con el dato actualizado.
                    except:
                        showinfo ('Alta Rechazada', sys.exc_info()[1])
            else:
                error_msg = self.tituloString.get() + " no es válido."
                showerror ("Error en el ingreso", error_msg)
        except:
            showinfo ('Error con la BD', sys.exc_info()[1])

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def crearTabla(self):
        pass

    def crearBD(self):
        pass

    def validarRE(self, datoAValidar):
        patron = compile("^[A-Za-z]+(?:[ _-][A-Za-z]+)*$")  
        return patron.match(datoAValidar)




test = Crud()


mainloop()