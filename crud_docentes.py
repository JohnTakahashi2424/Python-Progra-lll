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
    cursor.execute("SELECT * FROM docentes")
    resultado = cursor.fetchall()
    cursor.close()
    cnx.close()
    return resultado

def agregar(datos):
    cnx = conectar()
    cursor = cnx.cursor()
    sql = "INSERT INTO docentes (codigo, nombre, direccion, telefono, email, dui, escalafon) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (
        datos["codigo"],
        datos["nombre"],
        datos["direccion"],
        datos["telefono"],
        datos["email"],
        datos["dui"],
        datos["escalafon"]
    ))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True

def actualizar(id, datos):
    cnx = conectar()
    cursor = cnx.cursor()
    sql = "UPDATE docentes SET codigo=%s, nombre=%s, direccion=%s, telefono=%s, email=%s, dui=%s, escalafon=%s WHERE id=%s"
    cursor.execute(sql, (
        datos["codigo"],
        datos["nombre"],
        datos["direccion"],
        datos["telefono"],
        datos["email"],
        datos["dui"],
        datos["escalafon"],
        id
    ))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True

def eliminar(id):
    cnx = conectar()
    cursor = cnx.cursor()
    cursor.execute("DELETE FROM docentes WHERE id=%s", (id,))
    cnx.commit()
    cursor.close()
    cnx.close()
    return True 
