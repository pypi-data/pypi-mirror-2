import playdoh, time, multiprocessing
try:
    import import1
except:
    pass

glob = 6
machines = ['localhost']

def fun3(z):
    fun4 = import1.fun4
    return fun4(z)+fun4(2*z)

def fun2(z):
    return 3*fun1(z,z)+glob

def fun1(x,y):
    return x*y

def test1():
    r = playdoh.map(fun1, [1,2], [3,4], _max_cpu=1, _machines=machines)
    assert (r == [3, 8])

def test2():
    r = playdoh.map(fun2, [1, 2], _max_cpu=1, _machines=machines)
    assert (r == [9, 18])

def test3():
    r = playdoh.map(fun3, [1, 2], _max_cpu=1, _machines=machines)
    assert (r == [9, 18])

def run():
    test1()
    
    time.sleep(1)
    test2()
    
    time.sleep(1)
    test3()

if __name__ == '__main__':
    run()