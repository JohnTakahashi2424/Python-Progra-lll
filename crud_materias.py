import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # tu contraseña de MySQL
        database="db_academica"
    )

def consultar():
    cnx = conectar()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM materias")
    resultado = cursor.fetchall()
    cursor.close()
    cnx.close()
    return resultado

def agregar(datos):
    cnx = conectar()
    cursor = cnx.cursor()
    sql = "INSERT INTO materias (codigo, nombre, descripcion) VALUES (%s, %s, %s)"
    cursor.execute(sql, (
        datos["codigo"],
        datos["nombre"],
        datos["descripcion"]
    ))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True

def eliminar(idMateria):
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM materias WHERE idMateria=%s", (idMateria,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True
