import SimpleHTTPServer
import SocketServer

PORT, Handler = 8080, SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("localhost", PORT), Handler)
httpd.serve_forever()