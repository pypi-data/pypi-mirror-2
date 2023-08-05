"""
Distributed optimization example
********************************

This example shows how to get started with Playdoh optimization. You use playdoh.maximize
to maximize a function accross your different CPUs if you have a multicore machine.
"""

"""
Gaussian function
"""
import numpy
def fun(x,y):
    return numpy.exp(-(x**2+y**2))

"""
Any playdoh instruction must be called after this line
"""
if __name__ == '__main__':
    import playdoh
    
    """
    We optimize fun with two parameters initially uniformly sampled in [-10,10].
    'results' is a dictionary. results['x'] and results['y'] contain the best parameters
    results['fitness'] contains the best fitness value
    """
    results = playdoh.maximize(fun, x = [-10.,10.], y = [-10.,10.])
    
    """
    We print the results
    """
    playdoh.printr(results)