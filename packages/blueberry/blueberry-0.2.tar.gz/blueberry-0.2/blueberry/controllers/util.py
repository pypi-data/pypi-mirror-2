# blueberry - Yet another Python web framework.
#
#       http://code.google.com/p/blueberrypy
#
# Copyright 2009 David Reynolds
#
# Use and distribution licensed under the BSD license. See
# the LICENSE file for full text.

import hmac
import base64
import binascii
import time
import datetime
from Cookie import BaseCookie

try:
    import cPickle as pickle
except ImportError:
    import pickle

try:
    from hashlib import sha1
except ImportError:
    import sha as sha1

import webob
from webob.exc import status_map

from blueberry import config

class Request(webob.Request):

    def signed_cookie(self, name, secret=None):
        if not secret:
            secret = config['app'].get('secret', 'secret')
        cookie = self.str_cookies.get(name)
        if not cookie:
            return

        try:
            sig, pickled = cookie[:40], base64.decodestring(cookie[40:])
        except binascii.Error:
            return
        if hmac.new(secret, pickled, sha1).hexdigest() == sig:
            return pickle.loads(pickled)

    def _protocol(self):
        p = self.environ.get('HTTP_X_FORWARDED_PROTO')
        if p:
            return p

        p = self.environ.get('HTTP_X_FORWARDED_SSL')
        if p:
            return p

        return self.scheme
    protocol = property(_protocol)

    def _subdomain(self):
        # very bad...
        domain_match = config['app'].get('domain', '')
        # strip port
        host = self.environ['HTTP_HOST'].split(':')[0]

        if host == domain_match:
            return ''

        match = re.compile('^(.+?)\.%s$' % domain_match)
        subdomain = re.sub(match, r'\1', host)
        return subdomain
    subdomain = property(_subdomain)

def _serialize_cookie_date(dt):
    if dt is None:
        return None
    if isinstance(dt, unicode):
        dt = dt.encode('ascii')
    if isinstance(dt, datetime.timedelta):
        dt = datetime.datetime.now() + dt
    if isinstance(dt, (datetime.datetime, datetime.date)):
        dt = dt.timetuple()
    return time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', dt)

class Response(webob.Response):

    def set_cookie(self, key, value='', max_age=None,
                   path='/', domain=None, secure=None, httponly=False,
                   version=None, comment=None, expires=None):
        if isinstance(value, unicode):
            value = value.encode(self.charset)
        value = value.replace('\n', '')

        cookie = BaseCookie()
        cookie[key] = value

        if isinstance(max_age, datetime.timedelta):
            max_age = max_age.seconds + max_age.days * 24 * 60 * 60
        if max_age is not None and expires is None:
            expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
        if isinstance(expires, datetime.timedelta):
            expires = datetime.datetime.utcnow() + expires
        if isinstance(expires, datetime.datetime):
            expires = _serialize_cookie_date(expires)

        for k, v in [('max_age', max_age),
                     ('path', path),
                     ('domain', domain),
                     ('secure', secure),
                     ('HttpOnly', httponly),
                     ('version', version),
                     ('comment', comment),
                     ('expires', expires)]:
            if v is not None and v is not False:
                cookie[key][k.replace('_', '-')] = str(v)
        self.headers.add('Set-Cookie', cookie[key].OutputString(None))

    def delete_cookie(self, key, path='/', domain=None):
        self.set_cookie(key, '', path=path, domain=domain,
                        max_age=0, expires=datetime.timedelta(days=-5))

    def unset_cookie(self, key):
        existing = self.headers.get_all('Set-Cookie')
        if not existing:
            raise KeyError('No cookies have been set')

        del self.headers['Set-Cookie']
        found = False

        for header in existing:
            cookies = BaseCookie()
            cookies.load(header)
            if key in cookies:
                found = True
                del cookies[key]
                header = cookies.output(header='').lstrip()
            if header:
                if header.endswith(';'):
                    header = header[:-1]
                self.headers.add_header('Set-Cookie', header)

        if not found:
            raise KeyError('No cookie has been set with the name %r' % key)

    def signed_cookie(self, name, data, secret=None, **kwargs):
        if not secret:
            secret = config['app'].get('secret', 'secret')
        pickled = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        sig = hmac.new(secret, pickled, sha1).hexdigest()
        self.set_cookie(name, sig + base64.encodestring(pickled), **kwargs)

def abort(status_code=None, detail="", headers=None, comment=None):
    exc = status_map[status_code](detail=detail, headers=headers, comment=comment)
    raise exc.exception

def redirect(url, code=302):
    exc = status_map[code]
    raise exc(location=url).exception
