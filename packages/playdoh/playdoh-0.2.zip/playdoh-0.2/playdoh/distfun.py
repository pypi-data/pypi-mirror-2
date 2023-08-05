import numpy, os, sys, subprocess
from numpy import split, concatenate, array, ndarray, cumsum, ndim
from clustertools import ClusterManager, cluster_worker_script
from serializedfunction import SerializedFunction, _cachedir
#from processtools import Popen, PIPE

__all__ = ['map']

class DistributedWorker(object):
    """
    Worker class for the ClusterManager object.
    
    Simply calls the function stored in `shared_data['_fun']`
    with the arguments stored in `job`.
    """
    def __init__(self, shared_data, use_gpu):
        self.shared_data = shared_data
        self.use_gpu = use_gpu
    
    def process(self, (args, kwds)):
        result = self.shared_data['_fun'](shared_data = self.shared_data, 
                                          use_gpu = self.use_gpu,
                                          *args, **kwds)
        return result

class DistributedFunction(object):
    """
    Defines a distributed function from any function, allowing to execute it 
    transparently in parallel over several workers (multiple CPUs on a single machine
    or several machines connected in a network). 

    *Arguments*
    
      * `fun`
        The Python function to parallelize. It must accept a single argument and return a single object. The distributed function can then be called with a list of arguments that are transparently spread among the workers.

      * `shared_data = None`
        Shared data is read-only. It should be a dictionary, whose values are picklable. If the values are numpy arrays, and the data is being shared to processes on a given computer, the memory will not be copied, but a pointer passed to the child processes, saving memory. Large read-only data to be shared should be put in here.
      
      * `max_cpu = None`
        An integer giving the maximum number of CPUs in the current machine that the package can use. Set to None to use all CPUs available.
      
      * `max_gpu = None`
        An integer giving the maximum number of GPUs in the current machine that the package can use. Set to None to use all GPUs available. By default, the GPU is not used, so this argument is used only in conjunction with `gpu_policy`.
      
      * `gpu_policy = no_gpu`
        The policies are 'prefer_gpu' which will use only GPUs if any are available on any of the computers, 'require_all' which will only use GPUs if all computers have them, or 'no_gpu' (default) which will never use GPUs even if available.
      
      * `machines=[]`
        A list of machine names to use in parallel.
      
      * `named_pipe`
        Set to `True` to use Windows named pipes for networking, or a string to use a particular name for the pipe.
      
      * `port`
        The port number for IP networking, you only need to specify this if the default value of 2718 is blocked.
      
      * `accept_lists = False`
         Set to True if the provided function handles a list of any size as a parameter.
      
      * `endaftercall = True`
        Set to True to cleans up memory at the end of the first call to the distributed function. Set to False if you plan to make several successive calls to the distributed function.
      
      * `verbose = False`
        Set to True to display information about the function evaluation.
    
    *Methods*
    
      * `__call__(x = None)`
        Calls the distributed function with the given parameter.
    
      * `finished()`
        Closes the manager and the workers on the local machine properly.
        
      * `shutdown()`
        Closes the manager and the workers on every machine properly.
    
    *Usage*
    
    You use the DistributedFunction object like this:
    
    {{{
        dfun = DistributedFunction(fun, ...)
        y = dfun(x)
    }}}
    
    which is a shorthand for:
    
    {{{
        dfun = DistributedFunction(fun, ...)
        y = dfun.__call__(x)
    }}}
    """
    def __init__(self,  fun,
                        shared_data = None,
                        max_cpu = None,
                        max_gpu = None,
                        gpu_policy = 'no_gpu',
                        machines = [],
                        named_pipe = None,
                        port = None,
                        accept_lists = False,# Set to True if the provided function handles a list as a parameter
                        endaftercall = True,
                        verbose = False,
                        ):
        """
        Creates a ClusterManager object and prepares each worker to receive
        data and function evaluation requests.
        """
        if fun is None:
            raise Exception('The function must be provided')
        
        if shared_data is None:
            shared_data = dict([])
        
        self.endaftercall = endaftercall
        self.verbose = verbose
        # Shared data contains a serializable object containing the byte code of the function
        # as a Python list of bytes so that it can be fully pickled 
        shared_data['_fun'] = SerializedFunction(fun)
        self.manager = ClusterManager(DistributedWorker, 
                                      shared_data = shared_data,
                                      machines = machines,
                                      gpu_policy = gpu_policy,
                                      own_max_cpu = max_cpu,
                                      own_max_gpu = max_gpu,
                                      named_pipe = named_pipe,
                                      port = port)
        
        self.numprocesses = self.manager.total_processes
        self.accept_lists = accept_lists
        
        if verbose:
            # Displays the number of cores used
            if self.manager.use_gpu:
                cores =  'GPU'
            else:
                cores = 'CPU'
            if self.numprocesses > 1:
                b = 's'
            else:
                b = ''
            print "Using %d %s%s..." % (self.numprocesses, cores, b)

    def divide(self, n):
        """
        Defines the repartition of the resources for each worker.
        
        *Arguments*
        
        `n`
            The number of particles.
            
        *Returns*
        
        `bins`
            The cumulative sum of `workers_size`, starting from 0, where
            `worker_size` is the list of the number of particles for each worker.
        """
        worker_size = [n/self.numprocesses for _ in xrange(self.numprocesses)]
        worker_size[-1] = int(n-sum(worker_size[:-1]))
        
        bins = [0]
        bins.extend(list(cumsum(worker_size)))
        
        return bins

    def prepare_jobs(self, *args, **kwds):
        """
        Prepares the jobs to send to each worker.
        
        *Arguments*
        
        `*args`
            The arguments passed to the distributed function.
        
        `**kwds`
            The keywords passed to the distributed function.
        
        *Returns*
        
        `jobs`
            The list of the arguments passed to the original function in each worker.
            `jobs[i]` is a pair (args, kwds).
            
        `ncalls`
            The number of function calls for each worker.
        """
        ncalls = 1
        
        # Find the number of tuples of arguments (number of jobs)
        if len(args)>0:
            n = len(args[0])
        elif len(kwds)>0:
            n = len(kwds[kwds.keys()[0]])
        else:
            raise Exception("The function should have at least one argument.")
        
        jobs = []
        
        if self.accept_lists:
            bins = self.divide(n)
            job = []
            for i in xrange(self.numprocesses):
                locarg = []
                lockwd = dict([])
                for arg in args:
                    locarg = arg[bins[i]:bins[i+1]]
                for key,val in kwds.iteritems():
                    lockwd[key] = val[bins[i]:bins[i+1]]
                job.append((locarg, lockwd))
            jobs.append(job)
        else:
            job = []
            for i in xrange(n):
                if len(job) >= self.numprocesses:
                    jobs.append(job)
                    job = []
                    ncalls += 1
                locarg = [] # the list of arguments for job i
                lockwd = dict([]) # the dict of keywords for job i
                for arg in args:
                    locarg.append(arg[i])
                for key,val in kwds.iteritems():
                    lockwd[key] = val[i]
                job.append((locarg, lockwd))
            if len(job)>0:
                jobs.append(job)
            else:
                ncalls -= 1

