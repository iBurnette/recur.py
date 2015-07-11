"""
This plugin serves to provide similar functionality to clojure/clojurescript's
recur, which allows tail recursion optimization to take place in a hostile
environment (e.g. the Python interpreter).

Example usage:

@recur_anchor
def factorial(n, acc=1):
    if n == 0:
        return acc
    else:
        return recur(n-1, acc=(acc*n))

# Doesn't overflow the stack!
print factorial(30000)
"""

class RecurException:
    """
    Serves as the vessle for the updated arguments and the method with which we
    clear the stack of the most recent function call.
    """
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def recur_anchor(g):
    """
    Decorator that enables the use of recur() within a function. Use of recur()
    without this decorator will result in error.
    """
    def func(*args, **kwargs):
        while True:
            try:
                return g(*args, **kwargs)
            except RecurException, e:
                args = e.args
                kwargs = e.kwargs
    return func


def recur(*args, **kwargs):
    """
    Calling recur within a function (decorated with @recur_anchor) will run the
    parent function again with the updated parameters given to recur.
    """
    raise RecurException(args, kwargs)