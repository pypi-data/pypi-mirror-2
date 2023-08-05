"""
Example with global variables : you can define global variables in your script
and use them in your function.
"""
y = 10

def fun(x):
    return x+y

if __name__ == '__main__':
    import playdoh
    print playdoh.map(fun, [4,5,6,7])
    