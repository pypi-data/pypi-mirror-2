import numpy, playdoh
def fun(args):
    x = args['x']
    y = args['y']
    return numpy.exp(-(x**2+y**2))
        
if __name__ == '__main__':
    optparams = dict(x = [-10.,10.], y = [-10.,10.])
    results = playdoh.maximize(fun, optparams)
    playdoh.print_results(results)


#
#
#import numpy, playdoh
#def matinv(A):
#    return numpy.linalg.inv(A)
#
#if __name__ == '__main__':
#    A = 2*numpy.eye(2)
#    B = 4*numpy.eye(2)
#    invA, invB = playdoh.map(matinv, [A,B])
#    print invA
#    print invB
