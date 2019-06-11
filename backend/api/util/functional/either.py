from .monad import *

class Left(Maybe):

    def is_left(self): return True
    def is_right(self): return False

class Right(Maybe):

    def is_left(self): return False
    def is_right(self): return  True

class Either(Monad):
    def __init__(self, right = None, left = None):
        if left and right:
            raise(Exception("Either must be either right or left, not both"))
        self.__left = left
        self.__right = right
        val = self.__right if self.__right else self.__left
        super(Either, self).__init__(val)

    def __str__(self):
        if self.is_left():
            return "<Left: %s>" % (str(self.__left))
        else:
            return "<Right: %s>" % (str(self.__right))

    def __rshift__(self, fn):
        """Monad >> func => Monad[func_return]"""
        if self is Nothing:
            return Nothing
        else:
            v = self.right if self.is_right() else self.left
            fn = liftF(fn, self.__class__)
            return unlift(fn(v))

    def is_left(self): return self.__left is not None
    def is_right(self): return self.__right is not None
    def valid(self): return self.is_right()

    @property
    def right(self):
        if self.is_right():
            return Right(self.__right)
        else:
            return Nothing

    @property
    def left(self):
        if self.is_left(): return Left(self.__left)
        else: return Nothing

    #override for get
    def get(self):
        if self.is_right(): return self.right
        else: return self.left

    def map(self, func):
        """we cheat here a bit and auto-select the projection"""
        if self.is_right(): return self.right.map(func)
        if self.is_left(): return self.left.map(func)

    def flat_map(self, func):
        return self.map(func)

    def as_option(self):
        if self.is_right(): return Maybe(unlift(self.right))
        else: return Nothing


#Both is a special Either where both slots can have values
#it inherits all either functions and has a right bias
class Both(Either):
    def __init__(self, left = None, right = None):
        self.__left = left
        self.__right = right
        val = (self.__left, self.__right,)
        super(Both, self).__init__(right = val)
