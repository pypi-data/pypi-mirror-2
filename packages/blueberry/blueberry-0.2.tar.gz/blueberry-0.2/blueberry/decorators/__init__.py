# blueberry - Yet another Python web framework.
#
#       http://code.google.com/p/blueberrypy
#
# Copyright 2009 David Reynolds
#
# Use and distribution licensed under the BSD license. See
# the LICENSE file for full text.

from decorator import decorator

import formencode

from blueberry import request, response
from blueberry.utils.routing import url_for

# TODO: Rewrite these decorators to work with new routing method
"""
def https(meth):
    def wrapper(self, *args, **kwargs):
        # replacement for request.scheme
        # that works with proxy headers
        proto = request.protocol
        if proto == 'https':
            return meth(self, *args, **kwargs)

        if request.method.lower() == 'post':
            # don't allow posts
            self.abort(405)

        self.redirect(url_for(request.path_info, protocol='https'))

    return wrapper
"""

def validate(schema=None, form=None, post_only=True):
    def wrapper(func, self, *args, **kwargs):
        if request.environ['REQUEST_METHOD'] == 'GET':
            return func(self, *args, **kwargs)

        if post_only:
            params = request.POST.copy()
        else:
            params = request.params.copy()

        errors = {}
        values = {}

        if schema:
            try:
                self.defaults = schema.to_python(params)
            except formencode.Invalid, e:
                errors = e.error_dict
                values = e.value

        if errors:
            request.environ['REQUEST_METHOD'] = 'GET'

            self.defaults = values
            self.errors = errors

            if not form:
                return func(self, *args, **kwargs)

            request.environ['blueberry.routes_dict']['action'] = form
            # _dispatch_call doesn't exist
            resp = self._dispatch_call()
            form_content = resp
            resp = response

            if hasattr(form_content, '_exception'):
                return form_content
            return form_content

        return func(self, *args, **kwargs)
    return decorator(wrapper)
