from numpy import split, concatenate, ndarray, cumsum, ndim
from clustertools import ClusterManager, cluster_worker_script
from serializedfunction import SerializedFunction

__all__ = ['distribute', 'map', 'finished', 'shutdown', 'funworker']

class DistributedWorker(object):
    """
    Worker class for the ClusterManager object.
    
    Simply calls the function stored in ``shared_data['_fun']``
    with the arguments stored in ``job``.
    """
    def __init__(self, shared_data, use_gpu):
        self.shared_data = shared_data
    
    def process(self, job):
        # if shared_data only contains _fun, it means that the function
        # doesn't use shared_data.
        if len(self.shared_data)>1:
            result = self.shared_data['_fun'](job, self.shared_data)
        else:
            result = self.shared_data['_fun'](job)
        return result

class DistributedFunction(object):
    """
    Defines a distributed function from any function, allowing to execute it 
    transparently in parallel over several workers (multiple CPUs on a single machine
    or several machines connected in a network). 

    **Arguments**
    
    ``fun``
        The Python function to parallelize. There are two different ways of 
        parallelizing a function.
        * If ``fun`` accepts a single argument and returns a single object,
          then the distributed function can be called with a list of arguments
          that are transparently spread among the workers.
        * If ``fun`` accepts any D*N matrix and returns a N-long vector,
          in such a way that the computation is performed column-wise
          (that is, there exists a function f : R^d -> R such that
          ``fun(x)[i] == f(x[:,i])``), then the distributed function can be 
          called exactly like the original function ``fun`` : each worker 
          will call ``fun`` with a view on ``x``. The results are then 
          automatically concatenated, so that using the distributed
          function is strictly equivalent to using the original function.
    
    ``shared_data = None``
        Shared data is read-only. It should be a dictionary, whose values
        are picklable. If the values are numpy arrays, and the data is being
        shared to processes on a given computer, the memory will not be
        copied, but a pointer passed to the child processes, saving memory.
        Large read-only data to be shared should be put in here.
    
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
    
    ``accept_lists = False``
         Set to True if the provided function handles a list of any size as a parameter.
    
    ``endaftercall = True``
        Set to True to cleans up memory at the end of the first call to the 
        distributed function. Set to False if you plan to make several
        successive calls to the distributed function.
    
    ``verbose = False``
        Set to True to display information about the function evaluation.
    
    **Methods**
    
    ``__call__(x = None)``
        Calls the distributed function with the given parameter.
    
    ``finished()``
        Closes the manager and the workers on the local machine properly.
        
    ``shutdown()``
        Closes the manager and the workers on every machine properly.
    
    **Usage**
    
    You use the DistributedFunction object like this::
    
        dfun = DistributedFunction(fun, ...)
        y = dfun(x)
    
    which is a shorthand for::
        dfun = DistributedFunction(fun, ...)
        y = dfun.__call__(x)
    """
    def __init__(self,  fun = None,
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
                                      port = port,
                                      authkey = 'distopt') 
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
        
        **Arguments**
        
        ``n``
            The number of particles.
            
        **Returns**
        
        ``bins``
            The cumulative sum of ``workers_size``, starting from 0, where
            ``worker_size`` is the list of the number of particles for each worker.
        """
        worker_size = [n/self.numprocesses for _ in xrange(self.numprocesses)]
        worker_size[-1] = int(n-sum(worker_size[:-1]))
        
        bins = [0]
        bins.extend(list(cumsum(worker_size)))
        
        return bins

    def prepare_jobs(self, x):
        """
        Prepares the jobs to send to each worker.
        
        **Arguments**
        
        ``x``
            The argument passed to the distributed function.
        
        **Returns**
        
        ``jobs``
            The list of the arguments passed to the original function in each worker.
        ``ncalls``
            The number of function calls each worker does.
        """
        ncalls = 1
        if x is None:
            jobs = [None for _ in xrange(self.numprocesses)]
        elif isinstance(x, list):
            n = len(x)
            # Nothing to do if x is smaller than numprocesses
            if n <= self.numprocesses:
                jobs = x
            else:
                # If the function handles lists, then divide the list into sublists
                if self.accept_lists:
                    bins = self.divide(n)
                    jobs = [x[bins[i]:bins[i+1]] for i in xrange(self.numprocesses)]
                # Otherwise, performs several calls of the function on each worker
                # for each element in the list (default case)
                else:
                    jobs = []
                    job = []
                    for i in xrange(len(x)):
                        if len(job) >= self.numprocesses:
                            jobs.append(job)
                            job = []
                            ncalls += 1
                        job.append(x[i])
                    if len(job)>0:
                        jobs.append(job)
                    else:
                        ncalls -= 1
        elif isinstance(x, ndarray):
            d = ndim(x)
            if d == 0:
                jobs = [None for _ in xrange(self.numprocesses)]
            else:
                n = x.shape[-1]
                bins = self.divide(n)
                bins = bins[1:-1]
                jobs = split(x, bins, axis=-1)
                jobs = [job for job in jobs if len(job)>0]
        elif isinstance(x, dict):
            jobs = [dict([]) for _ in xrange(self.numprocesses)]
            for param, value in x.iteritems():
                subjobs = self.prepare_jobs(value)
                for i in xrange(self.numprocesses):
                    jobs[i][param] = subjobs
        return jobs, ncalls

    def __call__(self, x = None):
        """
        Sends evaluation function requests to each worker and concatenates the results
        """
        jobs, ncalls = self.prepare_jobs(x)
        if ncalls == 1:
            results = self.manager.process_jobs(jobs)
        else:
            if self.verbose:
                print "Using %d successive function calls on each worker..." % ncalls
            results = []
            for subjobs in jobs:
                # Concatenates the results in a list
                results.extend(self.manager.process_jobs(subjobs))
        if isinstance(x, ndarray):
            # Concatenates the results in a Numpy array.
            results = concatenate(results, axis=-1)
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

def distribute( fun = None,
                shared_data = None,
                max_cpu = None,
                max_gpu = None,
                gpu_policy = 'no_gpu',
                machines = [],
                named_pipe = None,
                port = None,
                accept_lists = False,
                endaftercall = True,
                verbose = False,
                ):
    """
    Defines a distributed function from any function, allowing to execute it 
    transparently in parallel over several workers (multiple CPUs on a single machine
    or several machines connected in a network). 

    **Arguments**
    
    ``fun``
        The Python function to parallelize. There are two different ways of 
        parallelizing a function.
        * If ``fun`` accepts a single argument and returns a single object,
          then the distributed function can be called with a list of arguments
          that are transparently spread among the workers.
        * If ``fun`` accepts any D*N matrix and returns a N-long vector,
          in such a way that the computation is performed column-wise
          (that is, there exists a function f : R^d -> R such that
          ``fun(x)[i] == f(x[:,i])``), then the distributed function can be 
          called exactly like the original function ``fun`` : each worker 
          will call ``fun`` with a view on ``x``. The results are then 
          automatically concatenated, so that using the distributed
          function is strictly equivalent to using the original function.
    ``shared_data = None``
        Shared data is read-only. It should be a dictionary, whose values
        are picklable. If the values are numpy arrays, and the data is being
        shared to processes on a given computer, the memory will not be
        copied, but a pointer passed to the child processes, saving memory.
        Large read-only data to be shared should be put in here.
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
    ``accept_lists = False``
         Set to True if the provided function handles a list of any size as a parameter.
    ``endaftercall = True``
        Set to True to cleans up memory at the end of the first call to the 
        distributed function. Set to False if you plan to make several
        successive calls to the distributed function.
    ``verbose = False``
        Set to True to display information about the function evaluation.
    """
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
    return dfun

def map(fun, args,
        shared_data = None,
        max_cpu = None,
        max_gpu = None,
        gpu_policy = 'no_gpu',
        machines = [],
        named_pipe = None,
        port = None,
        accept_lists = False,
        endaftercall = True,
        verbose = False):
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
    return dfun(args)

def finished(dfun):
    """
    Cleans up the memory on the current machine, but leaves the workers
    on the other machines running.
    """
    dfun.finished()

def shutdown(dfun):
    """
    Cleans up the memory on the current machine, and kills all workers
    on the other machines.
    """
    dfun.shutdown()

def funworker(max_cpu = None, max_gpu = None, named_pipe = None, port = None):
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
    distributed, then call ``funworker``. The script must be killed by hand
    at the end, unless you call ``shutdown(dfun)`` at the end of the manager script.
    """
    cluster_worker_script(DistributedWorker,
                          max_gpu=max_gpu, max_cpu=max_cpu, port=port,
                          named_pipe=named_pipe, authkey='distopt')

