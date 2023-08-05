from numpy import ones, inf

__all__ = ['OptAlg']

class OptAlg(object):
    def __init__(self, worker_index,
                       X0,
                       Xmin = None,
                       Xmax = None,
                       optparams = None,
                       returninfo = False):
        """
        Distributed optimization algorithm.
        
        This class allows to implement an optimization algorithm in a distributed
        fashion. The fitness function is a function f : Y=f(X), where X is a
        D*N matrix, and Y a N-long vector. The dimension of the parameter space
        is D. The fitness function is evaluated in parallel over N particles.
        
        Definition: a particle is a point in the parameter space.
        
        We suppose that there are K decoupled workers. Each one calls the fitness
        function in parallel over different sets of particles. Then, each worker
        runs the update iteration step of the optimization algorithm, using
        only the fitness values of its particles, and makes only its particles evolve.
        
        When each worker terminates this step, it returns to a global manager an 
        object called local_state. The manager collects the local states of each
        worker, computes a new object from these, called global state, and sends
        it back to each worker. The idea is that each worker should know the 
        state of the particles in the other workers, without knowing the fitness
        values of each one of them, which would not be efficient (the workers
        communicate with a potentially high time lag). The local state is then
        the minimal information about the evolution of the particles in the worker
        that the other workers should know about. In the example of the PSO algorithm,
        the local state is the best position reached by the particles within the worker.
        The global state is computed from the local states of every worker by taking
        again the best position among these positions.
        
        There is one FittingOptimization object per worker.
        
        The FittingOptimization class *must* implement the following methods.
        
        *Methods*
    
        `__init__(self, worker_index, X0, Xmin, Xmax, optparams, returninfo)`.
          * `worker_index` is the index of the worker.
          * `X0` is the initial state DxN matrix.
          * `Xmin` is the minimal values for each parameter (boundaries). It is a D-long vector. Same thing for `Xmax`.
          * `optparams` is a dictionary containing optimization parameters, specific to the optimization algorithm.
          * `returninfo` is a boolean expressing whether information about a run of the algorithm should be returned at the end of the optimization or not.
            
            The purpose of this method is to initialize the object (the state matrix, etc.)
        
        `iterate(self, fitness, global_state)`
            The main function of the class : performs one iteration of the optimization
            algorithm. `fitness` is a N-long vector containing the fitness values
            of the particles at the end of the previous iteration (or at the initialization 
            if it is the first iteration). We have `fitness=f(X)` if `X` is 
            the state matrix. `global_state` is an object containing the merged
            information about the local states of every worker at the end
            of the previous iteration. It is returned by `combine_local_states()`.
            The `iterate` function must return the local state of the worker at 
            the end of the iteration.
        
        `terminate(self)`
            Terminates the optimization and returns the information about the run if requested in the parameter `returninfo`.
        
        `return_result(self)`
            Returns the best position and the best fitness value as a tuple.
        
        `combine_local_states(local_states)`
            This *static* method is used to combine the local states of every worker
            and return a global state `global_state` from them. The global state is 
            then sent by the manager to each worker at the next iteration.
          
        `get_best_fitness(global_state)`
            This *static* method is used to retrieve the best particle position and fitness
            from the global state. It returns a tuple `(particle_position, fitness)`
            where `particle_position` is a D-long vector, and `fitness` is a scalar.
        
        *Instructions to implement a new distributed optimization algorithm*
        
          1. Copy this file into `[your algorithm name].py` in the folder `playdoh/optalg/`.
        
          2. Choose the structure of the local objects. It can be a dictionary for example. Define precisely the items names and data types. This object should contain the minimal information about the current particles and their fitness values needed to perform the next iteration. It should be as light as possible since it will be transfered twice for each worker at each iteration inside a network.
        
          3. Write the `combine_local_states()` function. It takes the list of the local states of every worker as arguments, and returns the global state.
        
          4. Complete the `__init__()` function by defining the variables needed for the optimization algorithm. The `optparams` argument of the constructor (a dictionary) should be used to let the user change some optimization parameters.
        
          5. Write the `iterate()` function. Use the fitness values given as an argument and also the global state from the last iteration to perform the current iteration. Return the new local state at the end.
        
          6. Complete the `terminate()` function if needed.
        """
        self.worker_index = worker_index
        self.optparams = optparams
        self.returninfo = returninfo
        self.info = None # contains the information about the run
        
        self.D, self.N = X0.shape
        self.X = X0
        
        # Boundaries
        if Xmin is None:
            Xmin = -inf*ones(self.D)
        if Xmax is None:
            Xmax = inf*ones(self.D)
        self.Xmin = Xmin
        self.Xmax = Xmax
        # TODO: preparation of the optimization algorithm
    
    def iterate(self, fitness, global_state):
        """
        Iteration step of the optimization algorithm. `fitness` here
        is the vector of the fitness values for the particles in the worker.
        `global_state` is the information about the last iteration for all workers
        that each worker should know in order to perform its next iteration step.
        This function must return `local_state` at the end of the iteration.
        """
        local_state = None
        # TODO: iterate the algorithm and return local_state
        return local_state
    
    @staticmethod
    def combine_local_states(local_states):
        """
        Combines the local states of every worker and returns the global state.
        """
        global_state = None
        # TODO: combine the local_states into global_state
        return global_state
    
    @staticmethod
    def get_best_fitness(global_state):
        """
        Returns the best fitness value.
        """
        # TODO
        return fitness_gbest_global
     
    def terminate(self):
        # TODO: terminates the optimization
        return self.info
        
    def return_result(self):
        """
        Return the best position and the best fitness.
        """
        return self.X_gbest, self.fitness_gbest