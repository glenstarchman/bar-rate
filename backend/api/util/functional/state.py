from .monad import *
from .either import Both
from .flow import Try


class Union(Monad):
    """a monad that supports two values"""
    pass

class State(Both):

    def __init__(self, accumulator = Nothing, exception = Nothing):
        self.__exception = exception
        self.__accumulator = accumulator
        super(State, self).__init__((exception, accumulator,))

    def set_state(self, value):
        return State(self.__exception, value)

    def get_state(self):
        return self.value
