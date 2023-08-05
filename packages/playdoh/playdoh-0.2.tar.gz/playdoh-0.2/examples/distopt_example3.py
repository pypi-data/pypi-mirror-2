"""
Distributed optimization example 3
**********************************

Same example as example 2, except that the function is wrapped inside a class.
This is useful because the function is called at each iteration of the optimization.
If the processing of global and static data (shared_data, local_data) is long,
you may want to do it only at the beginning of the optimization.
You define then a class where you process shared_data and local_data in the constructor,
and where the __call__ method is called at each iteration with the parameter values as
arguments.
"""

from numpy import exp
class myclass(object):
    def __init__(self, shared_data, local_data):
        self.sigma = shared_data['sigma']
        try:
            self.a0 = local_data['a0']
            self.b0 = local_data['b0']
        except:
            self.a0 = self.b0 = 0
    def __call__(self, a, b):
        return exp(-((a-self.a0)**2+(b-self.b0)**2)/(2*self.sigma*2))

if __name__ == '__main__':
    import playdoh
    
    shared_data = dict(sigma = 1.0)
    local_data = dict(a0 = [1.0, 2.0], b0 = [3.0, 4.0])
    
    results = playdoh.maximize(myclass, a = [-10.,10.], b = [-10.,10.],
                       _shared_data=shared_data, _local_data=local_data,
                       _max_cpu = 2,
                       _group_size = 500, _group_count = 2,
                       _iterations = 10, _verbose = True)
    
    playdoh.printr(results)
    