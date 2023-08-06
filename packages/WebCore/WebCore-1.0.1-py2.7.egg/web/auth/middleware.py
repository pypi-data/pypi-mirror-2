# encoding: utf-8

import urllib

import web
import webob.exc

from paste.deploy.converters import asbool, aslist


__all__ = ['WebAuth', 'BasicAuthMiddleware']
log = __import__('logging').getLogger(__name__)

default_config = web.utils.dictionary.adict(
        name = 'uid',
        intercept = '401',
        handler = '/login',
        internal = False,
        lookup = None,
        authenticate = None
    )



class WebAuth(object):
    def __init__(self, application, config=dict(), prefix='auth.'):
        self.application = application
        
        prefix_length = len(prefix)
        our_config = web.utils.dictionary.adict(default_config.copy())
        
        for i, j in config.iteritems():
            if i.startswith(prefix):
                our_config[i[prefix_length:]] = j
        
        our_config.intercept = [i.strip() for i in aslist(our_config.intercept)]
        our_config.internal = asbool(our_config.internal)
        
        if our_config.lookup is None:
            raise Exception('You must define an authentication lookup method.')
        
        our_config.lookup = self.get_method(our_config.lookup)
        our_config.authenticate = self.get_method(our_config.authenticate)
        
        web.auth.config = our_config
    
    def get_method(self, string):
        """Returns a lazily-evaluated callable."""
        
        if not string: return None
        
        if hasattr(string, '__call__'):
            return string
        
        package, reference = string.split(':', 1)
        prop = None
        
        if '.' in reference:
            reference, prop = reference.rsplit('.', 1)
        
        obj = web.utils.object.get_dotted_object('%s:%s' % (package, reference))
        
        if not prop:
            def lazy(*args, **kw):
                return obj(*args, **kw)
            
            return lazy
        
        def lazy(*args, **kw):
            return getattr(obj, prop)(*args, **kw)
        
        return lazy
    
    def authenticate(self, environ, start_response):
        raise webob.exc.HTTPTemporaryRedirect(location=web.auth.config.handler + '?redirect=' + urllib.quote_plus(environ['SCRIPT_NAME']) + urllib.quote_plus(environ['PATH_INFO']))
    
    def __call__(self, environ, start_response):
        session = environ['beaker.session']
        config = web.auth.config
        
        # We set this to None on the first request to ensure the session ID stabalizes.
        if config.name not in session:
            session[config.name] = None
            session.save()
        
        if environ.has_key('paste.registry'):
            environ['paste.registry'].register(
                    web.auth.user,
                    config.lookup(session[config.name]) if session[config.name] else None
                )
        
        def our_start_response(status, headers):
            if status.split(' ', 1)[0] in config.intercept:
                return self.authenticate(environ, start_response)
            
            return start_response(status, headers)
        
        try:
            result = self.application(environ, our_start_response)
        
        except webob.exc.HTTPException, e:
            return e(environ, start_response)
        
        return result


class BasicAuthMiddleware(object):
    def __init__(self, application):
        self.application = application
 
    def __call__(self, environ, start_response):
        if 'HTTP_AUTHORIZATION' in environ:
            authtype, auth = environ['HTTP_AUTHORIZATION'].split()
            
            if authtype.lower() == 'basic':
                try:
                    un, pw = b64decode(auth).split(':')
                
                except TypeError:
                    return HTTPUnauthorized()
                
                if not web.auth.authenticate(un, pw):
                    return HTTPUnauthorized()
 
        try:
            return self.application(environ, start_response)
        
        except HTTPException, e:
            return e(environ, start_response)
