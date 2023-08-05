from clustertools import *
from optparams import OptParams
from optalg import *
from numpy import hstack
import sys

__all__ = ['OptWorker']

class OptWorker(object):
    def __init__(self, shared_data, use_gpu):
        """
        The Fitting worker manipulates the simulation and optimization features via
        the classes FittingSimulation and FittingOptimization.
        It initializes these objects at the first process_jobs() call.
        """
        self.shared_data = shared_data
        self.OptAlg = self.shared_data['_optalg']
        self.use_gpu = use_gpu
        if self.shared_data['_minmax'] == "maximize":
            self.sign = 1
        elif self.shared_data['_minmax'] == "minimize":
            self.sign = -1
        else:
            raise Exception("minmax must be 'maximize' or 'minimize'")
    
    def process(self, (call, job)):
        """
        Calls the correct function according to the process_jobs() call occurence.
        """
        if call == 'prepare':
            # job contains the local worker data
            result = self.prepare(job)
        if call == 'iterate':
            # job is 'global_state' (a dictionnary specific to the optimization
            # algorithm).
            result = self.iterate(job)
        if call == 'terminate':
            result = self.terminate()
        sys.stdout.flush()
        return result
    
    def prepare(self, local_data):
        """
        Creates the Simulation and Optimization objects with both shared data
        and local data. The shared data is passed in the constructor of the worker,
        while the local data is passed at the first process_jobs() call in the manager.
        """
        self.local_data = local_data
        self.groups = self.local_data['_groups']
        
        # These variables are available
#        local['worker_size'] 
#        local['worker_index']
        self.fun = self.shared_data['_fun']
        if self.fun.type == 'class':
            self.fun.setpersistent(self.shared_data, self.local_data, self.use_gpu)
        
        """
        There is one optimization object per group within each worker. The 
        FittingWorker object should take care
        of calling once the FittingSimulation object to compute the fitness
        values of every particle within the worker. Then, in each group, 
        the optimization update iteration is executed, one after the other.
        """
        # Generates the initial state matrix
        self.fp = OptParams(**self.shared_data['_optparams'])
        initial_param_values = self.fp.get_initial_param_values(self.local_data['_worker_size'])
        X0 = self.fp.get_param_matrix(initial_param_values)
        Xmin, Xmax = self.fp.set_constraints()
        
        # Initializes the OptAlg objects (once per group)
        self.opts = dict([])
        k = 0
        for group in self.groups.keys():
            n = self.groups[group]
            self.opts[group] = self.OptAlg(self.local_data['_worker_index'],
                                      X0[:,k:k+n], Xmin, Xmax,
                                      self.shared_data['_optinfo'],
                                      self.shared_data['_returninfo'])
            k += n
        
    def iterate(self, global_states):
        """
        Optimization iteration. The global states of the groups are passed and the function returns
        the new local states. The new global state, used at the next iteration,
        is computed by the manager from the local states of every worker.
        global_states is a dictionary containing the global states for each group inside the worker.
        """
        local_states = dict([])
        
        # Compute the fitness values for all the particles inside the worker.
        X = hstack([self.opts[group].X for group in self.groups.keys()])
        param_values = self.fp.get_param_values(X)
        
        if self.fun.type == 'class':
            r = self.fun(**param_values)
        elif self.fun.type == 'function':
            r = self.fun(shared_data = self.shared_data, 
                         local_data = self.local_data, 
                         use_gpu = self.use_gpu,
                         **param_values)
        
        if self.shared_data['_returninfo']:
            fitness, self.siminfo = r
        else:
            fitness = r
            self.siminfo = None
        
        # Splits the fitness values according to groups
        k = 0
        for group, global_state in global_states.iteritems():
            n = self.groups[group] # Number of particles in the group
            # Iterates each group in series
            # self.sign = -1 if minimize
            local_states[group] = self.opts[group].iterate(self.sign*fitness[k:k+n], global_state)
            k += n
        
        # Returns a dictionary (group, local state)
        return local_states
        
    def terminate(self):
        """
        Returns fitting info at the end
        """
        results = dict([(group, self.opts[group].return_result()) for group in self.groups.keys()])
        fitinfo = dict([])
        fitinfo['sim'] = self.siminfo
        fitinfo['opt'] = dict([(group, self.opts[group].terminate()) for group in self.groups.keys()])
        return results, fitinfo

    