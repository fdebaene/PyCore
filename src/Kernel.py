import modules


class Kernel():
    def __init__(self):
        
        self.loadedModule={}
        self.sharedModuleData={}
        self.privateModuleData={}
        self.kernelPublicData={}
        self.kernelprivateData={}
        self.globalCallback={}
        
    # load module from subfolder modules, allowing plugin module for testing purpose, need to change the loading process to avoid loading this module
    # all every other plugin need to subclass this module
    def loadModules(self):
        for mod_name in modules.__all__:
            mod = __import__ ("modules." + mod_name, fromlist=modules.__all__) # on charge le module
            mod_instance = getattr(mod, mod_name)(self.sharedModuleData,self.privateModuleData,self.kernelPublicData) # on appelle le constructeur
            self.loadedModule[mod_name]={}
            self.loadedModule[mod_name]["instance"]=mod_instance
            self.loadedModule[mod_name]["callback"]={}
            mod_instance.load(self.registerLocalCallback,self.registerGlobalCallback)
          
            
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
    def registerGlobalCallback(self,event,callback):
        if event not in self.globalCallback.keys():
            self.globalCallback[event]=[]
        self.globalCallback[event].append(callback)    
    def registerLocalCallback(self,event,callback,moduleName):
        print "registring callback "+event+" in module "+moduleName
        self.loadedModule[moduleName]["callback"][event]=callback
    def raiseGlobalEvent(self,event,param):
        if event in self.globalCallback["event"].keys():
            for callback in self.globalCallback["event"]:
                callback(param)
    def raiseLocalEvent(self,event,param,moduleName):
        if moduleName not in self.loadedModule.keys():
            print moduleName+ "not loaded"
            return
        for key in self.loadedModule[moduleName]["callback"].keys():
            if key==event:
                self.loadedModule[moduleName]["callback"][event](param)
                
        
        
        
        
            
            
        
            
            
tmp=Kernel()
tmp.loadModules()
#tmp.unloadModule()
tmp.raiseLocalEvent("GetRequest", "param", "plugin")    