#        if x is None:
#            jobs = [None for _ in xrange(self.numprocesses)]
#        elif isinstance(x, list):
#            n = len(x)
#            # Nothing to do if x is smaller than numprocesses
#            if n <= self.numprocesses:
#                jobs = x
#            else:
#                # If the function handles lists, then divide the list into sublists
#                if self.accept_lists:
#                    bins = self.divide(n)
#                    jobs = [x[bins[i]:bins[i+1]] for i in xrange(self.numprocesses)]
#                # Otherwise, performs several calls of the function on each worker
#                # for each element in the list (default case)
#                else:
#                    jobs = []
#                    job = []
#                    for i in xrange(n):
#                        if len(job) >= self.numprocesses:
#                            jobs.append(job)
#                            job = []
#                            ncalls += 1
#                        job.append(x[i])
#                    if len(job)>0:
#                        jobs.append(job)
#                    else:
#                        ncalls -= 1
##        elif isinstance(x, ndarray):
##            d = ndim(x)
##            if d == 0:
##                jobs = [None for _ in xrange(self.numprocesses)]
##            else:
##                n = x.shape[-1]
##                bins = self.divide(n)
##                bins = bins[1:-1]
##                jobs = split(x, bins, axis=-1)
##                jobs = [job for job in jobs if len(job)>0]
#        elif isinstance(x, dict):
#            jobs = [dict([]) for _ in xrange(self.numprocesses)]
#            for param, value in x.iteritems():
#                subjobs = self.prepare_jobs(value)
#                for i in xrange(self.numprocesses):
#                    jobs[i][param] = subjobs
        return jobs, ncalls

    def __call__(self, *args, **kwds):
        """
        Sends evaluation function requests to each worker and concatenates the results
        """
        jobs, ncalls = self.prepare_jobs(*args, **kwds)
        if ncalls == 1:
            results = self.manager.process_jobs(jobs[0])
        else:
            if self.verbose:
                print "Using %d successive function calls on each worker..." % ncalls
            results = []
            for subjobs in jobs:
                # Concatenates the results in a list
                results.extend(self.manager.process_jobs(subjobs))
