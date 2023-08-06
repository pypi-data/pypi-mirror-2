"""
Example usage of :func:`map` with a function that has module dependencies. 
"""
from playdoh import *

# Import an external module in the same folder
from external_module import external_fun

# The function to parallelize
def fun(x):
    # Use the function defined in the external module
    return external_fun(x)**2

# This line is required on Windows, any call to a Playdoh function
# must be done after this line on this OS.
# See http://docs.python.org/library/multiprocessing.html#windows
if __name__ == '__main__':
    # Execute ``fun(1)`` and ``fun(2)`` in parallel on two CPUs on this machine
    # and return the result.
    # The ``codedependencies`` argument contains the list of external Python modules
    # to transfer on the machines executing the task. It is only needed when using
    # remote machines, and not when using CPUs on the local machine.
    print map(fun, [1,2], codedependencies=['external_module.py'])

