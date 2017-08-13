""" Mathematical Library
"""
from math import sqrt
from numpy import shape, matrix, size, long, NaN, append

def pythagoras(*sites):
    """ calculates the pythagorean distance from a various number of arguments
    """
    res = 0
    for i in sites:
        res += i ** 2
    return sqrt(res)

def toVector(a, b, c, d='none'):
    """ transforms 3 or 4 scalars to a 3x1 numpy matrix
    """
    assert d == 'none' or isinstance(d, (int, long, float)), "Not a valid input for d"
    if isinstance(d, (int, long, float)) :
        vector = matrix([a, b, c, d])
    else: 
        vector = matrix([a, b, c])
    return vector.transpose()    
    

def toValue(mat):
    """ transforms a 3x1 numpy matrix to scalars
        same as x1, x2, x3 = numpy.matrix()
    """
    dim = shape(mat)
    assert (max(dim) == 3 or max(dim) == 4) and min(dim) == 1, "Not a 3 or 4 dimensional vector" 
    if dim[0] > dim[1]: mat = mat.transpose()
    a = mat[0, 0]
    b = mat[0, 1]
    c = mat[0, 2]
    if size(mat) == 4:
        d = mat[0, 3]
        return a, b, c, d
    else:
        return a, b, c

def resize(array1, array2):
    """ adjust the dimension of two arrays by appending NaN
    """
    if array1.shape > array2.shape:
        array2 = append(array2, NaN)
    elif array1.shape < array2.shape:
        array1 = append(array1, NaN)
    return array1, array2

def mvMultiplication(vector1, vector2):
    """ matrix-vector multiplication 
        returns a 4x1 vector
    """
    a, b, c, d = toValue(vector1)
    return matrix([[a, -b, -c, -d], [b, a, -d, c], [c, d, a, -b], [d, -c, b, a]]) * vector2
            
def runningAverage(old, new, weight):
    """ recursive running average
        old, new is either a scalar or vector 
        weight is the reciprocal of times this function was called
    """
    K = weight
    return old + K*(new - old)