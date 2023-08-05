"""
Distributed function example : worker
*************************************

This example shows how to execute a distributed function in parallel over
several machines connected in a network.

This script must be run on each machine except the one which runs the manager.

It is important to always place the code after ``if __name__ == '__main__':``
to avoid computer crashes on Windows.
"""
if __name__ == '__main__':
    """
    We import the funworker function, which listens to jobs to be sent over the network.
    """
    from playdoh import funworker
    
    """
    A single call to this function makes the machine waits for jobs to do, and
    execute it when requested.
    If your computers have an IP address and can accept incoming connections 
    (i.e. they are not behind a NAT firewall), you can use the IP address of this machine
    in the ``machines`` keyword in the manager. Otherwise, you should pass the keyword
    ``named_pipe=True`` in ``funworker`` here, and also on the manager, to use the named
    pipes feature of Windows networks.
    """
    funworker(max_cpu=1)
    
    """
    Now, this script is continuously running and can execute an infinite number of jobs,
    so you basically have nothing to do here. If you want to stop the script, you should
    kill the process manually. Also, you can kill all workers at distance from the manager
    using ``shutdown(dfun)``.
    """