#        if isinstance(x, ndarray):
#            # Concatenates the results in a Numpy array.
#            results = concatenate(results, axis=-1)
        # Closes the workers after the first call to the distributed function
        if self.endaftercall:
            self.finished()
        return results
        
    def finished(self):
        """
        Cleans up the memory and closes the workers on the machine. Should always be called
        at the end of any script.
        """
        self.manager.finished()
        
    def shutdown(self):
        """
        Cleans up the memory and closes the workers on *every* machine.
        """
        self.manager.completelyfinished()

def map(fun, *args, **kwds
#        shared_data = None,
#        max_cpu = None,
#        max_gpu = None,
#        gpu_policy = 'no_gpu',
#        machines = [],
#        named_pipe = None,
#        port = None,
#        accept_lists = False,
#        endaftercall = True,
#        verbose = False,
         ):
    """
    Executes a function with a list of parameters in parallel over several workers 
    (multiple CPUs on a single machine or several machines connected in a network). 
    
    *Arguments*
    
      * `fun`
        The Python function to parallelize. It must accept a single argument and return a single object.
        Any module import must be done outside the function (in the top-level module).
      
      * `*args`
        The arguments to evaluate the function on. Each argument is a list with the values to use for each different job.  
        
      * `**kwds`
        The keywords to evaluate the function on. Each keyword is a list with the values to use for each different job.

      * `_shared_data = None`
        Shared data is read-only. It should be a dictionary, whose values are picklable. If the values are numpy arrays, and the data is being shared to processes on a given computer, the memory will not be copied, but a pointer passed to the child processes, saving memory. Large read-only data to be shared should be put in here.
      
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
      
      * `_accept_lists = False`
         Set to True if the provided function handles a list of any size as a parameter.

      * `_verbose = False`
        Set to True to display information about the function evaluation.
    """
    
    # Checks that all arguments have the same number of elements
    m = []
#    try:
    for arg in args:
        m.append(len(arg))
    for key,arg in kwds.iteritems():
        if key[0] is not '_':
            m.append(len(arg))
#    except:
#        raise Exception("Each argument must be a list")
    m = array(m)
    if min(m) < max(m):
        raise Exception("All arguments must have the same number of elements")
    
    if '_shared_data' in kwds.keys():
        shared_data = kwds['_shared_data']
        del kwds['_shared_data']
    else:
        shared_data = None
    if '_max_cpu' in kwds.keys():
        max_cpu = kwds['_max_cpu']
        del kwds['_max_cpu']
    else:
        max_cpu = None
    if '_max_gpu' in kwds.keys():
        max_gpu = kwds['_max_gpu']
        del kwds['_max_gpu']
    else:
        max_gpu = 0
    if '_gpu_policy' in kwds.keys():
        gpu_policy = kwds['_gpu_policy']
        del kwds['_gpu_policy']
    else:
        gpu_policy = 'no_gpu'
    if '_machines' in kwds.keys():
        machines = kwds['_machines']
        del kwds['_machines']
    else:
        machines = []
    if '_named_pipe' in kwds.keys():
        named_pipe = kwds['_named_pipe']
        del kwds['_named_pipe']
    else:
        named_pipe = None
    if '_port' in kwds.keys():
        port = kwds['_port']
        del kwds['_port']
    else:
        port = None
    if '_accept_lists' in kwds.keys():
        accept_lists = kwds['_accept_lists']
        del kwds['_accept_lists']
    else:
        accept_lists = None
    if '_endaftercall' in kwds.keys():
        endaftercall = kwds['_endaftercall']
        del kwds['_endaftercall']
    else:
        endaftercall = True
    if '_verbose' in kwds.keys():
        verbose = kwds['_verbose']
        del kwds['_verbose']
    else:
        verbose = None
    
    dfun = DistributedFunction( fun = fun,
                                shared_data = shared_data,
                                max_cpu = max_cpu,
                                max_gpu = max_gpu,
                                gpu_policy = gpu_policy,
                                machines = machines,
                                named_pipe = named_pipe,
                                port = port,
                                accept_lists = accept_lists,
                                endaftercall = endaftercall,
                                verbose = verbose)
    
    return dfun(*args, **kwds)
