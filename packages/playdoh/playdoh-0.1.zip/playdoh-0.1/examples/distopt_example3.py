"""
Distributed optimization example 3
**********************************

TODO
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
    def __call__(self, args):
        a = args['a']
        b = args['b']
        return exp(-((a-self.a0)**2+(b-self.b0)**2)/(2*self.sigma*2))

if __name__ == '__main__':
    optparams = dict(a = [-10.,10.], b = [-10.,10.])
    shared_data = dict(sigma = 1.0)
    group_size = 500
    local_data = dict(a0 = [1.0, 2.0], b0 = [3.0, 4.0])
    
    from playdoh import *
    results = maximize(myclass, optparams, shared_data, local_data,
                       max_cpu = 2,
                       group_size = group_size, group_count = 2,
                       iterations = 10, verbose = True)
    
    print_results(results)
    