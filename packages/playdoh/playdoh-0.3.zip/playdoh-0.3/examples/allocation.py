"""
Resource allocation example showing how to allocate manually resources on the servers.
The Playdoh server must run on the local machine and on the default port (2718 by default)
for this script to work.
"""
from playdoh import *

# It can also be a list of server IP addresses
servers = 'localhost'

# Allocate automatically the maximum number of resources on the specified servers
alloc = allocate(servers)

# alloc is an Allocation object, it can be used as a dictionary
for machine, count in alloc.iteritems():
    print "%d CPUs allocated on machine %s" % (count, str(machine))
    

