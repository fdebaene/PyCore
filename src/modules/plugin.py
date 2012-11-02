MajorVersion=0
MinorVersion=1
class plugin():
    def __init__(self,setModuleData,accesModuleData,kernelData):
        
        #setModuleData(self,module,dataName,value)
        self.setModuleData=setModuleData
        #exist,data=accesModuleData(self,moduleName,dataName)
        self.accesModuleData=accesModuleData
        self.kernelData=kernelData
        self.name=self.__class__.__name__
        self.majorVersion=MajorVersion
        self.minorVersion=MinorVersion
        self.status={}
        self.status["Name"]=self.name
        self.status["State"]=0
        self.status["Author"]="not set"
        self.status["License"]="not set"
        self.status["AuthorContact"]="not set"
        self.status["Website"]="not set"
        self.status["Version"]=str(self.majorVersion)+"."+str(self.minorVersion)
        
    def getStatus(self):
        return self.status   
    def registerEventFunction(self,registerLocalCallback,registerGlobalCallback,raiseGlobalEvent, raiseLocalEvent,removeGlobalCallback,removeLocalCallback):
        #registerLocalCallback(event,callback,moduleName)
        self.registerLocalCallback=registerLocalCallback
        #registerGlobalCallback(event,callback)
        self.registerGlobalCallback=registerGlobalCallback
        #raiseGlobalEvent(self,event,moduleName,param1=None,param2=None,param3=None,param4=None,param5=None)
        self.raiseGlobalEvent=raiseGlobalEvent
        #raiseLocalEvent(event,moduleName,moduleName,param1=None,param2=None,param3=None,param4=None,param5=None)
        self.raiseLocalEvent=raiseLocalEvent
        #removeLocalCallback(event,,moduleName)
        self.removeLocalCallback=removeLocalCallback
        #removeGlobalCallback(event,callback)
        self.removeGlobalCallback=removeGlobalCallback
    def load(self):
        print "loading of "+self.name
        #self.registerGlobalCallback("eventTest",self.testCallback)
        self.registerLocalCallback("Post",self.testCallback,self)
        self.status["State"]=1
    def unload(self):
        print "unloading of "+self.name
        self.status["State"]=-1
    def run(self):
        self.status["State"]=2   
    def testCallback(self,param1,param2="",param3=""):
        print param1+param2+param3
        return self.name+": calling test callback param="+param1 