"""
Example of :func:`maximize` with a fitness function accepting arrays
rather than keyword arguments.
"""
from playdoh import *
import numpy

def fun(x):
    if x.ndim == 1:
        x = x.reshape((1,-1))
    result = numpy.exp(-(x**2).sum(axis=0))
    return result

if __name__ == '__main__':
    # State space dimension (D)
    dimension = 4
    
    # ``initrange`` is a Dx2 array with the initial intervals for every dimension 
    initrange = numpy.tile([-10.,10.], (dimension,1))
    
    # Maximize the fitness function in parallel
    results = maximize(fun,
                       popsize = 10000, # size of the population
                       maxiter = 10, # maximum number of iterations
                       cpu = 1, # number of CPUs to use on the local machine
                       initrange = initrange)
    
    # Display the final result in a table
    print_table(results)
    