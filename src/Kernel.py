import modules


class Kernel():
    def __init__(self):
        self.loadedModule={}
        self.sharedModuleData={}
        self.privateModuleData={}
        self.kernelPublicData={}
        self.kernelprivateData={}
        self.globalCallback={}
        
        
    def loadModules(self):
        for mod_name in modules.__all__:
            mod = __import__ ("modules." + mod_name, fromlist=modules.__all__) # on charge le module
            mod_instance = getattr(mod, mod_name)(self.sharedModuleData,self.privateModuleData,self.kernelPublicData) # on appelle le constructeur
            self.loadedModule[mod_name]={}
            self.loadedModule[mod_name]["instance"]=mod_instance
            self.loadedModule[mod_name]["callback"]={}
            
            mod_instance.load(self.registerLocalCallback,self.registerGlobalCallback)
            self.loadedModule[mod_name]["htmlConfigcallback"]=mod_instance.getHtmlConfigCallback()
            self.loadedModule[mod_name]["htmlConfigcallback"]()
            
    def unloadModule(self,moduleName=""):
        if moduleName=="":
            for mod in self.loadedModule.keys():
                self.loadedModule[mod].unload()
                del self.loadedModule[mod]
            self.loadedModule.clear()
        else:
            self.loadedModule[moduleName].unload()
            del self.loadedModule[moduleName]
    def reloadModule(self):
        self.unloadModule()
        self.loadModules()
    def test(self):
        self.loadedModule["plugin"]["callback"]["GetRequest"]("a query")
    def registerGlobalCallback(self,event,callback):
        if event not in self.globalCallback:
            self.globalCallback[event]=[]
        self.globalCallback[event].append(callback)    
    def registerLocalCallback(self,event,callback,moduleName):
        self.loadedModule[moduleName]["callback"][event]=callback    
            
            
        
            
            
tmp=Kernel()
tmp.loadModules()
#tmp.unloadModule()
tmp.test()    