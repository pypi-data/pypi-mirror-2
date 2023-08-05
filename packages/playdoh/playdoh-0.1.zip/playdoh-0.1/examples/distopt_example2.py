"""
Distributed optimization example 2
**********************************

This example shows more options of the optimization features.
There are two main differences compared to the first example :
- The variance of the Gaussian function is now a global (static) parameter
  stored in global memory,
- The center of the Gaussian is a local parameter, and we optimize independently
  two groups of particles that have different centers.
"""

"""
We define our fitness function. This time, we use ``shared_data`` to store
``sigma``, and ``local_data`` to store the center of the Gaussian.
"""
from numpy import exp
def fun(args, shared_data, local_data):
    a = args['a']
    b = args['b']
    try:
        a0 = local_data['a0']
        b0 = local_data['b0']
    except:
        a0 = b0 = 0
    sigma = shared_data['sigma']
    return exp(-((a-a0)**2+(b-b0)**2)/(2*sigma*2))

if __name__ == '__main__':
    """
    We define the parameters to optimize as in the first example.
    """
    optparams = dict(a = [-10.,10.], b = [-10.,10.])
    
    """
    We define the ``shared_data`` object, containing a single value for ``sigma``.
    """
    shared_data = dict(sigma = 1.0)
    
    """
    The optimization algorithm uses a given number of particles to find the global 
    maximum of the fitness function. This number is set with the ``group_size`` keyword.
    If several groups of particles are optimized simultaneously and independently, the 
    total number of particles is then ``group_size * group_count``.
    """
    group_size = 500
    
    """
    ``local_data`` contains the value of the local data for each group. Each
    value is a list with as many values as there are groups.
    """
    local_data = dict(a0 = [1.0, 2.0], b0 = [3.0, 4.0])
    
    """
    We now call the ``optimize`` function. We first pass the ``shared_data``
    and ``local_data`` dictionaries. The ``max_cpu`` keyword allows to limit
    the number of CPUs used on this machine for the optimization.
    The ``group_count`` argument gives the number of independent groups to
    optimize. If it is not set (or set to None), this number will be automatically
    infered from ``local_data``.
    The number of iterations of the optimization algorithm is set to 10 here.
    Finally, the ``verbose`` keyword allows to display information about the optimization
    in real time.
    """
    from playdoh import *
    results = maximize(fun, optparams, shared_data, local_data,
                       max_cpu = 2,
                       group_size = group_size, group_count = 2,
                       iterations = 10, verbose = True)
    
    """
    Finally, we print the results. There is one column per optimized group.
    Here, the optimization should find both (a=1,b=3) for the first group,
    and (a=2,b=4) for the second group. 
    """
    print_results(results)
    