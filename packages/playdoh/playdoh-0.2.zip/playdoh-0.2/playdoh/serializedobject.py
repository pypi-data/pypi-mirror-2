import sys, inspect, os, exceptions

class SerializedObject(object):
    def __init__(self, obj, parentdir = None):
        self.vars = dict()
        self.module = None
        self.foundmodules = False
        self.parentdir = parentdir # full path of the directory where the original object is defined
        
        # modules to import * (those that are needed and not in the right folder)
        self.starmodules = []
        
        if inspect.ismodule(obj):
            self.type = "module"
            self.name = obj.__name__
#            self.themodule = obj
            path = obj.__file__
            if (os.path.splitext(path)[1] == '.pyc') or (os.path.splitext(path)[1] == '.pyo'):
                path = path[:-1]
            self.path = path
            self.dir = os.path.dirname(self.path)
            if self.dir == "":
                self.path = "./"+obj.__file__
            self.dir = os.path.dirname(os.path.realpath(self.path))
            if self.parentdir is None:
                self.parentdir = self.dir
            self.filename = os.path.basename(self.path)
        elif inspect.isfunction(obj):
            self.type = "function"
            self.name = obj.__name__
            self.module = SerializedObject(sys.modules[obj.__module__], self.parentdir)
            if self.parentdir is None:
                self.parentdir = self.module.parentdir
            # Names of the global variables (functions, modules)
            self.varnames = obj.func_code.co_names
            self.vars, self.starmodules = self.getvars(obj)
        elif inspect.ismethod(obj):
            self.type = "method"
            self.name = obj.__name__
            self.module = SerializedObject(sys.modules[obj.__module__], self.parentdir)
            if self.parentdir is None:
                self.parentdir = self.module.parentdir
        elif inspect.isclass(obj):
            self.type = "class"
            self.name = obj.__name__
            self.module = SerializedObject(sys.modules[obj.__module__], self.parentdir)
            if self.parentdir is None:
                self.parentdir = self.module.parentdir
            
            self.varnames = []
            self.vars = dict()
            
            members = ['__init__', '__call__']
#            members = inspect.getmembers(obj)
            
            for member in members:
                if member in inspect.getmembers(obj):
                    self.varnames.extend(getattr(obj, member).func_code.co_names)
                    # BUG: func_code.co_names contains the self.*** vars even if they are not available in the module
                    vars, modules = self.getvars(getattr(obj, member))
                    for name, var in vars.iteritems():
                        self.vars[name] = var
                    for m in modules:
                        if m not in self.starmodules:
                            self.starmodules.append(m)
        # TODO: instance of a user-defined class??
        else:
            self.type = "other"
            self.klass = obj.__class__
            self.value = obj
     
    def __getattr__(self, key):
        return self.vars[key]
        
    def __repr__(self):
        if self.type == "module":
            return "<'%s' module in '%s'>" % (self.name, self.path)
        else:
            return "<'%s' %s in '%s'>" % (self.name, self.type, self.module.name)
        
    @staticmethod
    def _getvars(f):
        varnames = f.func_code.co_names
        module = f.__module__
        themodule = sys.modules[module]
        modules = []
        vars = dict()
        for name in varnames:
            try:
                var = getattr(themodule, name)
                if inspect.ismodule(var):
                    modules.append(var)
                    continue
            except:
                var = None
                for module2 in modules:
                    try:
                        var = getattr(module2, name)
                    except:
                        pass
                if var is None:
#                    raise Exception("Unable to find %s in module %s" % (name, module))
                    pass
            if not inspect.ismodule(var):
                vars[name] = var
        return vars

    def getvars(self, f):
        """
        Retrieves the variables used by the object in a recursive fashion.
        """
        vars = SerializedObject._getvars(f)
        vars2 = dict()
        modules = []
        for name, val in vars.iteritems():
            try:
                module = val.__module__#.__file__# sys.modules[val.__module__].__file__
                # we don't bother looking at the variables defined in the modules we don't import
                # (the ones that are assumed to be preinstalled on every worker machine)
                file = sys.modules[module].__file__
    #            if module.split('.')[0] not in self.notimportedmodules:
                if self.isindir(file, self.parentdir):
                    vars2[name] = SerializedObject(val, self.parentdir)
                else:
                    if module not in modules:
                        modules.append(module)
            except exceptions.AttributeError:
                pass
        # returns the variables, and also the modules that are not in the 
        # path where the script is launched and that are assumed to be available
        # on every worker machine : we want to do import mod and from mod import *
        # for those modules.
        return vars2, modules

    def isindir(self, path, dir):
        """
        Imports only the modules located in the directory (or subdirectories)
        where the original object is defined.
        """
        return (os.path.commonprefix([dir, os.path.dirname(path)]) == dir)

    def getmodulesindir(self):
        if not self.foundmodules:
            self.getmodules()
        modulesindir = []
        
        for m in self.modules:
            if (m.name == self.module.name) or (self.isindir(m.path, self.parentdir)):
                m.subdir = os.path.relpath(m.dir, self.module.dir)
                modulesindir.append(m)
                
        return modulesindir

    def getmodules(self):
        """
        self.modules contain the list of the modules to import, in the right order
        for the dependencies to be satisfied.
        self.modulevars is a dict, each key is a module name, each value is the
        list of the global variables to import in that module.
        """
        self.foundmodules = True
        modules = []
        modulenames = []
        modulevars = dict()
        
        # The order matters in 'modules' : the dependencies must be resolved in the right order
        def add(o):
            for v in o.vars.itervalues():
                if v.type is not "other":
                    add(v)
                    if v.module.name not in modulenames:
                        modules.append(v.module)
                        modulenames.append(v.module.name)
                    if v.module.name not in modulevars.keys():
                        modulevars[v.module.name] = []
                    modulevars[v.module.name].append(v)
        add(self)
        
        if self.module.name not in modulenames:
            modules.append(self.module)
            modulenames.append(self.module.name)
            modulevars[self.module.name] = [self]
        
        self.modules = modules
        self.modulenames = modulenames
        self.modulevars = modulevars
        
        return modules

    def getimports(self):
        if not self.foundmodules:
            self.getmodules()
        imports = ""
        for name in self.starmodules:
            if name == "__main__":
                continue
            imports += "import %s\n" % name
            imports += "from %s import *\n" % name
        for module in self.modules:
            vars = [v.name for v in self.modulevars[module.name]]
            sys.stdout.flush()
            if module.name == "__main__":
                continue
            imports += "import %s\n" % module.name
            if len(vars)>0:
                imports += "from %s import " % module.name
                imports += ", ".join(vars)
            imports += "\n"
        return imports

