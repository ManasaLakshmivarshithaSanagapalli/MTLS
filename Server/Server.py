from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

server_address = ('localhost', 4443)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
context.load_verify_locations('../CA2/ca2.crt')
context.verify_mode = ssl.CERT_REQUIRED

httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
print("Server running on https://localhost:4443")
httpd.serve_forever()
