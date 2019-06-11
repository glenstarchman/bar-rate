import functools

def curried(n):
    def curry(fn):
        def _inner(*args):
            if len(args) < n:
                return curried(n - len(args))(functools.partial(fn, *args))
            return fn(*args)
        return _inner
    return curry
