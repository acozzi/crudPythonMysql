# Bibliotecas
from tkinter import *
from tkinter.messagebox import *
import tkinter.simpledialog
import funciones as f
import mysql.connector
from tkinter import ttk
import json
from clases import Crud

main = Crud()
# Functions
def callAlta():
    f.altaReg(verDatos,tituloString, descripcionString)

def selectTree(event):
    item = verDatos.selection()
    idInteger.set(verDatos.item(item)['values'][0]) 
    tituloString.set(verDatos.item(item)['values'][1])   
    descripcionString.set(verDatos.item(item)['values'][2])

# Variables Declaracion
master = Tk()
idInteger = IntVar()
tituloString = StringVar()
descripcionString = StringVar()
mostrarString = StringVar()

# Configuro el Widget
master.resizable(0, 0)
master.iconbitmap('logo.ico')
master.title("Ejercicio POO")

# Labels
ingrese = Label(master, text="Ingrese sus datos", font="Arial 12", width=45)
ingrese.grid(row=0, column=0, sticky=N, columnspan=5, pady=10)
ingrese.configure(bg="#9a32cd")
tituloLabel = f.crearEtiqueta(master, "Título", "Arial 12", 1, 0, "#f2f2f2")
descripcionLabel = f.crearEtiqueta(master, "Descripción", "Arial 12", 2, 0, "#f2f2f2")

# Entrys
tituloEntry = f.crearEntrada(master, tituloString, 30, 1, 1)
descripcionEntry = f.crearEntrada(master, descripcionString, 30, 2, 1)

# TreeView Crear y configurar el objeto

mostrarString.set('Mostrando Registros Existentes en ' + f.getNameDB())
tituloTree = Label(master, text=mostrarString.get(), font="Arial 10")
tituloTree.grid(row=3, column=0, sticky=N, columnspan=4,pady=10)

verDatos = ttk.Treeview(height=10, columns=3)
verDatos["columns"] = ("idbase","titulo", "descripcion")

verDatos.column("#0", width=80, minwidth=20, anchor=E)
verDatos.column("idbase", width=60, minwidth=20, anchor=W)
verDatos.column("titulo", width=150, minwidth=150, anchor=W)
verDatos.column("descripcion", width=150, minwidth=150, anchor=W)

verDatos.heading("#0", text="index", anchor=CENTER)
verDatos.heading("idbase", text="id", anchor=CENTER)
verDatos.heading("titulo", text="Título", anchor=CENTER)
verDatos.heading("descripcion", text="Descripción", anchor=CENTER)

verDatos.grid(column=0, row=4, columnspan=3, rowspan=2, padx=20, pady=15)
verDatos.bind("<<TreeviewSelect>>", selectTree)

# Buttons
modificar = Button(master,text="Modificar", font="Arial 10",command= lambda: f.updateItem(verDatos,idInteger.get(),tituloString.get(), descripcionString.get()) , width="8")
modificar.grid(row=1, column=2, rowspan=1)

borrar = Button(master,text="Borrar", font="Arial 10",command= lambda: f.deleteItem(verDatos,idInteger.get(),tituloString.get(), descripcionString.get()) , width="8")
borrar.grid(row=2, column=2,rowspan=1)

alta = Button(master, text="Alta", font="Arial 10", command=callAlta)
alta.grid(row=6, column=0, pady=15)

crearTabla = Button(master,text="Crear Tabla", font="Arial 10",command=f.crearTabla, width="8")
crearTabla.grid(row=6, column=1)

crearBD = Button(master,text="Crear BD", font="Arial 10",command= lambda: f.crearBD(mostrarString, tituloTree), width="8")
crearBD.grid(row=6, column=2)

# Mostrar la tabla al inicio
f.query(verDatos) 

mainloop()
