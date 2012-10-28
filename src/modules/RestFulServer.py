from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from plugin import plugin

class GetHandler(BaseHTTPRequestHandler):
    def __init__(self):
        super( GetHandler, self ).__init__()
        self.moduleCallBackGetRequest={}
    def do_GET(self):
        #message=self.Getcallback(self.path)
        message=self.path
        #print self.path
        self.send_response(200)
        self.end_headers()
        self.wfile.write(message)
        return
    def addModuleGetRequestCallback(self,moduleName,callback ):
        self.moduleCallBackGetRequest[moduleName]=callback

class RestFulServer(plugin):
    def __init__(self):
        self.handler = GetHandler()

    server = HTTPServer(('localhost', 8080), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()