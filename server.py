from http.server import HTTPServer, SimpleHTTPRequestHandler
port = 3000

class miServirdor(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/":
            self.path="index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
    
print("Servidor Ejecutandose en el puerto 80", port)
server = HTTPServer(("localhost", port), miServirdor)
server.serve_forever() 