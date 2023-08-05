from clustertools import *
from optmanager import *
from optworker import *
from numpy import exp, ndarray, floor, log10
from serializedfunction import SerializedFunction
import inspect

__all__ = ['maximize', 'minimize', 'printr']

def maximize(   fun, 
                _shared_data = None,
                _local_data = None,
                _group_size = None,
                _group_count = None,
                _iterations = None,
                _optinfo = None,
                _machines = [],
                _gpu_policy = 'no_gpu',
                _max_cpu = None,
                _max_gpu = None,
                _named_pipe = None,
                _port = None,
                _returninfo = False,
                _verbose = False,
                _minimize = False,
                _optalg = None,
                _doserialize = True,
                **optparams
                ):
    """
    Maximizes a fitness function in parallel over several workers 
    (multiple CPUs on a single machine or several machines connected in a network). 

    *Arguments* 
      * `fun`
        
        The fitness function's signature must be the following:
        
        {{{
            def fun(**args[, shared_data[, local_data[, use_gpu]]]):
                ...
                return result
        }}}
        
          * `**args` is a dictionary containing the values of the parameters to optimize. Each key is the parameter name as a string, each value is a Numpy vector containing the values of all the particles for this  parameter.
          
          * `shared_data` is a dictionary containing any data the function needs to evaluate the fitness function. This data must be shared by all the particles and can be stored in global memory for worker running on the same machine. The keys must be strings, and the values any picklable data (typically Numpy arrays).
          
          * `local_data` is only used when optimizing independently several groups of particles. The fitness function should be the same for each group, except that some parameters (that are not optimized) change between the groups. These parameters are passed to the fitness function with the `local_data` argument. It is a dictionary which keys are parameter names, and values are lists containing the parameter values for each group. The lists must have the same length as the number of groups. The `local_data` values passed in the fitness function are vectors of the same length than the number of particles on the current worker. The following extra keys are automatically and always available in `local_data` :
              * `local_data[_worker_size]` is the number of particles to evaluate on the current worker.
              * `local_data[_worker_index]` is the index of the current worker.
              * `local_data[_groups]` is a dictionary : the keys are the group indices, the values are the number of particles in the given group and worker.
          
          * `use_gpu` is a Boolean value indicating whether to use the GPU for the fitness evaluation. The manager decides whether to use the GPU or not, depending on if the GPU is present on this machine and/or the other machines. See the documentation about `gpu_policy` to know more.
        
        `fun` can also be a class : if processing the static data (`shared_data` and `local_data` that do not change between iterations) takes too long,
        then you can create a class like this :
        
        {{{
        class myclass(object):
            def __init__(self, shared_data, local_data, use_gpu):
                # ...
                pass
                
            def __call__(self, args):
                # ...
                pass
        }}}
        
        The constructor is called only at the beginning of the optimization, and at each iteration, `__call__` is called with the parameter values (particle positions).
        
      * `**optparams`
        a dictionary : the keys are the parameter names, the values are lists with two or four elements. If you don't want to set boundaries to the parameter, you just give two elements : the initial minimum and maximum values for the parameter. If you want to set boundaries, you give them in addition to the initial minimum and maximum values.
    
      * `_shared_data = None`
        Shared data is read-only. It should be a dictionary, whose values  are picklable. If the values are numpy arrays, and the data is being shared to processes on a given computer, the memory will not be copied, but a pointer passed to the child processes, saving memory. Large read-only data to be shared should be put in here. Shared data is static over iterations.
    
      * `_local_data = None`
        `local_data` is only used when optimizing independently several groups of particles. The fitness function should be the same for each group, except that some parameters (that are not optimized) change between the groups. These parameters are passed to the fitness function with the `local_data` argument. It is a dictionary which keys are parameter names, and values are lists containing the parameter values for each group. The lists must have the same length as the number of groups. 
    
      * `_group_size = None`
        The number of particles for each group.
    
      * `_group_count = None`
        The number of independent groups to optimize in parallel.
    
      * `_iterations = None`
        Number of iterations in the optimization algorithm.
    
      * `_optinfo = None`
        A dictionary containing values about the optimization algorithm. It is specific to the optimization algorithm.
        
      * `_optalg = None`
        The optimization algorithm class. The class must be defined in `playdoh.optalg`.
        
      * `_max_cpu = None`
        An integer giving the maximum number of CPUs in the current machine that the package can use. Set to None to use all CPUs available.
        
      * `_max_gpu = None`
        An integer giving the maximum number of GPUs in the current machine that the package can use. Set to None to use all GPUs available. By default, the GPU is not used, so this argument is used only in conjunction with `gpu_policy`.
        
      * `_gpu_policy = no_gpu`
        The policies are 'prefer_gpu' which will use only GPUs if any are available on any of the computers, 'require_all' which will only use GPUs if all computers have them, or 'no_gpu' (default) which will never use GPUs even if available.
        
      * `_machines=[]`
        A list of machine names to use in parallel.
        
      * `_named_pipe`
        Set to `True` to use Windows named pipes for networking, or a string to use a particular name for the pipe.
        
      * `_port`
        The port number for IP networking, you only need to specify this if the default value of 2718 is blocked.
    
      * `_returninfo = False`
         Set to True if you want to retrieve information about the optimization at the end. In this case, call `results, info = optimize(...)`.
    
      * `_verbose = False`
        Set to True to display information about the optimization in real time.

      * `_doserialize = True`
        Set to False if the function is importable on all the machines, set to True if not. In this case, the function will be fully serialized along with the byte code of the module where it is defined and the modules that are imported in that module, in a recursive fashion.
    """
    if _group_size is None:
        _group_size = 100
    
    if _group_count is None:
        _group_count = 1
    
    # Checks local_data
    if _local_data is not None:
        for key, val in _local_data.iteritems():
            if type(val) == list:
                if _group_count == 1:
                    _group_count = len(val)
                if len(val) != _group_count:
                    raise Exception('Each local_data value must have as many elements as group_count')
            if type(val) == ndarray:
                if _group_count == 1:
                    _group_count = val.shape[-1]
                if val.shape[-1] != _group_count:
                    raise Exception('The last dimension of each local_data array must be equal to group_count')
        
    if _iterations is None:
        _iterations = 10
    
    if _shared_data is None:
        _shared_data = dict([])
    
    if _optinfo is None:
        _optinfo = dict([])
    
    if optparams is None:
        raise Exception('optparams must be specified.')
    
    _shared_data['_fun'] = SerializedFunction(fun, _doserialize = _doserialize)
    
    if _named_pipe is False:
        _named_pipe = None
    
    _shared_data['_group_size'] = _group_size
    _shared_data['_group_count'] = _group_count
    _shared_data['_returninfo'] = _returninfo
    _shared_data['_optparams'] = optparams
    _shared_data['_optinfo'] = _optinfo
    _shared_data['_verbose'] = _verbose
    if _minimize:
        _shared_data['_minmax'] = "minimize"
    else:
        _shared_data['_minmax'] = "maximize"
    
    # Adds iterations to optinfo
    _optinfo['iterations'] = _iterations
    
    # Creates the clusterinfo object
    _clusterinfo = dict(machines = _machines,
                        gpu_policy = _gpu_policy,
                        max_cpu = _max_cpu,
                        max_gpu = _max_gpu,
                        named_pipe = _named_pipe,
                        port = _port)

    fm = OptManager(_shared_data, _local_data, _clusterinfo, _optinfo, _optalg)
    fm.run()
    
    if _returninfo:
        results, fitinfo = fm.get_results()
        r = results, fitinfo
    else:
        results = fm.get_results()
        r = results
    
    return r

