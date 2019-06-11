# import inspect
from rest_framework.exceptions import MethodNotAllowed
from django.conf.urls import url
from ...models.get_taggable import *


def get_module_name(function):
    return function.__module__


def method_dispatch(**table):
    def invalid_method(request, *args, **kwargs):
        #logger.warning('Method Not Allowed (%s): %s', request.method, request.path,
        #    extra={
        #        'status_code': 405,
        #        'request': request
        #    }
        #)
        raise MethodNotAllowed(table.keys())

    def d(request, *args, **kwargs):
        handler = table.get(request.method, invalid_method)
        return handler(request, *args, **kwargs)
    return d


def build_taggable_urls():
    from ...views import taggable
    patterns = []
    for u in TAGGABLE_URLS:
        disp = "GET = taggable.get, PUT = taggable.put, DELETE = taggable.delete"
        d = eval("method_dispatch(%s)" % (disp))
        u2 = url(u['url'], d, u['extra'])
        patterns.append(u2)

    return patterns


def get_decorators(function):
    """from http://schinckel.net/2012/01/20/get-decorators-wrapping-a-function/"""
    # If we have no func_closure, it means we are not wrapping any other functions.
    if not function.__closure__:
        return [function]
    decorators = []
     # Otherwise, we want to collect all of the recursive results for every closure we have.
    for closure in function.__closure__:
        decorators.extend(get_decorators(closure.cell_contents))
    return [function] + decorators
