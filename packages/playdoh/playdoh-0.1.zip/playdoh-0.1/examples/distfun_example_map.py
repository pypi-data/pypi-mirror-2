from numpy.linalg import inv
def fun(x):
    return inv(x)

if __name__ == '__main__':
    from numpy import eye, diag
    import playdoh
    
    A = diag([1,2])
    B = diag([3,4])
    invA, invB = playdoh.map(fun, [A,B], max_cpu=2)
    print invA
    print invB
    