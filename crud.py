from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, askyesno
from validar import validarTitulo
import tkinter.simpledialog
from sys import exc_info
from db import Database


class Crud():
    def __init__(self):
        self.master = Tk()
        self.idInteger = IntVar()
        self.checkStatus1 = BooleanVar()
        self.checkStatus1.set(True)
        self.checkStatus2 = BooleanVar()
        self.checkStatus3 = BooleanVar()
        self.tituloString = StringVar()
        self.descripcionString = StringVar()
        self.mostrarString = StringVar()
        self.base = Database()
        self.verDatos = ttk.Treeview()
        self.widgetSetup()
        self.iniciarEtiquetas()
        self.iniciarEntradas()
        self.iniciarTreeView()
        self.iniciarBotones()
        self.crearChecks()
        self.read()
    def widgetSetup(self):
        self.master.resizable(0, 0)
        self.master.iconbitmap('logo.ico')
        self.master.title("Ejercicio POO")

        self.master.bind("<Return>", lambda e: self.create())
        self.master.bind("<Delete>", lambda e: self.delete())
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
        self.mostrarString.set('Mostrando Registros Existentes en ' + str(self.base.getDbName()))
        self.tituloTree = Label(text=self.mostrarString.get(), font="Arial 10", bg="#d9d9d9")
        self.tituloTree.grid(row=3, column=0, sticky=N, columnspan=4,pady=10)
    def crearChecks(self):
        check1 = Checkbutton(self.master, text="Tema 1", variable=self.checkStatus1, command= self.updateCheck)
        check1.grid(row=7, column=1)
        check2 = Checkbutton(self.master, text="Tema 2", variable=self.checkStatus2, command= self.updateCheck)
        check2.grid(row=8, column=1)
        check3 = Checkbutton(self.master, text="Tema 3", variable=self.checkStatus3, command= self.updateCheck)
        check3.grid(row=9, column=1)
    def updateCheck(self):
        if (self.checkStatus1.get() == True):
            self.master.configure(background='#f5f5f0')
            self.checkStatus2.set(False)
            self.checkStatus3.set(False)

        elif (self.checkStatus2.get() == True):
            self.master.configure(background='#ff99ff')
            self.checkStatus3.set(False)
            self.checkStatus1.set(False)
        elif (self.checkStatus3.get() == True):
            self.master.configure(background='#00ff00')
            self.checkStatus1.set(False)
            self.checkStatus2.set(False)


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
                rows = self.base.insertData(data)
                mensaje = "Se cargó " + str(rows) + " registro."
                showinfo('Resultado', mensaje)
                self.updateTree()       
        else:
            error_msg = data[0] + " no es válido."
            showerror("Error en el ingreso", error_msg)        
    def read(self):
        try:
            datos = self.base.readData()
            for i in range(len(datos)):
                self.verDatos.insert('', i+1, text = i+1, values = (datos[i][0], datos[i][1], datos[i][2]))
        except:
            showerror("Error", exc_info()[1])
    def update(self):
        data = (self.tituloString.get(),self.descripcionString.get(),self.idInteger.get())
        if self.validarRE(data[0]):
            if askyesno('Confirma', '¿Desea confirmar la modificación?'):
                rows = self.base.updateData(data)
                mensaje = "Se actualizó " + str(rows) + " registro."
                showinfo('Resultado', mensaje)
                self.updateTree()
        else:
            error_msg = data[0] + " no es válido."
            showerror("Error en el ingreso", error_msg)
    def delete(self):
        data = (self.idInteger.get(),)
        if askyesno('Confirma', '¿Desea eliminar el registro?'):
            rows = self.base.deleteData(data)
            mensaje = "Se eliminó " + str(rows) + " registro."
            showinfo('Resultado', mensaje)
            self.updateTree()     
    def crearTabla(self):
        mensaje = self.base.createTable()
        showinfo('Resultado', mensaje)
    def crearBD(self):
        if self.base.isConnected():
            mensaje = "Usted ya se encuentra conectado a la base " + self.base.getDbName() + ", ¿Desea Crear una nueva?"
            if askyesno("Atención", mensaje):
                nombre = tkinter.simpledialog.askstring("Elija el Nombre de la Base", prompt="Nombre")
                self.base.setDbName(nombre)
                resultado = self.base.createDB()
                showinfo('Resultado', resultado)
                self.crearTabla()
                self.mostrarString.set('Mostrando Registros Existentes en ' + self.base.getDbName())
                self.tituloTree.configure(text=self.mostrarString.get())
                self.updateTree()
        else:
            try:
                mibase = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password=""
                )
                baseNombre['nombre'] = tkinter.simpledialog.askstring("Elija el Nombre de la Base", prompt="Nombre")
                buffer = open('nombreBD.json', 'w')
                buffer.write(json.dumps(baseNombre))
                buffer.close()        
                micursor = mibase.cursor()
                baseSQL = f"CREATE DATABASE {getNameDB()}"
                micursor.execute(baseSQL)
                mensaje = f"Se ha creado la base {getNameDB()}"
                showinfo('BD Creada', mensaje)
                mostrarString.set('Mostrando Registros Existentes en ' + getNameDB())
                tituloTree.configure(text=mostrarString.get())

                if askyesno('Tabla Inexistente', '¿Desea crear una tabla?'):
                    crearTabla()
            except:
                showinfo ('Error', exc_info()[1])          
    def validarRE(self, datoAValidar):
        return validarTitulo(datoAValidar)


if __name__ == '__main__':
    poo = Crud()
    mainloop()
