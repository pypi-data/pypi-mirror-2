from playdoh import SerializedFunction

def fun(x):
    return x**2

if __name__ == '__main__':
    print fun(3)
    sfun = SerializedFunction(fun)
    print sfun(3)