from operator import floordiv, mod

def divde_exact(n,d):
    """ Return the quotient and remainder of divding N by D.
    >>> q,r = divde_exact(2013,10)
    >>> q
    201
    >>> r
    3
    """
    return floordiv(n,d), mod(n,d)

x = 3
def local_test():
    print(x)

def local_test2():
    print(x)
    x=44
    print(x)


