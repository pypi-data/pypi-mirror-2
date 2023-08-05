import playdoh, time, multiprocessing
import import1

glob = 6

def fun3(z):
    fun4 = import1.fun4
    return fun4(z)+fun4(2*z)

def fun2(z):
    return 3*fun1(z,z)+glob

def fun1(x,y):
    return x*y

def test1():
    r = playdoh.map(fun1, [1,2], [3,4], _max_cpu=1, _machines=['localhost'])
    assert (r == [3, 8])

def test2():
    r = playdoh.map(fun2, [1, 2], _max_cpu=1, _machines=['localhost'])
    assert (r == [9, 18])

def test3():
    r = playdoh.map(fun3, [1, 2], _max_cpu=1, _machines=['localhost'])
    assert (r == [9, 18])

def run():
    
    p = multiprocessing.Process(target=playdoh.simple_worker, 
                                kwargs=dict(max_cpu=1, n=3, verbose=False))
    p.start()
    time.sleep(.5)

    test1()
    time.sleep(.5)
    
    test2()
    time.sleep(.5)
    
    test3()
    time.sleep(.5)
    
    if p:
        p.terminate()

if __name__ == '__main__':
    run()