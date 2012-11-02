from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from plugin import plugin
import json
MajorVersion=0
MinorVersion=1


def getIndexHtmlPage():
    fic=open("./misc/index.html",'r')
    lignes=fic.readlines()
    return "".join(lignes)
def getMiscHtmlPage(page):
    fic=open("./misc/"+page,'r')
    lignes=fic.readlines()
    return "".join(lignes)

class RestFulRequestHandler(BaseHTTPRequestHandler):
   
    def do_GET(self):
        #message=self.Getcallback(self.path)
        message=self.path
        
        module=self.path.split("/")[1]
        param="/".join(self.path.split("/")[2:])
        print "module:"+module
        print "param:"+param
        
        if module!="favicon.ico" :
            if module.lower()=="getstatus":
                
                valid,message=self.server.getRestFulPlugin().raiseGlobalEvent("GetStatus",param)
                if len(message)>0:
                    if len(message[0])>0:
                        message=json.dumps(message[0])
            elif module=="":
                
                message=getIndexHtmlPage()
                valid=True
            elif module=="misc":
                
                message=getMiscHtmlPage(param)
                valid=True
            else:
                valid,message=self.server.getRestFulPlugin.raiseLocalEvent("Get",module,param)
                
            self.send_response(200)
            self.end_headers()
            if valid:
                self.wfile.write(message)
            else:
                self.wfile.write("error: "+message)
            return
class RestFulHttpServer(HTTPServer):
    def getRestFulPlugin(self):
        return self.RestFulPlugin
    def setRestFulPlugin(self,plugin):
        self.RestFulPlugin=plugin
    

class RestFulServer(plugin):
        def __init__(self,setModuleData,accesModuleData,kernelData):
            
            plugin.__init__(self,setModuleData,accesModuleData,kernelData)
            self.status["Author"]="debaene franck"
            self.status["License"]="not set"
            self.status["AuthorContact"]="devdfranck@gmail.com"
            self.status["Website"]="not set"
                
        def load(self):        
            #self.raiseLocalEvent
            self.server = RestFulHttpServer(('localhost', 8080), RestFulRequestHandler)
            self.server.setRestFulPlugin(self)
            
        
        def run(self):
            print "webserver running ..."
            self.server.serve_forever()