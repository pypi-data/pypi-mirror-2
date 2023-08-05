from decorator import decorator

from blueberry import request

def dispatch_on(**method_map):
    """Works like pylons @rest.dispatch_on"""
    def dispatcher(func, self, *args, **kwargs):
        alt_method = method_map.get(request.method)
        if alt_method:
            alt_method = getattr(self, alt_method)
            return self._inspect_call(alt_method)
        return func(self, *args, **kwargs)
    return decorator(dispatcher)
