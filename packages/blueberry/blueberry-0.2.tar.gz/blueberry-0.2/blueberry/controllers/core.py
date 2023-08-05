# blueberry - Yet another Python web framework.
#
#       http://code.google.com/p/blueberrypy
#
# Copyright 2009 David Reynolds
#
# Use and distribution licensed under the BSD license. See
# the LICENSE file for full text.

import types
import inspect

from webob.exc import HTTPException, HTTPNotFound

import blueberry

class WSGIController(object):

    def __call__(self, environ, start_response):
        response = self._dispatch_call()

        bb_response = blueberry.response._obj()

        if isinstance(response, str):
            bb_response.body = bb_response.body + response
        elif isinstance(response, unicode):
            bb_response.unicode_body = bb_response.unicode_body + response
        elif hasattr(response, 'wsgi_response'):
            for k, v in bb_response.headers.iteritems():
                # pass response headers to http response
                if k.lower() == 'set-cookie':
                    response.headers.add(k, v)
                else:
                    response.headers.setdefault(k, v)

            blueberry.response.set(response)
            bb_response = response
        elif response is None:
            # TODO: log something for the developer
            pass
        else:
            bb_response.app_iter = response
        response = bb_response

        return response(environ, start_response)

    def _dispatch_call(self):
        try:
            action = blueberry.request.environ['blueberry.routes_dict']['action']
        except KeyError:
            raise Exception("No action matched from Routes")

        func = getattr(self, action, None)

        if action != 'start_response' and callable(func):
            blueberry.request.environ['blueberry.action_method'] = func
            response = self._inspect_call(func)
        else:
            if blueberry.config['app']['debug']:
                raise NotImplementedError("Action %r not implemented" % action)
            response = HTTPNotFound()

        return response

    def _inspect_call(self, func):
        # TODO: argspec caching
        argspec = inspect.getargspec(func)
        kwargs = blueberry.request.environ['blueberry.routes_dict'].copy()

        args = {}
        if argspec[2]:
            args = kwargs
        else:
            i = isinstance(func, types.MethodType) and 1 or 0
            argnames = argspec[0][i:]
            for name in argnames:
                if name in kwargs:
                    args[name] = kwargs[name]

        try:
            result = func(**args)
        except HTTPException, httpe:
            result = httpe
            if result.wsgi_response.status_int == 304:
                result.wsgi_response.headers.pop('Content-Type', None)
            result._exception = True
        return result
