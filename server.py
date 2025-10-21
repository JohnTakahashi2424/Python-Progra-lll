from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import json 
import crud_alumno
import crud_docente
import crud_materia
import crud_usuario

port = 3000

crudAlumno = crud_alumno.crud_alumno()
crudDocente = crud_docente.crud_docente()
crudMateria = crud_materia.crud_materia()
crudUsuario = crud_usuario.crud_usuario()

class miServidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            url_parseada = urlparse(self.path)
            path = url_parseada.path
            parametros = parse_qs(url_parseada.query)

            # Página principal (login)
            if self.path == "/":
                self.path = "login.html"
                return SimpleHTTPRequestHandler.do_GET(self)

            # Página principal tras el login
            if self.path == "/index.html":
                self.path = "index.html"
                return SimpleHTTPRequestHandler.do_GET(self)

            # Endpoints JSON
            if path == "/alumnos":
                alumnos = crudAlumno.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(alumnos).encode("utf-8"))
                return

            if path == "/docentes":
                docentes = crudDocente.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(docentes).encode("utf-8"))
                return

            if path == "/materias":
                materias = crudMateria.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(materias).encode("utf-8"))
                return

            if path == "/usuarios":
                usuarios = crudUsuario.consultar("")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(usuarios).encode("utf-8"))
                return

            # Cargar vistas dinámicas
            if path == "/vistas" and "form" in parametros:
                self.path = f"modulos/{parametros['form'][0]}.html"
                return SimpleHTTPRequestHandler.do_GET(self)

            # Servir cualquier archivo estático (HTML, JS, CSS, imágenes, etc.)
            return SimpleHTTPRequestHandler.do_GET(self)

        except Exception as e:
            print("Error en do_GET:", e)
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error interno del servidor: {str(e)}".encode("utf-8"))

    def do_POST(self):
        try:
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud)
            datos = datos.decode("utf-8")
            datos = parse.unquote(datos)
            datos = json.loads(datos)

            url_parseada = urlparse(self.path)
            path = url_parseada.path

            if path == "/alumnos":
                resp = {"msg": crudAlumno.administrar(datos)}
            elif path == "/docentes":
                resp = {"msg": crudDocente.administrar(datos)}
            elif path == "/materias":
                resp = {"msg": crudMateria.administrar(datos)}
            elif path == "/usuarios":
                resp = {"msg": crudUsuario.administrar(datos)}
            elif path == "/login":
                resp = crudUsuario.login(datos['usuario'], datos['clave'])
            else:
                resp = {"msg": "error: ruta no encontrada"}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        except Exception as e:
            print("Error en do_POST:", e)
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error en POST: {str(e)}".encode("utf-8"))

print(f"Servidor ejecutándose en http://localhost:{port}")
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()    
