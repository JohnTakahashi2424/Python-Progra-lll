from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import json
import crud_alumno
import crud_docentes
import crud_materias

port = 3000
crudAlumno = crud_alumno.crud_alumno()

class miServidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        url_parseada = urlparse(self.path)
        path = url_parseada.path
        parametros = parse_qs(url_parseada.query)

        if self.path == "/":
            self.path = "index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        if self.path == "/alumnos":
            alumnos = crudAlumno.consultar("")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(alumnos).encode('utf-8'))
            return
        
        if self.path == "/docentes":
            docentes = crud_docentes.consultar()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(docentes).encode("utf-8"))
            return
        
        # Ruta para materias
        if self.path == "/materias":
            try:
                materias = crud_materias.consultar()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(materias).encode("utf-8"))
            except Exception as e:
                print(f"Error en GET /materias: {e}")
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"msg": "error", "detalle": str(e)}).encode("utf-8"))
            return
        
        if path == "/vistas":
            self.path = '/modulos/' + parametros['form'][0] + '.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        try:
            if self.path == "/alumnos":
                longitud = int(self.headers['Content-Length'])
                datos = self.rfile.read(longitud)
                datos = datos.decode("utf-8")
                datos = parse.unquote(datos)
                datos = json.loads(datos)
                resp = {"msg": crudAlumno.administrar(datos)}
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return
            
            if self.path == "/guardar_docente":
                longitud = int(self.headers['Content-Length'])
                datos = self.rfile.read(longitud)
                datos = datos.decode("utf-8")
                datos = parse.unquote(datos)
                datos = json.loads(datos)
                resp = {"msg": "ok"} if crud_docentes.agregar(datos) else {"msg": "error"}
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                return
            
            # Ruta para materias
            if self.path == "/materias":
                print("=== Recibiendo POST en /materias ===")
                longitud = int(self.headers['Content-Length'])
                print(f"Longitud del contenido: {longitud}")
                
                datos = self.rfile.read(longitud)
                print(f"Datos raw: {datos}")
                
                datos = datos.decode("utf-8")
                print(f"Datos decodificados: {datos}")
                
                datos = parse.unquote(datos)
                print(f"Datos después de unquote: {datos}")
                
                datos = json.loads(datos)
                print(f"Datos parseados como JSON: {datos}")
                
                resultado = crud_materias.administrar(datos)
                print(f"Resultado de administrar: {resultado}")
                
                resp = {"msg": resultado}
                
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp).encode("utf-8"))
                print("Respuesta enviada exitosamente")
                return
                
        except Exception as e:
            print(f"ERROR en do_POST: {e}")
            import traceback
            traceback.print_exc()
            
            try:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"msg": f"Error en servidor: {str(e)}"}).encode("utf-8"))
            except:
                pass

print("Servidor ejecutandose en el puerto", port)
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()