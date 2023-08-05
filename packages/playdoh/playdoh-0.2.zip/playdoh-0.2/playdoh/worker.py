from clustertools import cluster_worker_script, ClusterMachine
import gc, sys

__all__ = ['worker', 'simple_worker']

def worker(max_cpu = None, max_gpu = None, named_pipe = None, port = None):
    """
    Launches a worker on a machine and waits for jobs to be sent to it over the network.
    Allows to distribute a function over several machines in a network.
    
    *Arguments*
    
      * `max_cpu=None`
        If specified, ensures that this machine will use at most that number of
        CPUs, otherwise it will use the maximum number.
        
      * `max_gpu=None`
        If specified, ensures that this machine will use at most that number of
        GPUs, otherwise it will use the maximum number.
        
      * `port=None`
        The port number to communicate with if using IP, should be the same on
        all machines.
        
      * `named_pipe=None`
        Set to `True` if using Windows named pipes, or a string to choose a
        particular pipe name. Should be the same on all machines.
    
    *Usage*
    
    When you run this function, it enters an infinite job queue, and the machine
    is ready to receive  and process jobs from the manager. 
    """
    cluster_worker_script(max_gpu=max_gpu, max_cpu=max_cpu, port=port,
                          named_pipe=named_pipe)

def simple_worker(max_cpu = None, max_gpu = None, named_pipe = None, n = 1, verbose = True):
    """
    Launches a worker on a machine and waits for jobs to be sent to it over the network.
    Allows to distribute a function over several machines in a network. Run only one job.
    
    *Arguments*
    
      * `max_cpu=None`
        If specified, ensures that this machine will use at most that number of
        CPUs, otherwise it will use the maximum number.
        
      * `max_gpu=None`
        If specified, ensures that this machine will use at most that number of
        GPUs, otherwise it will use the maximum number.
        
      * `port=None`
        The port number to communicate with if using IP, should be the same on
        all machines.
        
      * `named_pipe=None`
        Set to `True` if using Windows named pipes, or a string to choose a
        particular pipe name. Should be the same on all machines.
    
      * `n=1`
        The number of jobs to run before terminating.
    
      * `verbose=True`
        Print information about the running jobs.
    
    *Usage*
    
    When you run this function, it waits for a job to be sent by the manager, then
    processes it and terminates.
    """
    for i in xrange(n):
        if verbose:
            print "Worker waiting for job %d..." % (i+1)
            sys.stdout.flush()
        machine = ClusterMachine(max_gpu=max_gpu, max_cpu=max_cpu,
                                  named_pipe=named_pipe)
        machine.finished()
        del machine
        gc.collect()
        if verbose:
            print "Finished"

if __name__ == '__main__':
    simple_worker(max_cpu=1)
    