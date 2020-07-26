from tkinter import *
from tkinter.messagebox import *
import tkinter.simpledialog
import mysql.connector
from sqlConnect import conectarBase
from validar import validar

baseNombre = "PYTHON"

def crearEtiqueta(widget, texto, fuente, fila, columna, color):
    etiqueta = Label(widget, text=texto, font=fuente)
    etiqueta.grid(row=fila, column=columna,sticky=W, padx=10)
    etiqueta.configure(bg=color)
    return etiqueta
    
def crearEntrada(widget, valueForm, ancho, fila, columna):
    return Entry(widget, width=ancho, textvariable=valueForm).grid(row=fila, column=columna, pady=10)

def reset(titulo, descripcion):
    descripcion.set("")
    titulo.set("")

def altaReg(tabla,titulo, descripcion):
    try:
        db = conectarBase(baseNombre)
        micursor = db.cursor()
        if validar(titulo.get()):
            registro = (titulo.get(), descripcion.get())
            sql = "INSERT INTO producto (titulo,descripcion) VALUES (%s,%s)"
            if askyesno ('Confirma','¿Desea confirmar el Alta?'):
                try:
                    micursor.execute(sql,registro)
                    db.commit()
                    mensaje = "Se cargó " + str(micursor.rowcount) + " registro correctamente: " + str(registro[0])
                    showinfo('Alta Confirmada', mensaje)
                    reset(titulo, descripcion)
                    resetTree(tabla) # Borra la tabla
                    query(tabla)    # Completa la tabla con el dato actualizado.
                except:
                    showinfo ('Alta Rechazada', sys.exc_info()[1])
        else:
            error_msg = titulo.get() + " no es válido."
            showerror ("Error en el ingreso", error_msg)
    except:
        showinfo ('Error con la BD', sys.exc_info()[1])


def crearBD():
    try:
        mibase = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        baseNombre = tkinter.simpledialog.askstring("Elija el Nombre de la Base", prompt="Nombre")
        micursor = mibase.cursor()
        baseSQL = f"CREATE DATABASE {baseNombre}"
        micursor.execute(baseSQL)
        mensaje = f"Se ha creado la base {baseNombre}"
        showinfo ('BD Creada', mensaje)
    except:
        showinfo ('Error', sys.exc_info()[1])
    
def crearTabla():
    try:
        mibase = conectarBase(baseNombre)
        micursor= mibase.cursor()
        micursor.execute("CREATE TABLE producto (id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, titulo VARCHAR(128) COLLATE utf8_spanish2_ci NOT NULL, descripcion TEXT COLLATE utf8_spanish2_ci NOT NULL)")
        mensaje = "Se ha creado la tabla "
        showinfo ('Tabla Creada', mensaje) 
    except:
        showinfo ('Error', sys.exc_info()[1])
        
def query(tabla):
    try:
        mibase = conectarBase(baseNombre)
        micursor = mibase.cursor()
        selectQuery = "SELECT * FROM producto"
        micursor.execute(selectQuery)
        showInfo = micursor.fetchall()  # Devuelve un arreglo de tuplas
        
        for i in range(len(showInfo)):
            tabla.insert('', i+1, text = i+1, values = (showInfo[i][0],showInfo[i][1],showInfo[i][2]))
            #tabla.insert('', i, text = showInfo[i][0], values = (showInfo[i][1],showInfo[i][2]))
            #tabla.insert("","end",values=(showInfo[i]))
    except:
        mensaje = str(sys.exc_info()[1])
        mensajeDB = mensaje + ' Pruebe Crear una base de datos.'

        showinfo ('Error', mensajeDB )

def resetTree(tabla):
    for fila in tabla.get_children():
        tabla.delete(fila)

def updateItem(tabla,id,titulo, descripcion):
    try:
        db = conectarBase(baseNombre)
        micursor = db.cursor()
        if validar(titulo):
            registro = (titulo, descripcion, id)
            sql = """UPDATE producto SET titulo = %s, descripcion = %s WHERE producto.id = %s"""
            if askyesno ('Confirma','¿Desea confirmar la modificación?'):
                try:
                    micursor.execute(sql,registro)
                    db.commit()
                    mensaje = "Se actualizó " + str(micursor.rowcount) + " registro correctamente: " + str(registro[0])
                    showinfo('Modificación Confirmada', mensaje)
                    resetTree(tabla) # Borra la tabla
                    query(tabla)    # Completa la tabla con el dato actualizado.
                except:
                    showinfo ('Actualización Rechazada', sys.exc_info()[1])
        else:
            error_msg = titulo + " no es válido."
            showerror ("Error en el ingreso", error_msg)
    except:
        showinfo ('Error con la BD', sys.exc_info()[1])

def deleteItem(tabla, id, titulo, descripcion):
    try:
        db = conectarBase(baseNombre)
        micursor = db.cursor()
        sql = """DELETE FROM producto WHERE producto.id = %s"""
        registro = (id,)
        if askyesno ('Confirma','¿Desea eliminar el registro ' + titulo +'?'):
            try:
                micursor.execute(sql,registro)
                db.commit()
                mensaje = "Se eliminó " + str(micursor.rowcount) + " registro correctamente: " + str(id)
                showinfo('Eliminación Confirmada', mensaje)
                resetTree(tabla) # Borra la tabla
                query(tabla)    # Completa la tabla con el dato actualizado.
            except:
                showinfo ('Eliminación Rechazada', sys.exc_info()[1])

    except:
        showinfo ('Error con la BD', sys.exc_info()[1])