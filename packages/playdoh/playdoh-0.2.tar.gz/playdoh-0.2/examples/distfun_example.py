"""
Distributed function example
****************************

This example shows how to get started with Playdoh. You use playdoh.map
to distribute a function accross your different CPUs if you have a multicore machine.
"""

"""
The function to distribute
"""
def sum(a,b):
    return a+b

"""
Any playdoh instruction must be called after this line
"""
if __name__ == '__main__':
    import playdoh
    
    """
    playdoh.map works like the builtin Python map function, except that the function 
    is evaluated in parallel over several CPUs (all the CPUs available in the system 
    by default). Here, if two CPUs at least are available on the computer, each one 
    will compute a different job (1+3 for the first one, 2+4 for the second one).
    """
    print playdoh.map(sum, [1, 2], [3, 4])