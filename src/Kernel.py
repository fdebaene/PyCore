import modules
MajorVersion=0
MinorVersion=1


class Kernel():
    def __init__(self):
        
        self.loadedModule={}
        self.kernelPublicData={}
        self.globalCallback={}
        self.majorVersion=MajorVersion
        self.minorVersion=MinorVersion
        
        self.status={}
        self.status["Name"]="kernel"
        self.status["Version"]=str(self.majorVersion)+"."+str(self.minorVersion)
        self.status["State"]=2
        self.status["Author"]="Debaene Franck"
        self.status["License"]="Not decided yet"
        self.status["AuthorContact"]="devdfranck@gmail.com"
        self.status["Website"]="not set"
    def accesModuleData(self,moduleName,dataName):
        if moduleName in self.loadedModule.keys():
            if dataName in self.loadedModule[moduleName]["data"].keys():
                return True,self.loadedModule[moduleName]["data"][dataName]
            else:
                return False,moduleName+" loaded but no data "+dataName+ "found."
        else:
            return False,moduleName+" not loaded, can't get "+ dataName+" data."
    def setModuleData(self,module,dataName,value):
        self.loadedModule[module.name]["data"][dataName]=value
        
    # load module from subfolder modules, allowing plugin module for testing purpose, need to change the loading process to avoid loading this module
    # all every other plugin need to subclass this module
    def loadModules(self):
        
        self.registerGlobalCallback("GetStatus",self.getStatus)
        for mod_name in modules.__all__:
            mod = __import__ ("modules." + mod_name, fromlist=modules.__all__) # on charge le module
            mod_instance = getattr(mod, mod_name)(self.setModuleData,self.accesModuleData,self.kernelPublicData) # on appelle le constructeur, with shared data attribution
            mod_instance.registerEventFunction(self.registerLocalCallback,self.registerGlobalCallback,self.raiseGlobalEvent, self.raiseLocalEvent,self.removeGlobalCallback, self.removeLocalCallback) 
            self.loadedModule[mod_name]={}
            self.loadedModule[mod_name]["instance"]=mod_instance
            self.loadedModule[mod_name]["callback"]={}
            self.loadedModule[mod_name]["data"]={}
        for mod_name in self.loadedModule.keys():
            self.loadedModule[mod_name]["instance"].load()
                
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
    def registerLocalCallback(self,event,callback,module):
        print "registring callback "+event+" in module "+module.name
        
        self.loadedModule[module.name]["callback"][event]=callback
    def removeGlobalCallback(self,event,callback):
        if event not in self.globalCallback.keys():
            return
        present=False
        for index,curCB in self.globalCallback[event]:
            if curCB==callback:
                present=True
        if present:
            self.globalCallback[event].remove(callback)    
    def removeLocalCallback(self,event,callback,module):
        if module.name in self.loadedModule.keys():
            if event in self.loadedModule[module.name]["callback"].keys():
                del self.loadedModule[module.name]["callback"][event]
        
        
        
        
    def raiseGlobalEvent(self,event,param1=None,param2=None,param3=None,param4=None,param5=None):
        if event in self.globalCallback.keys():
            result=[]
            for callback in self.globalCallback[event]:
                if param5!=None:
                    result.append(callback(param1,param2,param3,param4,param5))
                else:
                    if param4!=None:
                        result.append(callback(param1,param2,param3,param4,param4))
                    else:
                        if param3!=None:
                            result.append(callback(param1,param2,param3))
                        else:
                            if param2!=None:
                                result.append(callback(param1,param2))
                            else:
                                if param1!=None:
                                    result.append(callback(param1))
                                else:
                                    result.append(callback())
            return True,result
        return False, "No callback avaibale for event "+event
                                
    def raiseLocalEvent(self,event,moduleName,param1=None,param2=None,param3=None,param4=None,param5=None):
        if moduleName not in self.loadedModule.keys():
            
            return False,moduleName+ " not loaded"
        for key in self.loadedModule[moduleName]["callback"].keys():
            if key==event:
                callback=self.loadedModule[moduleName]["callback"][event]
                if param5!=None:
                    return True,callback(param1,param2,param3,param4,param5)
                else:
                    if param4!=None:
                        return True,callback(param1,param2,param3,param4,param4)
                    else:
                        if param3!=None:
                            return True,callback(param1,param2,param3)
                        else:
                            if param2!=None:
                                return True,callback(param1,param2)
                            else:
                                if param1!=None:
                                    return True,callback(param1)
                                else:
                                    return True,callback()
            else:
                return False, "no callback for event "+event+"@"+moduleName    
    def run(self):
        for module in self.loadedModule.keys():
            self.loadedModule[module]["instance"].run()                            
    def getStatus(self,param=""):
        currentState=[]
        currentState.append(self.status)
        for moduleName in self.loadedModule.keys():
            currentState.append(self.loadedModule[moduleName]["instance"].getStatus())
        return currentState
            
        
        
        
            
            
        
if __name__ == '__main__':
    tmp=Kernel()
    tmp.loadModules()
    #tmp.unloadModule()
    #tmp.raiseGlobalEvent("eventTest","plugin","c'est", " win")
    print tmp.getStatus()
    tmp.run()   