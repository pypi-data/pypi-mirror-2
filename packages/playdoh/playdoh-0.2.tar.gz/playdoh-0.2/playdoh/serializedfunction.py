import inspect, sys, imp, struct, os.path, py_compile, time
from serializedtools import *
from serializedobject import *
import playdoh

_cachedir = os.path.join(os.path.dirname(sys.modules['playdoh'].__file__), 'cache')
DEBUG = False

__all__ = ['SerializedFunction']

class ModuleStruct(object):
    def __init__(self, module = None):
        if module is not None:
            self.name = module.name
            self.path = module.path
            self.filename = module.filename
            self.dir = module.dir
            self.subdir = module.subdir
        
    def __repr__(self):
        return "<module '%s' in '%s'>" % (self.name, self.path)

def getmodulestructs(modulelist):
    r = []
    for m in modulelist:
        r.append(ModuleStruct(m))
    return r

class SerializedFunction(object):
    """
    Defines a serialized function which can be transmitted over a network.
    
    **Usage**
    
        @SerializedFunction
        def fun(x,y):
            return x+y
    
    When pickled/unpickled, the fun object will now work even if the body
    of the function is not available : it is now contained in the pickled file.
    """
    def __init__(self, fun, _doserialize = True, *args):
        if inspect.isfunction(fun):
            self.type = 'function'
        elif inspect.isclass(fun):
            self.type = 'class'
        else:
            raise Exception('fun must be either a function or a class')
        
        self.cacheduration = 5 # duration of the cache for writing modules in the cache folder
#        self.writtenmodules = False # has written modules in the cache yet?
        self.name = fun.__name__
        
        if len(args) > 0:
            self.args = args
        else:
            self.args = []
        
        self._doserialize = _doserialize
        if _doserialize:
            o = SerializedObject(fun)
            self.modulename = o.module.name
            if self.modulename == '__main__':
                self.modulename = "main"
            modulestotransfer = o.getmodulesindir()
            self.modulestotransfer = getmodulestructs(modulestotransfer)
#            self.moduleimports = o.getimports()
#            self.compilemodules()
            self.loadmodules()
            # The current directory is the one from which all the modules can be imported
            # any module not in this directory is assumed to be installed on every worker machine.
            self.dir = os.getcwd()
        else:
            self.modulename = sys.modules[fun.__module__].__name__
            if self.modulename == '__main__':
                self.modulename = "main"
#            self.moduleimports = "from %s import %s\nimport %s" % (self.modulename,
#                                                                   self.name,
#                                                                   self.modulename)
        self.fun = None
        
        if self.type == 'function':
            inspfun = fun
        elif self.type == 'class':
            self.nargs = fun.__init__.func_code.co_argcount-1
            inspfun = fun.__call__
        insp = inspect.getargspec(inspfun)
        self.varnames = insp[0] # names of the variables of the function
        self.varargs = insp[1]
        self.keywords =  insp[2]
         
#    def compilemodules(self):
#        """
#        Compiles the modules to transfer if necessary.
#        """
#        for i in xrange(len(self.modulestotransfer)):
#            file = self.modulestotransfer[i].path
#            # Compiles the script if it is not already compiled
#            if os.path.splitext(file)[1] == '.py':
#                py_compile.compile(file)
#                self.modulestotransfer[i].path += 'c'
     
    def loadmodules(self):
        """
        Loads the compiled modules to transfer in this object
        as char lists, using serializedtools.
        """
        modules = []
        for i in xrange(len(self.modulestotransfer)):
            m = self.modulestotransfer[i]
            file = m.path
            if os.path.splitext(file)[1] == '.py':
                self.modulestotransfer[i].filename = os.path.basename(file)
                self.modulestotransfer[i].code = readbinary(file)
                modules.append(self.modulestotransfer[i])
                
#                # loads __init__.py if exists
                initfile = os.path.join(os.path.dirname(file), '__init__.py')
                if os.path.exists(initfile) and not(self.modulestotransfer[i].filename == initfile):
                    submod = ModuleStruct()
                    submod.name = '.'.join(m.name.split('.')[:-1])
                    submod.path = initfile
                    submod.filename = os.path.basename(initfile)
                    submod.dir = os.path.dirname(initfile)
                    submod.subdir = m.subdir
                    submod.code = readbinary(initfile)
                    modules.append(submod)
            else:
                raise Exception('The file in which %s is defined must be a valid .py module' % self.name)

