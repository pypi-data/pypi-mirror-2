"""
Distributed function example : manager
**************************************

This example shows how to execute a distributed function in parallel over
several machines connected in a network.

The way it works is that there are a central machine (the manager) and several
worker machines. Each machine must have an identical copy of the code available
on it. The central machine runs a script which defines the function to distribute, 
and the workers run a much simpler script, essentially just calling the
``funworker`` function to set up the machine to listen for data
sent over the network and then run code when it receives the data. The manager
just calls the distributed function as with a single machine, but including an extra keyword
``machines`` with the list of connection details to the worker machines.
"""

"""
We define in the global namespace the function to distribute.
"""
from numpy import sum
def fun(x):
    return sum(x, axis=0)

if __name__ == '__main__':
    from numpy import ones
    from playdoh import *
    
    """
    We define here the distributed version of the function ``fun ``
    running over the machine where this script is executed and also
    on the machines which addresses are given in the ``machines`` keyword.
    The ``max_cpu=1`` argument limits the number of CPUs that are being used
    by the script on the current machine.
    """
    dfun = distribute(fun, max_cpu=1,
                           machines=['localhost'])
    
    """
    The rest of the script is similar than in the single machine examples.
    """
    x = ones((5,8))
    y = dfun(x)
    print y
    
    """
    At the end of this script, the memory is cleaned up on this computer,
    but the other computers are still running, so you can run this script several
    times with the other computers without restarting them.
    If you want to stop the other machines at distance, from this manager, you can 
    call ``shutdown(dfun)``.
    """
    