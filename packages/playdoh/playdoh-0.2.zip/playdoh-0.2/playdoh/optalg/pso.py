from numpy import inf, ones, zeros, tile, ones, histogram, nonzero, isscalar, maximum, minimum
from numpy.random import rand

class PSO(object):
    def __init__(self, worker_index,
                       X0,
                       Xmin = None,
                       Xmax = None,
                       optinfo = None,
                       returninfo = False):
        self.worker_index = worker_index
        self.optinfo = optinfo
        
        if not 'omega' in self.optinfo.keys():
            self.optinfo['omega'] = .9
        if not 'cl' in self.optinfo.keys():
            self.optinfo['cl'] = 1.2
        if not 'cg' in self.optinfo.keys():
            self.optinfo['cg'] = 1.8
        
        self.returninfo = returninfo
        if not(self.returninfo):
            self.info = None # contains the information about the run
        else:
            self.info = dict([])
        
        self.D, self.N = X0.shape
        self.X = X0
        self.V = zeros((self.D, self.N))
        
        # Boundaries
        if Xmin is None:
            Xmin = -inf*ones(self.D)
        if Xmax is None:
            Xmax = inf*ones(self.D)
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.Xmin = tile(Xmin.reshape((-1,1)), (1, self.N))
        self.Xmax = tile(Xmax.reshape((-1,1)), (1, self.N))
        
        # Preparation of the optimization algorithm
        self.fitness_lbest = -inf*ones(self.N)
        self.fitness_gbest = -inf
        self.X_lbest = self.X
        self.X_gbest = None
        
        if self.returninfo:
            self.info['fitness_matrix'] = None
        
    def iterate(self, fitness, global_state):
        if global_state is not None:
            self.X_gbest, self.fitness_gbest = global_state
            
        
        # Local update
        indices_lbest = nonzero(fitness > self.fitness_lbest)[0]
        if (len(indices_lbest)>0):
            self.X_lbest[:,indices_lbest] = self.X[:,indices_lbest]
            self.fitness_lbest[indices_lbest] = fitness[indices_lbest]
        
        # Global update
        max_fitness = fitness.max()
        if max_fitness > self.fitness_gbest:
            index_gbest = nonzero(fitness == max_fitness)[0]
            if not(isscalar(index_gbest)):
                index_gbest = index_gbest[0]
            self.X_gbest = self.X[:,index_gbest]
            self.fitness_gbest = max_fitness
            
        # Creates the local state
        local_state = (self.X_gbest, self.fitness_gbest)
        
        # State update
        rl = rand(self.D, self.N)
        rg = rand(self.D, self.N)
        X_gbest_expanded = tile(self.X_gbest.reshape((-1,1)), (1, self.N))
        self.V = self.optinfo['omega']*self.V + self.optinfo['cl']*rl*(self.X_lbest-self.X) + self.optinfo['cg']*rg*(X_gbest_expanded-self.X)
        self.X = self.X + self.V
        
        # Boundary checking
        self.X = maximum(self.X, self.Xmin)
        self.X = minimum(self.X, self.Xmax)
        
        # Record histogram at each iteration, for each group within the worker
        if self.returninfo:
            (hist, bin_edges) = histogram(fitness, 100, range=(0.0,1.0))
            self.info["fitness_matrix"].append(list(hist))
                
#        print "new iteration", self.worker_index
#        print "    Fitness: mean %.3f, max %.3f, std %.3f" % (fitness.mean(), fitness.max(), fitness.std())
        
        return local_state
    
    @staticmethod
    def combine_local_states(local_states):
        """
        Combines the local states of every worker and returns the global state.
        """
        X_gbest_global = None
        fitness_gbest_global = -inf
        for local_state in local_states:
            X_gbest, fitness_gbest = local_state
            if fitness_gbest > fitness_gbest_global:
                X_gbest_global = X_gbest
                fitness_gbest_global = fitness_gbest
        return (X_gbest_global, fitness_gbest_global)
     
    @staticmethod
    def get_best_fitness((X_gbest_global, fitness_gbest_global)):
        return fitness_gbest_global
     
    def terminate(self):
        """
        Returns the optimization info if requested, and clears the memory.
        """
        return self.info

    def return_result(self):
        """
        Return the best position and the best fitness.
        """
        return self.X_gbest, self.fitness_gbest