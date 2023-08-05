"""
Distributed optimization example 1
**********************************

This example shows how to optimize a simple function over a single computer
and multiple CPUs.

The optimization feature of Playdoh allows you to find the parameters
that maximize any function you provide in a distributed fashion.
We assume that you already have such a function, which works in
a vectorized way thanks to Numpy matrices operations.
 
To use the optimization feature, you should follow these three steps :

1.  Your fitness function depends probably on a lot of different parameters.
    You should start by defining which ones you want to optimize and which ones
    are constant.
2.  Write the fitness function using the signature imposed by Playdoh.
3.  Call ``optimize`` to launch the optimization over several CPUs, GPUs
    or machines and retrieve the results !
"""

"""
Let's start with a quick example. It consists in maximizing a simple fitness function
which is a bidimensional centered Gaussian function.
There are two parameters to fit here : ``x`` and ``y``.
The ``optimize`` function has to find 0 for the two parameters, since ``(x=0,y=0)`` 
corresponds to the global maximum of the fitness function.
"""

"""
The first thing to do is to write the fitness function::
"""
from numpy import exp
def fun(args):
    x = args['x']
    y = args['y']
    return exp(-(x**2+y**2))

"""
The function accepts a dictionary containing the parameter values as an argument. 
Here, ``x`` and ``y`` are
Numpy vectors containing the values of each particle. The function returns the fitness
values of all particles (note that we're using vectorized matrices operations with ``+``
and ``**``).
"""

"""
For Windows users, it is required that any code using Playdoh is placed after
this line, otherwise the system will crash!
"""
if __name__ == '__main__':
    
    """  
    Now we define some information about the parameters to optimize::
    """
    optparams = dict(x = [-10.,10.], y = [-10.,10.])
    
    """
    ``optparams`` is a dictionary : each key is a parameter name, each value is a list
    containing the initial minimum and maximum values to use at the beginning of the
    optimization algorithm. The initial positions of the particles are uniformly sampled
    in these intervals.
    
    Finally, we're launching the optimization on all CPUs available on the machine::
    """
    from playdoh import *
    results = maximize(fun, optparams, max_cpu=1)
    print_results(results)

    """
    The variable ``results`` is a dictionary containing the best value for each parameter
    found by the optimization algorithm. This last statement should give you values very close
    to 0 for both ``x`` and ``y``, along with a corresponding fitness value very close to 1.
    """
