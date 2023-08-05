"""
Distributed optimization example with multiple machines
*******************************************************

This example shows how to get started with Playdoh. You use playdoh.maximize
to maximize a function in parallel accross different machines.

You first need to launch the workers on every machine. Then, launch this script.
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
    We optimize over two parameters initially uniformly sampled in [-10,10]
    results is a dictionary. results['x'] and results['y'] contain the best parameters
    results['fitness'] contains the best fitness value
    _machines contains the list of the machine IPs
    """
    results = playdoh.maximize(fun, x = [-10.,10.], y = [-10.,10.],
                               _machines = ['localhost'],
                               _max_cpu=2)
    
    """
    We print the results
    """
    playdoh.printr(results)
    