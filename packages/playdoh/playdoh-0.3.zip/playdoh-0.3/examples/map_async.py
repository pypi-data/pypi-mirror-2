"""
Example usage of the asynchronous version of :func:`map`.
"""
from playdoh import *
import time

# The function to parallelize
def fun(x):
    # Simulate a 1 second long processing
    time.sleep(1)
    return x**2

# This line is required on Windows, any call to a Playdoh function
# must be done after this line on this OS.
# See http://docs.python.org/library/multiprocessing.html#windows
if __name__ == '__main__':
    # Execute ``fun(1)`` and ``fun(2)`` in parallel on two CPUs on this machine.
    # The ``map_async`` function returns immediately a ``Task`` object
    # which allows to get the results later.
    task = map_async(fun, [1,2], cpu=2)
    
    # Get the job results
    print task.get_result()
