from collections import Iterable

class EmptyMonad:
    def __init__(self):
        self.value = None

    def __repr__(self):
        return "<Nothing>"

    def is_empty(self): return True

#the Nothing singleton
Nothing = EmptyMonad()

class Monad(object):
    """Basic Monadic operations"""
    def __init__(self, value = None):
        self.value = value

    def __call__(self, *args, **kwargs):
        return Nothing if self is Nothing \
            else self.__class__(self.value(*args, **kwargs))

    def __getattr__(self, name):
        return Nothing if self is Nothing \
            else self.__class__(getattr(self.value, name))


    def __rshift__(self, fn):
        """Monad >> func => Monad[func_return]"""
        if self is Nothing:
            return Nothing
        else:
            if not hasattr(fn, '__is_wrapped__'):
                fn = liftF(fn, self.__class__)
            return fn(self.value)

    def get(self):
        if self is Nothing: return None
        else: return self.value

    def get_or_else(self, other = None):
        if other == None: other = Nothing
        v = self.get()
        if v: return v
        else: return other

    def get_option(self, other = Nothing):
        return Maybe(self.get_or_else(other))

    def is_empty(self):
        if self is Nothing: return True
        else: return False

    def has_value(self): return not self.is_empty()

    def identity(self):
        return self.value

    def unit(self): return self

    def map(self, func):
        if self is Nothing: return Nothing
        f = None
        if not hasattr(func, '__is_wrapped__'): f = liftF(func, self.__class__)
        else: f = func
        f = func
        if isinstance(self.value, Iterable) and not isinstance(self.value, str):
            return self.__class__([f(x) for x in self])
        else:
            return self.__class__(f(self))

    def flat_map(self, func):
        if self is Nothing: return Nothing
        return unlift(self.map(func))

    #recursively flatten a Monad until all we have is the inner value
    def flatten(self):
        if self is None: return None
        if isinstance(self.value, Monad):
            return self.value.flatten()
        else:
            return self

#a la Haskell's Maybe or Scala's Option
class Maybe(Monad):

    class __metaclass__(type):

        ops = ['add', 'radd', 'sub', 'rsub', 'mul', 'div', 'mod', 'eq', 'ne', 'lt', 'gt']

        def __new__(mcs, name, bases, dct):
            import operator

            def reverse(fn):
                wrapper = lambda x, y: fn(y, x)
                wrapper.__name__ = fn.__name__
                wrapper.__doc__ = fn.__doc__
                return wrapper

            for opname in mcs.ops:
                op = getattr(operator, opname)
                dct['__' + opname + '__'] = lift(op)
                dct['__r' + opname + '__'] = lift(reverse(op))

            return type.__new__(mcs, name, bases, dct)


    def __repr__(self):
        return '<Nothing>' if self is Nothing else '<Just[%s]: %s>' % (type(self.value).__name__, repr(self.value))

    def __str__(self):
        return '' if self is Nothing else self.value

    def __add__(self, other):
        if self is Nothing or other is Nothing: return Nothing
        if not hasattr(self.value, '__add__'): return Nothing
        if isinstance(other, self.__class__):
            return self.__class__(self.value + other.value)
        return self.__class__(self.value + other)

    def __radd__(self, other):
        return self.__add__(other)

#alias for Maybe[SomeVal]
Just = Maybe

class IteratorLikeMonad(Monad):

    def __getitem__(self, key_or_slice):
        return Nothing if self is Nothing \
            else self.__class__(self.value.__getitem__(key_or_slice))

    def head(self):
        return self.value[0]

    def head_option(self):
        return lift(self.value[0], Maybe)

    def tail(self):
        return self.value[-1]

    def tail_option(self):
        return lift(self.value[-1], Maybe)

    def length(self):
        return len(self.value)

class StringMonad(IteratorLikeMonad):

    def __repr__(self):
        return "<StringMonad: '%s'>" % (self.value)

class NumericMonad(Monad):

    def __or__(self, other):
        if other is Nothing:
            return self
        if self is Nothing:
            return lift(other, self.__class__)
        else:
            return self

    def __nonzero__(self):
        return False if self is Nothing else bool(self.value)


    def __sub__(self, other):
        if self is Nothing or other is Nothing: return Nothing
        if not hasattr(self.value, '__sub__'): return Nothing
        if isinstance(other, self.__class__):
            return self.__class__(self.value - other.value)
        return self.__class__(self.value - other)

    def __rsub__(self, other):
        if not other is self.__class__: other = lift(other, self.__class__)
        return other.__sub__(self)



class List(IteratorLikeMonad, Iterable):

    def __repr__(self):
        return "<List: '%s'>" % (repr(self.value))
    def __iter__(self):
        return iter(self.value)

    def __getitem(self, slice_or_index):
        return self.value(slice_or_index)


def unlift(value):
    from .monad import Monad, Nothing
    if value is Nothing: return None
    elif isinstance(value, Monad): return value.value
    else: return value

def lift(value, monad):
    tname = type(value).__name__
    if tname == 'function' or tname == 'builtin_function_or_method':
        return liftF(value, monad)
    else:
        return liftV(value, monad)


def liftF(fn, monad):

    """lift a function to Maybe monad

    Converts a plain function to one that can accept Maybe arguments
    (positional or keyword) and returns a Maybe return value.

    The returning function returns Nothing if any of the arguments is Nothing.
    Otherwise, it returns Just(<return value of the original function>).

    The converted function accepts both Maybe (which are unpacked) and
    non-Maybe arguments (which are used as-is).

    Examples:

    >>> maybe_abs = lift(abs)
    >>> maybe_abs(Just(-1))
    Just(1)
    >>> maybe_abs(Nothing)
    Nothing
    >>> maybe_abs(0)
    Just(0)

    """
    from .monad import Nothing

    def wrapper(*args, **kwargs):
        def lift_arg(arg):
            return arg.value if isinstance(arg, monad) else arg

        largs = []
        for arg in args:
            #if arg is Nothing:
            #    return Nothing
            #else:
            largs.append(lift_arg(arg))
        lkwargs = {}
        for k, v in kwargs.items():
            #if v is Nothing:
            #    return Nothing
            #else:
            lkwargs.append(lift_arg(arg))
        return monad(fn(*largs, **lkwargs))
    try:
        wrapper.__name__ = fn.__name__
        wrapper.__doc__ = fn.__doc__
        wrapper.__is_wrapped__ = True
    except: pass
    return wrapper

def liftV(value, monad = Maybe):
    """lift a value to a Maybe monad"""
    if monad == None: monad = Maybe
    if value == None: return Nothing
    else: return value if isinstance(value, monad) else monad(value)

def liftM(value):
    tname = type(value).__name__
    if tname == 'function' or tname == 'builtin_function_or_method':
        return liftF(value, Maybe)
    else:
        return liftV(value, Maybe)

#IS functions
def is_monad(value):
    return isinstance(value, Monad) or isinstance(value, Nothing)

def is_maybe(value):
    return isinstance(value, Maybe)

def is_either(value):
    return isinstance(value, Either)

def is_try(value):
    from .flow import Try
    return isinstance(value, Try)

"""lift a value to a Maybe"""
def liftVM(value):
    return liftV(value, Maybe)

#lift a function to a maybe
def liftFM(func):
    return liftF(func, Maybe)
