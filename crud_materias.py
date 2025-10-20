import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_academica'
        )
        print("✓ Conexión exitosa a la base de datos")
        return conexion
    except Error as e:
        print(f"✗ Error de conexión: {e}")
        return None

def consultar():
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        if conexion is None:
            print("✗ No se pudo conectar a la base de datos")
            return []
        
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM materias ORDER BY idmaterias")
        materias = []
        
        for row in cursor.fetchall():
            materia = {
                'idmaterias': row[0],
                'codigo': row[1],
                'nombre': row[2],
                'creditos': row[3],
                'horas': row[4]
            }
            materias.append(materia)
        
        print(f"✓ Se consultaron {len(materias)} materias")
        return materias
        
    except Error as e:
        print(f"✗ Error al consultar materias: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def agregar(datos):
    conexion = None
    cursor = None
    try:
        print("\n=== INICIANDO INSERCIÓN DE MATERIA ===")
        print(f"Datos recibidos: {datos}")
        
        conexion = conectar()
        if conexion is None:
            print("✗ No se pudo conectar para agregar")
            return False
        
        cursor = conexion.cursor()
        
        # Preparar valores
        codigo = str(datos.get('codigo', '')).strip()
        nombre = str(datos.get('nombre', '')).strip()
        creditos = int(datos.get('creditos', 0))
        horas = int(datos.get('horas', 0))
        
        print(f"Valores a insertar:")
        print(f"  - codigo: '{codigo}'")
        print(f"  - nombre: '{nombre}'")
        print(f"  - creditos: {creditos}")
        print(f"  - horas: {horas}")
        
        sql = "INSERT INTO materias (codigo, nombre, creditos, horas) VALUES (%s, %s, %s, %s)"
        valores = (codigo, nombre, creditos, horas)
        
        print(f"Ejecutando SQL: {sql}")
        print(f"Con valores: {valores}")
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        print(f"✓ Materia insertada exitosamente (ID: {cursor.lastrowid})")
        return True
        
    except Error as e:
        print(f"✗ Error MySQL al agregar materia: {e}")
        print(f"   Código de error: {e.errno}")
        print(f"   Mensaje: {e.msg}")
        return False
    except Exception as e:
        print(f"✗ Error general al agregar materia: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
            print("Conexión cerrada")

def actualizar(datos):
    conexion = None
    cursor = None
    try:
        print("\n=== INICIANDO ACTUALIZACIÓN DE MATERIA ===")
        print(f"Datos recibidos: {datos}")
        
        conexion = conectar()
        if conexion is None:
            print("✗ No se pudo conectar para actualizar")
            return False
        
        cursor = conexion.cursor()
        
        sql = "UPDATE materias SET codigo=%s, nombre=%s, creditos=%s, horas=%s WHERE idmaterias=%s"
        valores = (
            str(datos.get('codigo', '')).strip(),
            str(datos.get('nombre', '')).strip(),
            int(datos.get('creditos', 0)),
            int(datos.get('horas', 0)),
            int(datos.get('idmaterias', 0))
        )
        
        print(f"Ejecutando: {sql}")
        print(f"Valores: {valores}")
        
        cursor.execute(sql, valores)
        conexion.commit()
        
        print(f"✓ Materia actualizada ({cursor.rowcount} fila(s) afectada(s))")
        return True
        
    except Error as e:
        print(f"✗ Error MySQL al actualizar: {e}")
        return False
    except Exception as e:
        print(f"✗ Error general al actualizar: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def eliminar(id_materia):
    conexion = None
    cursor = None
    try:
        print(f"\n=== INICIANDO ELIMINACIÓN DE MATERIA ID: {id_materia} ===")
        
        conexion = conectar()
        if conexion is None:
            print("✗ No se pudo conectar para eliminar")
            return False
        
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM materias WHERE idmaterias=%s", (id_materia,))
        conexion.commit()
        
        print(f"✓ Materia eliminada ({cursor.rowcount} fila(s) afectada(s))")
        return True
        
    except Error as e:
        print(f"✗ Error MySQL al eliminar: {e}")
        return False
    except Exception as e:
        print(f"✗ Error general al eliminar: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

def administrar(datos):
    print(f"\n{'='*50}")
    print(f"CRUD MATERIAS - ADMINISTRAR")
    print(f"{'='*50}")
    print(f"Datos completos: {datos}")
    print(f"Tipo de datos: {type(datos)}")
    
    accion = datos.get('accion', '').lower().strip()
    print(f"Acción solicitada: '{accion}'")
    
    if accion == 'agregar':
        resultado = agregar(datos)
        mensaje = 'Materia agregada correctamente' if resultado else 'Error al agregar materia'
        print(f"Resultado: {mensaje}")
        return mensaje
        
    elif accion == 'actualizar':
        resultado = actualizar(datos)
        mensaje = 'Materia actualizada correctamente' if resultado else 'Error al actualizar materia'
        print(f"Resultado: {mensaje}")
        return mensaje
        
    elif accion == 'eliminar':
        resultado = eliminar(datos.get('idmaterias', 0))
        mensaje = 'Materia eliminada correctamente' if resultado else 'Error al eliminar materia'
        print(f"Resultado: {mensaje}")
        return mensaje
        
    else:
        mensaje = f'Acción no válida: "{accion}"'
        print(f"✗ {mensaje}")
        return mensaje