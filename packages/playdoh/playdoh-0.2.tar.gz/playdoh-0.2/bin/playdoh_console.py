import sys, gc, time

max_cpu = None
max_gpu = None
named_pipe = None
finished = False

def extract_integer(name, arg):
    value = None
    if arg[0:len(name)] == name:
        try:
            value = int(arg[len(name)+1:])
        except Exception:
            value = None
#            print "Warning: %s must be an integer." % name
    return value

def extract_bool(name, arg):
    value = None
    if arg[0:len(name)] == name:
        value = arg[len(name)+1:]
        if value == "false":
            value = False
        if value == "true":
            value = True
    return value

for arg in sys.argv:
    if arg is "finished":
        finished = True
    if max_cpu is None:
        max_cpu = extract_integer('max_cpu', arg)
    if max_gpu is None:
        max_gpu = extract_integer('max_gpu', arg)
    if named_pipe is None:
        named_pipe = extract_bool('named_pipe', arg)
        
if __name__ == '__main__':
    from playdoh.clustertools import ClusterMachine
    
    print "Worker waiting for job..."
    sys.stdout.flush()
    machine = ClusterMachine(max_gpu=max_gpu, max_cpu=max_cpu,
                              print_pids = True,
                              named_pipe=named_pipe)
    machine.finished()
    del machine
    gc.collect()
    print "Finished"
    