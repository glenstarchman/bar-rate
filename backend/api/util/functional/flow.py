from .monad import *
from .either import (Either, Left, Right)

class Try(Monad):

    def __init__(self, func):
        #lift out function into a Try monad
        self.func = liftF(func, Maybe)

    def __call__(self, *args, **kwargs):
        try:
            return Either(right = unlift(self.func(*args, **kwargs)))
        except Exception as e:
            return Either(left = unlift(e))

    #map over the right
    def rmap(self, func):
        self.right.map(func)

    #map over the left
    def lmap(self, func):
        self.left.map(func)

#lift a function to Try(function)
def liftT(func):
    return Try(func)
