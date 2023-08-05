import inspect, sys, imp, struct, os.path, py_compile
from serializedtools import *

__all__ = ['SerializedFunction']

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
    def __init__(self, fun, *args):
        if inspect.isfunction(fun):
            self.type = 'function'
        elif inspect.isclass(fun):
            self.type = 'class'
        else:
            raise Exception('fun must be either a function or a class')
        
        self.name = fun.__name__
        
        if len(args) > 0:
            self.args = args
        else:
            self.args = None
            
        # Registers the bytecode
        modfile = sys.modules[fun.__module__].__file__

        # Compiles the script if it is not alread compiled
        if os.path.splitext(modfile)[1] == '.py':
            py_compile.compile(modfile)
            modfile += 'c'
        # Loads the byte code defining the function. It is stored in a list
        # of 'char' objects.
        if os.path.splitext(modfile)[1] == '.pyc':
            # Filename
            self.filename = os.path.basename(modfile)
            
            # Bytecode
            self.bytecode = readbinary(modfile)
        else:
            raise Exception('The file in which %s is defined must be a valid .py module' % self.name)
        
        # Full path to the original file
        self.path = modfile
        
        # Directory
        self.dir = os.path.dirname(modfile)
        
        if self.type == 'function':
            self.nargs = fun.func_code.co_argcount
        elif self.type == 'class':
            self.nargs = fun.__init__.func_code.co_argcount-1
        self.fun = None
           
    def setpersistent(self, *args):
        self.args = args
            
    def __call__(self, *funargs):
        if self.fun is None:
            if not(os.path.exists(self.path)):
                filename = self.filename
                filename = os.path.splitext(filename)[0]+"_serialized" + os.path.splitext(filename)[1]
                # Writes the byte code into a binary file and loads the module dynamically.
                writebinary(filename, self.bytecode)
            else:
                filename = self.path
            playdoh_module = imp.load_compiled("playdoh_module", filename)
            
            if self.type == 'class':
                if len(self.args) > 0:
                    args = ["self.args[%d]" % i for i in xrange(len(self.args))]
                    args = args[:self.nargs]
                    strargs = ", ".join(args)
                else:
                    strargs = ""
                execstr = "self.fun = playdoh_module."+(self.name)+"("+strargs+")"
            elif self.type == 'function':
                execstr = "self.fun = playdoh_module."+(self.name)
            # Loads the function/initializes the object
            exec(execstr)
        
        if self.type == 'function':
            # Truncates the argument list to match the 
            # number of arguments of the function
            if len(funargs) < self.nargs:
                raise Exception("The function must have no more than %d arguments" % len(funargs))
            if len(funargs) > self.nargs:
                funargs = funargs[:self.nargs]
        
        # Evaluates the function
        return self.fun(*funargs)