#        submodules.extend(self.modulestotransfer)
#        self.modulestotransfer = submodules
        self.modulestotransfer = modules
#        self.modulestotransfer.extend(submodules)
        
    def createcachedir(self, subdir):
        """
        Creates the sub directories in the cache folder if necessary.
        """
        curdir = ""
        submods = os.path.split(subdir)
        for submod in submods:
            curdir = os.path.join(curdir, submod)
            dir = os.path.realpath(os.path.join(_cachedir, curdir))
            if not os.path.exists(dir):
                os.mkdir(dir)
        
    def writemodules(self):
        """
        Writes the text code of the modules to transfer into .py files in the cache.
        """
        # TODO: cache system (not transferring already transfered files??
        
        if not os.path.exists(_cachedir):
            os.mkdir(_cachedir)
        
        if DEBUG:
            print self.modulestotransfer
            sys.stdout.flush()
        
        for i in xrange(len(self.modulestotransfer)):
            m = self.modulestotransfer[i]
            self.createcachedir(m.subdir)
            filename = os.path.join(_cachedir, m.subdir, m.filename)
            filename = os.path.realpath(filename)
            
            if DEBUG:
                print _cachedir, m.subdir, m.filename
                sys.stdout.flush()
            
            if (not os.path.exists(filename)) or (time.time()-os.path.getmtime(filename)>self.cacheduration):
                writebinary(filename, m.code)
            self.modulestotransfer[i].cachedpath = filename
            if m.name == "__main__":
                name = "main"
            else:
                name = m.name
            if name == self.modulename:
                self.modulecachedpath = filename
#            self.writtenmodules = True
            
            
        sys.stdout.flush()
    
    def importmodules(self):
        """
        Imports dynamically the modules.
        """
        self.loadedmodules = dict()
        if self._doserialize:
            for m in self.modulestotransfer:
#                
                if m.name == "__main__":
                    name = "main"
                else:
                    name = m.name   
                
                if DEBUG:
                    print name, m.cachedpath
                    sys.stdout.flush()
                
                
                self.loadedmodules[name] = imp.load_source(name, m.cachedpath)
                
                # We load the submodules with different names : pack1.pack2.mod, pack2.mod, etc.
                # to handle using the modules from different subfolders
                submods = name.split('.')
                if len(submods) > 1:
                    for i in xrange(1,len(submods)):
                        curmod = '.'.join(submods[i:])
                        
                        if DEBUG:
                            print curmod, m.cachedpath
                            sys.stdout.flush()
                        
                        
                        self.loadedmodules[curmod] = imp.load_source(curmod, m.cachedpath)
                        # TODO: more efficient: set the variables in the namespace instead of
                        # reloading the modules?

            # also, import the module where the function is defined in a variable
            # named self.modulename, so that we can access it later.
            self.loadedmodules[self.modulename] = imp.load_source(self.modulename, self.modulecachedpath)
        
        else:
            exec("import %s" % self.modulename)
#            self.loadedmodules[self.modulename] = imp.load_module(self.modulename, *imp.find_module(self.modulename))
        
        sys.stdout.flush()
    
    def setpersistent(self, *args):
        # TODO: **kwds?
        self.args = args[:self.nargs]
            
    def load_function(self):
        """
        Loads the function in self.fun
        """
        if self._doserialize:
#            if not self.writtenmodules:
            self.writemodules()
        self.importmodules()
        if self.type == 'class':
            setattr(self, "fun", getattr(sys.modules[self.modulename], self.name)(*self.args))
        elif self.type == 'function':
            setattr(self, "fun", getattr(sys.modules[self.modulename], self.name))
            
    def __call__(self, *funargs, **funkwds):
        if self.fun is None:
            self.load_function()
        if (self.varargs is None) and (self.keywords is None):
            for name in funkwds.keys():
                if name not in self.varnames:
                    del funkwds[name]
        return self.fun(*funargs, **funkwds)
