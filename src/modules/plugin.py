import commands
class plugin():
    def __init__(self,sharedData,privateData,kernelData):
        self.sharedData=sharedData
        self.privateData=privateData
        self.kernelData=kernelData
        self.name=self.__class__.__name__
        #self.name=self.__class__.__name__

    def load(self,localCallback,globalCallback):
        print "loading of "+self.name
        localCallback("GetRequest",self.callbackGetRequest,self.name)
    def getHtmlConfigCallback(self):
        return self.htmlConfigCallback
    def htmlConfigCallback(self):
        
        status,output = commands.getstatusoutput("scp /home/franck/torrent/*.torrent franck@ovh:/home/franck/")
        print "status:"+str(status)+", output:"+output
        return "<br/>No configuration module done<br/>"
    def unload(self):
        print "unloading of "+self.name    
    def callbackGetRequest(self,query):
        print query    