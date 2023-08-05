"""
Distributed function example 1
******************************

This example shows how to distribute a "one parameter-one result"-like function
over several workers.
"""

"""
We first define the function to distribute. It is required
to be defined at the top level of the module.
""" 
from numpy.linalg import inv
def fun(x):
    return inv(x)

"""
For Windows users, it is required that any code using Playdoh is placed after
this line, otherwise the system will crash!
"""
if __name__ == '__main__':
    from numpy import eye
    from playdoh import *

    """
    We import the library to have access to the ``distribute`` function,
    which is the main function used to distribute a function over multiple CPUs
    or machines.
    """
    
    """
    This is the most important instruction of this example. It defines a 
    distributed version of the Numpy ``inv`` function which inverses any square matrix.
    
    The first argument of ``distribute`` is the name of the function
    that is being distributed. This function must accept a single argument and return a
    single object.
    """
    fun = distribute(fun, max_cpu=2)
    
    """
    We define the two matrices that are going to be inversed in parallel.
    """
    A = 2*eye(3)
    B = 4*eye(3)
    
    """
    ``distinv`` is the distributed version of ``inv`` : it is called by passing
    a list of arguments. The original function ``inv`` is automatically called 
    once per argument in the list in a distributed fashion. The distributed function
    returns the list of the results of each call.
    
    The list can be of any size. If there are more arguments
    than workers, then each worker will process several arguments in series.
    Here, if there are two available CPUs in the system, the first CPU inverses
    A, the second inverses B. ``invA`` and ``invB`` contain the inverses of A and B.
    """
    invA, invB = fun([A,B])
    
    print invA
    print invB
    
    """
    That is the simplest way of distribute a function. It is used typically for
    functions that perform complex and costly operations on a single object.
    Distributing this function allows to perform the same operations on different
    objects in parallel.
    
    Go to quick example 2 to see how you can distribute Python functions that are
    already vectorized thanks to Numpy matrices operations.
    """