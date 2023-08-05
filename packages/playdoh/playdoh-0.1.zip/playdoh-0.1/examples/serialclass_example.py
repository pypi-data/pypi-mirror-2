from playdoh import SerializedFunction

class myclass(object):
    def __init__(self, y):
        self.y = y
    
    def __call__(self, x):
        return x+self.y

if __name__ == '__main__':
    o = myclass(3)
    print o(4)
    
    so = SerializedFunction(myclass, 3)
    print so(4)