def minimize(   fun, 
                _shared_data = None,
                _local_data = None,
                _group_size = None,
                _group_count = None,
                _iterations = None,
                _optinfo = None,
                _machines = [],
                _gpu_policy = 'no_gpu',
                _max_cpu = None,
                _max_gpu = None,
                _named_pipe = None,
                _port = None,
                _returninfo = False,
                _verbose = False,
                _minimize = False,
                _optalg = None,
                _doserialize = True,
                **optparams
                ):
    """
    Minimizes a function. See the reference of `maximize`, the arguments are the same.
    """
    return maximize(fun, 
                    _shared_data,
                    _local_data,
                    _group_size,
                    _group_count,
                    _iterations,
                    _optinfo,
                    _machines,
                    _gpu_policy,
                    _max_cpu,
                    _max_gpu,
                    _named_pipe,
                    _port,
                    _returninfo,
                    _verbose,
                    _minimize = True,
                    _optalg = _optalg,
                    _doserialize = _doserialize,
                    **optparams)

def print_quantity(x, precision=3):
    if x == 0.0:
        u = 0
    else:
        u = int(3*floor((log10(abs(x))+1)/3))
    y = float(x/(10**u))
    s = ('%2.'+str(precision)+'f') % y
    if (y>0) & (y<10.0):
        s = '  '+s
    elif (y>0) & (y<100.0):
        s = ' '+s
    if (y<0) & (y>-10.0):
        s = ' '+s
    elif (y<0) & (y>-100.0):
        s = ''+s
    if u is not 0:
        su = 'e'
        if u>0:
            su += '+'
        su += str(u)
    else:
        su = ''
    return s+su

def print_row(name, values, colwidth):
    spaces = ' '*(colwidth-len(name))
    print name+spaces,
    for value in values:
        s = print_quantity(value)
        spaces = ' '*(colwidth-len(s))
        print s+spaces,
    print
        
def printr(results, precision=4, colwidth=16):
    """
    Displays the results of an optimization in a table.
    
    *Arguments*
    
      * `results`
        The results returned by the `optimize` function.
    
      * `precision = 4`
        The number of decimals to print for the parameter values.
    
      * `colwidth = 16`
        The width of the columns in the table.
    """
    group_count = len(results['fitness'])
    
    print "RESULTS"
    print '-'*colwidth*(group_count+1)
    
    if group_count>1:
        print ' '*colwidth,
        for i in xrange(group_count):
            s = 'Group %d' % i
            spaces = ' '*(colwidth-len(s))
            print s+spaces,
        print
    
    keys = results.keys()
    keys.sort()
    for key in keys:
        val = results[key]
        if key != 'fitness':
            print_row(key, val, colwidth)
    
    print_row('fitness', results['fitness'], colwidth)
    print 
    