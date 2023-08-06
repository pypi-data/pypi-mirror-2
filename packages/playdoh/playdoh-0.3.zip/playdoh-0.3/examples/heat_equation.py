"""
PDE parallel numerical solver.
This example shows how to numerically solve the heat equation on a square
in parallel. 
"""
from playdoh import *
from numpy import *
from pylab import *

# Any task class must derive from the ParallelTask
class HeatSolver(ParallelTask):
    def initialize(self, X, dx, dt, iterations):
        # X is a matrix with the function values and the boundary values
        # X must contain the borders of the neighbors ("overlapping Xs")
        self.X = X 
        self.n = X.shape[0]
        self.dx = dx
        self.dt = dt
        self.iterations = iterations
        self.iteration = 0

    def send_boundaries(self):
        # Send boundaries of the grid to the neighbors
        if 'left' in self.tubes_out:
            self.push('left', self.X[:,1])
        if 'right' in self.tubes_out:
            self.push('right', self.X[:,-2])
    
    def recv_boundaries(self):
        # Receive boundaries of the grid from the neighbors
        if 'right' in self.tubes_in:
            self.X[:,0] = self.pop('right')
        if 'left' in self.tubes_in:
            self.X[:,-1] = self.pop('left')
    
    def update_matrix(self):
        # Implement the numerical scheme for the PDE
        Xleft, Xright = self.X[1:-1,:-2], self.X[1:-1,2:]
        Xtop, Xbottom = self.X[:-2,1:-1], self.X[2:,1:-1]
        self.X[1:-1,1:-1] += self.dt*(Xleft+Xright+Xtop+Xbottom-4*self.X[1:-1,1:-1])/self.dx**2

    def start(self):
        # Run the numerical integration of the PDE
        for self.iteration in xrange(self.iterations):
            log_info("Iteration %d/%d" % (self.iteration+1, self.iterations))
            self.send_boundaries()
            self.recv_boundaries()
            self.update_matrix()
    
    def get_result(self):
        # Return the result
        return self.X[1:-1,1:-1]

def heat2d(n, iterations, nodes = None, machines = []):
    # Default allocation
    allocation = allocate(machines=machines, cpu=nodes)
    nodes = len(allocation)
    
    # ``split`` is the grid size on each node, without the boundaries
    split = [(n-2)*1.0/nodes for _ in xrange(nodes)]
    split = array(split, dtype=int)
    split[-1] = n-2-sum(split[:-1])
    
    dx=2./n
    dt = dx**2*.2
    
    # y is a Dirac function at t=0
    y = zeros((n,n))
    y[n/2,n/2] = 1./dx**2
    
    # Split y horizontally
    split_y = []
    j = 0
    for i in xrange(nodes):
        size = split[i]
        split_y.append(y[:,j:j+size+2])
        j += size
    
    # Define a double linear topology 
    topology = []
    for i in xrange(nodes-1):
        topology.append(('right', i, i+1))
        topology.append(('left', i+1, i))
    
    # Start the task
    task = start_task(HeatSolver, # name of the task class
                      topology=topology,
                      allocation=allocation,
                      args=(split_y, dx, dt, iterations)) # arguments of the ``initialize`` method
                                     
    # Retrieve the result, as a list with one element returned by ``MonteCarlo.get_result`` per node
    result = task.get_result()
    result = hstack(result)
    
    return result

if __name__ == '__main__':
    result = heat2d(50, 50, nodes=MAXCPU-1)
#    hot()
#    imshow(result)
#    show()
    