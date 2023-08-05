import inspect, cPickle, sys, imp, struct, os.path, py_compile

__all__ = ['readbinary', 'writebinary']

def readbinary(filename):
    """
    Converts a binary file into a Python list of chars so that it can
    be pickled without problem.
    """
    binfile = open(filename, 'rb')
    datalist = []
    intsize = struct.calcsize('c')
    while 1:
        data = binfile.read(intsize)
        if data == '':
            break
        num = struct.unpack('c', data)
        datalist.append(num[0])
    binfile.close()
    return datalist

def writebinary(filename, datalist):
    """
    Writes data stored in datalist (returned by readbinary) into filename.
    """
    binfile = open(filename, 'wb')
    for char in datalist:
        data = struct.pack('c', char)
        binfile.write(char)
    binfile.close()
    return
