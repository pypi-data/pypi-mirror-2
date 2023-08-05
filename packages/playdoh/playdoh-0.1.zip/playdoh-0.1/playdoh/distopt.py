from clustertools import *
from optmanager import *
from optworker import *
from numpy import exp, ndarray, floor, log10
from serializedfunction import SerializedFunction
import inspect

__all__ = ['maximize', 'minimize', 'print_results', 'optworker']

def maximize(   fun, 
                optparams,
                shared_data = None,
                local_data = None,
                group_size = None,
                group_count = None,
                iterations = None,
                optinfo = None,
                machines = [],
                gpu_policy = 'no_gpu',
                max_cpu = None,
                max_gpu = None,
                named_pipe = None,
                port = None,
                returninfo = False,
                verbose = False,
                minimize = False
                ):
    """
    Optimizes a fitness function in parallel over several workers 
    (multiple CPUs on a single machine or several machines connected in a network). 

    **Arguments**
    
    ``fun``
        The fitness function. Its signature must be exactly the following::
        
            def fun(args, shared_data, local_data, use_gpu):
                ...
                return result
        
        * ``args`` is a dictionary containing the values of the parameters to 
          optimize. Each key is the parameter name as a string, each value is
          a Numpy vector containing the values of all the particles for this 
          parameter.
          
        * ``shared_data`` is a dictionary containing any data the function needs
          to evaluate the fitness function. This data must be shared by all the particles
          and can be stored in global memory for worker running on the same machine.
          The keys must be strings, and the values any picklable data (typically Numpy arrays).
          
        * ``local_data`` is only used when optimizing independently several groups of particles.
          The fitness function should be the same for each group, except that some parameters 
          (that are not optimized) change between the groups. These parameters are passed to
          the fitness function with the ``local_data`` argument. It is a dictionary which
          keys are parameter names, and values are lists containing the parameter values for each
          group. The lists must have the same length as the number of groups. 
          
        * ``use_gpu`` is a Boolean value indicating whether to use the GPU for the fitness
          evaluation. The manager decides whether to use the GPU or not, depending on if the GPU
          is present on this machine and/or the other machines. See the documentation about
          ``gpu_policy`` to know more.

    ``optparams``
        a dictionary : the keys are the parameter names, the values are 
        lists with two or four elements. If you don't want to set boundaries to the parameter,
        you just give two elements : the initial minimum and maximum values for the parameter.
        If you want to set boundaries, you give them in addition to the initial minimum and 
        maximum values.

    ``shared_data = None``
        Shared data is read-only. It should be a dictionary, whose values
        are picklable. If the values are numpy arrays, and the data is being
        shared to processes on a given computer, the memory will not be
        copied, but a pointer passed to the child processes, saving memory.
        Large read-only data to be shared should be put in here.
        Shared data is static over iterations.

    ``local_data = None``
        ``local_data`` is only used when optimizing independently several groups of particles.
        The fitness function should be the same for each group, except that some parameters 
        (that are not optimized) change between the groups. These parameters are passed to
        the fitness function with the ``local_data`` argument. It is a dictionary which
        keys are parameter names, and values are lists containing the parameter values for each
        group. The lists must have the same length as the number of groups. 
    
    ``group_size = None``
        The number of particles for each group.
    
    ``group_count = None``
        The number of independent groups to optimize in parallel.
    
    ``iterations = None``
        Number of iterations in the optimization algorithm.
    
    ``optinfo = None``
        A dictionary containing values about the optimization algorithm. It is specific
        to the optimization algorithm.
        
    ``max_cpu = None``
        An integer giving the maximum number of CPUs in the current machine that
        the package can use. Set to None to use all CPUs available.
        
    ``max_gpu = None``
        An integer giving the maximum number of GPUs in the current machine that
        the package can use. Set to None to use all GPUs available. By default,
        the GPU is not used, so this argument is used only in conjunction with 
        ``gpu_policy``.
        
    ``gpu_policy = no_gpu``
        The policies are 'prefer_gpu' which will use only GPUs if
        any are available on any of the computers, 'require_all' which will
        only use GPUs if all computers have them, or 'no_gpu' (default) which will
        never use GPUs even if available.
        
    ``machines=[]``
        A list of machine names to use in parallel.
        
    ``named_pipe``
        Set to ``True`` to use Windows named pipes for networking, or a string
        to use a particular name for the pipe.
        
    ``port``
        The port number for IP networking, you only need to specify this if the
        default value of 2718 is blocked.
    
    ``returninfo = False``
         Set to True if you want to retrieve information about the optimization at the end.
         In this case, call ``results, info = optimize(...)``.
    
    ``verbose = False``
        Set to True to display information about the optimization in real time.
    
    **Returns**
    
    ``results``
        A dictionary containing the best parameters found, and the corresponding fitness values.
        If there are several groups optimized independently, each value of the dictionary
        is a Numpy vector with the best parameters for each group.
    
    ``info``
        If ``returninfo = True``, it is a dictionary with information about the optimization.
        (TODO)
    """
    if group_size is None:
        group_size = 100
    
    if group_count is None:
        group_count = 1
    
    # Checks local_data
    if local_data is not None:
        for key, val in local_data.iteritems():
            if type(val) == list:
                if group_count == 1:
                    group_count = len(val)
                if len(val) != group_count:
                    raise Exception('Each local_data value must have as many elements as group_count')
            if type(val) == ndarray:
                if group_count == 1:
                    group_count = val.shape[-1]
                if val.shape[-1] != group_count:
                    raise Exception('The last dimension of each local_data array must be equal to group_count')
        
    if iterations is None:
        iterations = 10
    
    if shared_data is None:
        shared_data = dict([])
    
    if optinfo is None:
        optinfo = dict([])
    
    if optparams is None:
        raise Exception('optparams must be specified.')
    
    shared_data['_fun'] = SerializedFunction(fun)
    
    if named_pipe is False:
        named_pipe = None
    
    shared_data['_group_size'] = group_size
    shared_data['_group_count'] = group_count
    shared_data['_returninfo'] = returninfo
    shared_data['_optparams'] = optparams
    shared_data['_optinfo'] = optinfo
    shared_data['_verbose'] = verbose
    if minimize:
        shared_data['_minmax'] = "minimize"
    else:
        shared_data['_minmax'] = "maximize"
    
    # Adds iterations to optinfo
    optinfo['iterations'] = iterations
    
    # Creates the clusterinfo object
    clusterinfo = dict(machines = machines,
                        gpu_policy = gpu_policy,
                        max_cpu = max_cpu,
                        max_gpu = max_gpu,
                        named_pipe = named_pipe,
                        port = port)

    fm = OptManager(shared_data, local_data, clusterinfo, optinfo)
    fm.run()
    
    if returninfo:
        results, fitinfo = fm.get_results()
        r = results, fitinfo
    else:
        results = fm.get_results()
        r = results
    
    return r

