import numpy, playdoh

def fun(args):
    return numpy.exp(-(args['x']**2+args['y']**2)) # Gaussian function

# This line is necessary for Windows users
if __name__ == '__main__':
    optparams = dict(x = [-10.,10.], y = [-10.,10.]) # We optimize over two parameters initially sampled over [-10,10]
    results = playdoh.maximize(fun, optparams) # results['x'] and results['y'] contain the best parameters
    playdoh.print_results(results)