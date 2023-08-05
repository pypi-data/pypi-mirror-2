from numpy import exp

def fun(args):
    x = args['x']
    y = args['y']
    return exp(-(x**2+y**2))

if __name__ == '__main__':
    from playdoh import *
    optparams = dict(x = [-10.,10.], y = [-10.,10.])
    results = maximize(fun, optparams, max_cpu=2,
                       named_pipe=None, machines=['localhost'])
    print_results(results)
    