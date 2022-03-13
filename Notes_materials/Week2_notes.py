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


# higher-order functions
## use function as an arguement in a function
def identity(k):
    return k

def cube(k):
    return pow(k,3)  # pow(a,b) will return a ** b

def summation(n, term):
    """
    Sum the first N terms of a sequence
    summation(5, cube) is 1**3 + 2**3 + 3**3 + 4**3 + 5**3
    >>> summation(5,cube)
    225
    """
    total,k = 0,1  # why while? =_= why not for loop, you may slip to an infinite loop using while 
    while k <= n:
        total,k = total+term(k), k+1
    return total

def sum_naturals(n):
    """
    Sum the first N natural numbers.
    sum_naturals(5) is 1+2+3+4+5
    >>> sum_naturals(5) 
    15
    """
    return summation(n,identity)

def sum_cubes(n):
    """
    Sum the first N cubes of natural numbers
    >>> sum_cubes(5)
    225
    """
    return summation(n,cube)

## a function return another function
def make_adder(n):
    """
    make_adder(1)(2) 
    make_adder(1) is a function, because make_adder return a function
    >>> add_three = make_adder(3)
    >>> add_three(4)
    7
    """ 
    def adder(k):
        return k+n
    return adder


## inverse function
def search(f):
    x=0
    while True:
        if f(x):
            return(x)
        x+=1

def positive(x):
    return(max(0,x*x - 100))

def inverse(f):
    # return g(y) such that g(f(x)) -> x
    return lambda y: search(lambda x: f(x) ==y)
    