def minimize(   fun, 
                optparams,
                shared_data = None,
                local_data = None,
                group_size = None,
                group_count = None,
                iterations = None,
                optinfo = None,
                machines = [],
                gpu_policy = 'no_gpu',
                max_cpu = None,
                max_gpu = None,
                named_pipe = None,
                port = None,
                returninfo = False,
                verbose = False,
                minimize = False
                ):
    return maximize(fun, 
                    optparams,
                    shared_data,
                    local_data,
                    group_size,
                    group_count,
                    iterations,
                    optinfo,
                    machines,
                    gpu_policy,
                    max_cpu,
                    max_gpu,
                    named_pipe,
                    port,
                    returninfo,
                    verbose,
                    minimize = True)

def optworker(max_cpu = None, max_gpu = None, port = None,
                      named_pipe = None):
    """
    Launches a worker on a machine and waits for jobs to be sent to it over the network.
    Allows to distribute a function over several machines in a network.
    
    **Arguments**
    
    ``max_cpu = None``
        An integer giving the maximum number of CPUs in the current machine that
        the package can use. Set to None to use all CPUs available.
    ``max_gpu = None``
        An integer giving the maximum number of GPUs in the current machine that
        the package can use. Set to None to use all GPUs available. By default,
        the GPU is not used, so this argument is used only in conjunction with 
        ``gpu_policy``.
    ``named_pipe = None``
        Set to ``True`` to use Windows named pipes for networking, or a string
        to use a particular name for the pipe.
    ``port = None``
        The port number for IP networking, you only need to specify this if the
        default value of 2718 is blocked.
    
    **Usage**
    
    Create a Python script which first import the function that is being
    distributed, then call ``optworker``. The script must be killed by hand
    at the end.
    """
    cluster_worker_script(OptWorker,
                          max_gpu=max_gpu, max_cpu=max_cpu, port=port,
                          named_pipe=named_pipe, authkey='distopt')

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
    if u is not 0:
        su = 'e'
        if u>0:
            su += '+'
        su += str(u)
    else:
        su = ''
    return s+su

def print_results(results, precision=4, colwidth=16):
    """
    Displays the results in a table.
    
    **Arguments**
    
    ``results``
        The results returned by the ``optimize`` function.
    
    ``precision = 4``
        The number of decimals to print for the parameter values.
    
    ``colwidth = 16``
        The width of the columns in the table.
    """
    group_count = len(results['fitness'])
    
    print "RESULTS"
    print '-'*colwidth*(group_count+1)
    
    print ' '*colwidth,
    for i in xrange(group_count):
        s = 'Group %d' % i
        spaces = ' '*(colwidth-len(s))
        print s+spaces,
    print
    
    def print_row(name, values):
        spaces = ' '*(colwidth-len(name))
        print name+spaces,
        for value in values:
            s = print_quantity(value)
            spaces = ' '*(colwidth-len(s))
            print s+spaces,
        print
    
    keys = results.keys()
    keys.sort()
    for key in keys:
        val = results[key]
        if key != 'fitness':
            print_row(key, val)
    
    print_row('fitness', results['fitness'])
    print 
    