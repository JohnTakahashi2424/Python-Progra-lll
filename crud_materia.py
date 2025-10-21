import crud_academico

db = crud_academico.crud()

class crud_materia:
    def consultar(self, buscar):
        return db.consultar("SELECT * FROM materias WHERE nombre like '%"+ buscar +"%'")
    
    def administrar(self, datos):
        if datos['accion']=="nuevo":
            sql = """
                INSERT INTO materias (codigo, nombre, uv)
                VALUES (%s, %s, %s)
            """
            valores = (datos['codigo'], datos['nombre'], datos['uv'])
        if datos['accion']=="modificar":
            sql = """
                UPDATE materias SET codigo=%s, nombre=%s, uv=%s
                WHERE idMateria=%s
            """
            valores = (datos['codigo'], datos['nombre'], datos['uv'], datos['idMateria'])
        if datos['accion']=="eliminar":
            sql = "DELETE FROM materias WHERE idMateria=%s"
            valores = (datos['idMateria'],)
        return db.ejecutar(sql, valores)   