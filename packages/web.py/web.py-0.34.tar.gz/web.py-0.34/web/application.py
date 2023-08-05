#!/usr/bin/python
"""
Web application
(from web.py)
"""
import webapi as web
import webapi, wsgi, utils
import debugerror
from utils import lstrips, safeunicode
import sys

import urllib
import traceback
import itertools
import os
import re
import types
from exceptions import SystemExit

try:
    import wsgiref.handlers
except ImportError:
    pass # don't break people with old Pythons

__all__ = [
    "application", "auto_application",
    "subdir_application", "subdomain_application", 
    "loadhook", "unloadhook",
    "autodelegate"
]

class application:
    """
    Application to delegate requests based on path.
    
        >>> urls = ("/hello", "hello")
        >>> app = application(urls, globals())
        >>> class hello:
        ...     def GET(self): return "hello"
        >>>
        >>> app.request("/hello").data
        'hello'
    """
    def __init__(self, mapping=(), fvars={}, autoreload=None):
        if autoreload is None:
            autoreload = web.config.get('debug', False)
        self.mapping = mapping
        self.fvars = fvars
        self.processors = []
        
        self.add_processor(loadhook(self._load))
        self.add_processor(unloadhook(self._unload))
        
        if autoreload:
            def main_module_name():
                mod = sys.modules['__main__']
                file = getattr(mod, '__file__', None) # make sure this works even from python interpreter
                return file and os.path.splitext(os.path.basename(file))[0]

            def modname(fvars):
                """find name of the module name from fvars."""
                file, name = fvars.get('__file__'), fvars.get('__name__')
                if file is None or name is None:
                    return None

                if name == '__main__':
                    # Since the __main__ module can't be reloaded, the module has 
                    # to be imported using its file name.                    
                    name = main_module_name()
                return name
                
            mapping_name = utils.dictfind(fvars, mapping)
            module_name = modname(fvars)
            
            def reload_mapping():
                """loadhook to reload mapping and fvars."""
                mod = __import__(module_name)
                mapping = getattr(mod, mapping_name, None)
                if mapping:
                    self.fvars = mod.__dict__
                    self.mapping = mapping

            self.add_processor(loadhook(Reloader()))
            if mapping_name and module_name:
                self.add_processor(loadhook(reload_mapping))

            # load __main__ module usings its filename, so that it can be reloaded.
            if main_module_name() and '__main__' in sys.argv:
                try:
                    __import__(main_module_name())
                except ImportError:
                    pass
                    
    def _load(self):
        web.ctx.app_stack.append(self)
        
    def _unload(self):
        web.ctx.app_stack = web.ctx.app_stack[:-1]
        
        if web.ctx.app_stack:
            # this is a sub-application, revert ctx to earlier state.
            oldctx = web.ctx.get('_oldctx')
            if oldctx:
                web.ctx.home = oldctx.home
                web.ctx.homepath = oldctx.homepath
                web.ctx.path = oldctx.path
                web.ctx.fullpath = oldctx.fullpath
                
    def _cleanup(self):
        #@@@
        # Since the CherryPy Webserver uses thread pool, the thread-local state is never cleared.
        # This interferes with the other requests. 
        # clearing the thread-local storage to avoid that.
        # see utils.ThreadedDict for details
        import threading
        t = threading.currentThread()
        if hasattr(t, '_d'):
            del t._d
    
    def add_mapping(self, pattern, classname):
        self.mapping += (pattern, classname)
        
    def add_processor(self, processor):
        """
        Adds a processor to the application. 
        
            >>> urls = ("/(.*)", "echo")
            >>> app = application(urls, globals())
            >>> class echo:
            ...     def GET(self, name): return name
            ...
            >>>
            >>> def hello(handler): return "hello, " +  handler()
            ...
            >>> app.add_processor(hello)
            >>> app.request("/web.py").data
            'hello, web.py'
        """
        self.processors.append(processor)

    def request(self, localpart='/', method='GET', data=None,
                host="0.0.0.0:8080", headers=None, https=False, **kw):
        """Makes request to this application for the specified path and method.
        Response will be a storage object with data, status and headers.

            >>> urls = ("/hello", "hello")
            >>> app = application(urls, globals())
            >>> class hello:
            ...     def GET(self): 
            ...         web.header('Content-Type', 'text/plain')
            ...         return "hello"
            ...
            >>> response = app.request("/hello")
            >>> response.data
            'hello'
            >>> response.status
            '200 OK'
            >>> response.headers['Content-Type']
            'text/plain'

        To use https, use https=True.

            >>> urls = ("/redirect", "redirect")
            >>> app = application(urls, globals())
            >>> class redirect:
            ...     def GET(self): raise web.seeother("/foo")
            ...
            >>> response = app.request("/redirect")
            >>> response.headers['Location']
            'http://0.0.0.0:8080/foo'
            >>> response = app.request("/redirect", https=True)
            >>> response.headers['Location']
            'https://0.0.0.0:8080/foo'

        The headers argument specifies HTTP headers as a mapping object
        such as a dict.

            >>> urls = ('/ua', 'uaprinter')
            >>> class uaprinter:
            ...     def GET(self):
            ...         return 'your user-agent is ' + web.ctx.env['HTTP_USER_AGENT']
            ... 
            >>> app = application(urls, globals())
            >>> app.request('/ua', headers = {
            ...      'User-Agent': 'a small jumping bean/1.0 (compatible)'
            ... }).data
            'your user-agent is a small jumping bean/1.0 (compatible)'

        """
        path, maybe_query = urllib.splitquery(localpart)
        query = maybe_query or ""
        
        if 'env' in kw:
            env = kw['env']
        else:
            env = {}
        env = dict(env, HTTP_HOST=host, REQUEST_METHOD=method, PATH_INFO=path, QUERY_STRING=query, HTTPS=str(https))
        headers = headers or {}

        for k, v in headers.items():
            env['HTTP_' + k.upper().replace('-', '_')] = v

        if 'HTTP_CONTENT_LENGTH' in env:
            env['CONTENT_LENGTH'] = env.pop('HTTP_CONTENT_LENGTH')

        if 'HTTP_CONTENT_TYPE' in env:
            env['CONTENT_TYPE'] = env.pop('HTTP_CONTENT_TYPE')

        if method in ["POST", "PUT"]:
            data = data or ''
            import StringIO
            if isinstance(data, dict):
                q = urllib.urlencode(data)
            else:
                q = data
            env['wsgi.input'] = StringIO.StringIO(q)
            if not env.get('CONTENT_TYPE', '').lower().startswith('multipart/') and 'CONTENT_LENGTH' not in env:
                env['CONTENT_LENGTH'] = len(q)
        response = web.storage()
        def start_response(status, headers):
            response.status = status
            response.headers = dict(headers)
            response.header_items = headers
        response.data = "".join(self.wsgifunc()(env, start_response))
        return response

    def browser(self):
        import browser
        return browser.AppBrowser(self)

    def handle(self):
        fn, args = self._match(self.mapping, web.ctx.path)
        return self._delegate(fn, self.fvars, args)
        
    def handle_with_processors(self):
        def process(processors):
            try:
                if processors:
                    p, processors = processors[0], processors[1:]
                    return p(lambda: process(processors))
                else:
                    return self.handle()
            except web.HTTPError:
                raise
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print >> web.debug, traceback.format_exc()
                raise self.internalerror()
        
        # processors must be applied in the resvere order. (??)
        return process(self.processors)
                        
    def wsgifunc(self, *middleware):
        """Returns a WSGI-compatible function for this application."""
        def peep(iterator):
            """Peeps into an iterator by doing an iteration
            and returns an equivalent iterator.
            """
            # wsgi requires the headers first
            # so we need to do an iteration
            # and save the result for later
            try:
                firstchunk = iterator.next()
            except StopIteration:
                firstchunk = ''

            return itertools.chain([firstchunk], iterator)    
                                
        def is_generator(x): return x and hasattr(x, 'next')
        
        def wsgi(env, start_resp):
            # clear threadlocal to avoid inteference of previous requests
            self._cleanup()

            self.load(env)
            try:
                # allow uppercase methods only
                if web.ctx.method.upper() != web.ctx.method:
                    raise web.nomethod()

                result = self.handle_with_processors()
                if is_generator(result):
                    result = peep(result)
                else:
                    result = [result]
            except web.HTTPError, e:
                result = [e.data]

            result = web.utf8(iter(result))

            status, headers = web.ctx.status, web.ctx.headers
            start_resp(status, headers)
            
            def cleanup():
                self._cleanup()
                yield '' # force this function to be a generator
                            
            return itertools.chain(result, cleanup())

        for m in middleware: 
            wsgi = m(wsgi)

        return wsgi

    def run(self, *middleware):
        """
        Starts handling requests. If called in a CGI or FastCGI context, it will follow
        that protocol. If called from the command line, it will start an HTTP
        server on the port named in the first command line argument, or, if there
        is no argument, on port 8080.
        
        `middleware` is a list of WSGI middleware which is applied to the resulting WSGI
        function.
        """
        return wsgi.runwsgi(self.wsgifunc(*middleware))
    
    def cgirun(self, *middleware):
        """
        Return a CGI handler. This is mostly useful with Google App Engine.
        There you can just do:
        
            main = app.cgirun()
        """
        wsgiapp = self.wsgifunc(*middleware)

        try:
            from google.appengine.ext.webapp.util import run_wsgi_app
            return run_wsgi_app(wsgiapp)
        except ImportError:
            # we're not running from within Google App Engine
            return wsgiref.handlers.CGIHandler().run(wsgiapp)
    
    def load(self, env):
        """Initializes ctx using env."""
        ctx = web.ctx
        ctx.clear()
        ctx.status = '200 OK'
        ctx.headers = []
        ctx.output = ''
        ctx.environ = ctx.env = env
        ctx.host = env.get('HTTP_HOST')

        if env.get('wsgi.url_scheme') in ['http', 'https']:
            ctx.protocol = env['wsgi.url_scheme']
        elif env.get('HTTPS', '').lower() in ['on', 'true', '1']:
            ctx.protocol = 'https'
        else:
            ctx.protocol = 'http'
        ctx.homedomain = ctx.protocol + '://' + env.get('HTTP_HOST', '[unknown]')
        ctx.homepath = os.environ.get('REAL_SCRIPT_NAME', env.get('SCRIPT_NAME', ''))
        ctx.home = ctx.homedomain + ctx.homepath
        #@@ home is changed when the request is handled to a sub-application.
        #@@ but the real home is required for doing absolute redirects.
        ctx.realhome = ctx.home
        ctx.ip = env.get('REMOTE_ADDR')
        ctx.method = env.get('REQUEST_METHOD')
        ctx.path = env.get('PATH_INFO')
        # http://trac.lighttpd.net/trac/ticket/406 requires:
        if env.get('SERVER_SOFTWARE', '').startswith('lighttpd/'):
            ctx.path = lstrips(env.get('REQUEST_URI').split('?')[0], ctx.homepath)
            # Apache and CherryPy webservers unquote the url but lighttpd doesn't. 
            # unquote explicitly for lighttpd to make ctx.path uniform across all servers.
            ctx.path = urllib.unquote(ctx.path)

        if env.get('QUERY_STRING'):
            ctx.query = '?' + env.get('QUERY_STRING', '')
        else:
            ctx.query = ''

        ctx.fullpath = ctx.path + ctx.query
        
        for k, v in ctx.iteritems():
            if isinstance(v, str):
                ctx[k] = safeunicode(v)

        # status must always be str
        ctx.status = '200 OK'
        
        ctx.app_stack = []

    def _delegate(self, f, fvars, args=[]):
        def handle_class(cls):
            meth = web.ctx.method
            if meth == 'HEAD' and not hasattr(cls, meth):
                meth = 'GET'
            if not hasattr(cls, meth):
                raise web.nomethod(cls)
            tocall = getattr(cls(), meth)
            return tocall(*args)
            
        def is_class(o): return isinstance(o, (types.ClassType, type))
            
        if f is None:
            raise web.notfound()
        elif isinstance(f, application):
            return f.handle_with_processors()
        elif is_class(f):
            return handle_class(f)
        elif isinstance(f, basestring):
            if f.startswith('redirect '):
                url = f.split(' ', 1)[1]
                if web.ctx.method == "GET":
                    x = web.ctx.env.get('QUERY_STRING', '')
                    if x:
                        url += '?' + x
                raise web.redirect(url)
            elif '.' in f:
                x = f.split('.')
                mod, cls = '.'.join(x[:-1]), x[-1]
                mod = __import__(mod, globals(), locals(), [""])
                cls = getattr(mod, cls)
            else:
                cls = fvars[f]
            return handle_class(cls)
        elif hasattr(f, '__call__'):
            return f()
        else:
            return web.notfound()

    def _match(self, mapping, value):
        for pat, what in utils.group(mapping, 2):
            if isinstance(what, application):
                if value.startswith(pat):
                    f = lambda: self._delegate_sub_application(pat, what)
                    return f, None
                else:
                    continue
            elif isinstance(what, basestring):
                what, result = utils.re_subm('^' + pat + '$', what, value)
            else:
                result = utils.re_compile('^' + pat + '$').match(value)
                
            if result: # it's a match
                return what, [x for x in result.groups()]
        return None, None
        
    def _delegate_sub_application(self, dir, app):
        """Deletes request to sub application `app` rooted at the directory `dir`.
        The home, homepath, path and fullpath values in web.ctx are updated to mimic request
        to the subapp and are restored after it is handled. 
        
        @@Any issues with when used with yield?
        """
        web.ctx._oldctx = web.storage(web.ctx)
        web.ctx.home += dir
        web.ctx.homepath += dir
        web.ctx.path = web.ctx.path[len(dir):]
        web.ctx.fullpath = web.ctx.fullpath[len(dir):]
        return app.handle_with_processors()
            
    def get_parent_app(self):
        if self in web.ctx.app_stack:
            index = web.ctx.app_stack.index(self)
            if index > 0:
                return web.ctx.app_stack[index-1]
        
    def notfound(self):
        """Returns HTTPError with '404 not found' message"""
        parent = self.get_parent_app()
        if parent:
            return parent.notfound()
        else:
            return web._NotFound()
            
    def internalerror(self):
        """Returns HTTPError with '500 internal error' message"""
        parent = self.get_parent_app()
        if parent:
            return parent.internalerror()
        elif web.config.get('debug'):
            import debugerror
            return debugerror.debugerror()
        else:
            return web._InternalError()

class auto_application(application):
    """Application similar to `application` but urls are constructed 
    automatiacally using metaclass.

        >>> app = auto_application()
        >>> class hello(app.page):
        ...     def GET(self): return "hello, world"
        ...
        >>> class foo(app.page):
        ...     path = '/foo/.*'
        ...     def GET(self): return "foo"
        >>> app.request("/hello").data
        'hello, world'
        >>> app.request('/foo/bar').data
        'foo'
    """
    def __init__(self):
        application.__init__(self)

        class metapage(type):
            def __init__(klass, name, bases, attrs):
                type.__init__(klass, name, bases, attrs)
                path = attrs.get('path', '/' + name)

                # path can be specified as None to ignore that class
                # typically required to create a abstract base class.
                if path is not None:
                    self.add_mapping(path, klass)

        class page:
            path = None
            __metaclass__ = metapage

        self.page = page

# The application class already has the required functionality of subdir_application
subdir_application = application
                
class subdomain_application(application):
    """
    Application to delegate requests based on the host.

        >>> urls = ("/hello", "hello")
        >>> app = application(urls, globals())
        >>> class hello:
        ...     def GET(self): return "hello"
        >>>
        >>> mapping = (r"hello\.example\.com", app)
        >>> app2 = subdomain_application(mapping)
        >>> app2.request("/hello", host="hello.example.com").data
        'hello'
        >>> response = app2.request("/hello", host="something.example.com")
        >>> response.status
        '404 Not Found'
        >>> response.data
        'not found'
    """
    def handle(self):
        host = web.ctx.host.split(':')[0] #strip port
        fn, args = self._match(self.mapping, host)
        return self._delegate(fn, self.fvars, args)
        
    def _match(self, mapping, value):
        for pat, what in utils.group(mapping, 2):
            if isinstance(what, basestring):
                what, result = utils.re_subm('^' + pat + '$', what, value)
            else:
                result = utils.re_compile('^' + pat + '$').match(value)

            if result: # it's a match
                return what, [x for x in result.groups()]
        return None, None
        
def loadhook(h):
    """
    Converts a load hook into an application processor.
    
        >>> app = auto_application()
        >>> def f(): "something done before handling request"
        ...
        >>> app.add_processor(loadhook(f))
    """
    def processor(handler):
        h()
        return handler()
        
    return processor
    
def unloadhook(h):
    """
    Converts an unload hook into an application processor.
    
        >>> app = auto_application()
        >>> def f(): "something done after handling request"
        ...
        >>> app.add_processor(unloadhook(f))    
    """
    def processor(handler):
        try:
            result = handler()
            is_generator = result and hasattr(result, 'next')
        except:
            # run the hook even when handler raises some exception
            h()
            raise

        if is_generator:
            return wrap(result)
        else:
            h()
            return result
            
    def wrap(result):
        def next():
            try:
                return result.next()
            except:
                # call the hook at the and of iterator
                h()
                raise

        result = iter(result)
        while True:
            yield next()
            
    return processor

def autodelegate(prefix=''):
    """
    Returns a method that takes one argument and calls the method named prefix+arg,
    calling `notfound()` if there isn't one. Example:

        urls = ('/prefs/(.*)', 'prefs')

        class prefs:
            GET = autodelegate('GET_')
            def GET_password(self): pass
            def GET_privacy(self): pass

    `GET_password` would get called for `/prefs/password` while `GET_privacy` for 
    `GET_privacy` gets called for `/prefs/privacy`.
    
    If a user visits `/prefs/password/change` then `GET_password(self, '/change')`
    is called.
    """
    def internal(self, arg):
        if '/' in arg:
            first, rest = arg.split('/', 1)
            func = prefix + first
            args = ['/' + rest]
        else:
            func = prefix + arg
            args = []
        
        if hasattr(self, func):
            try:
                return getattr(self, func)(*args)
            except TypeError:
                raise web.notfound()
        else:
            raise web.notfound()
    return internal

class Reloader:
    """Checks to see if any loaded modules have changed on disk and, 
    if so, reloads them.
    """
    def __init__(self):
        self.mtimes = {}

    def __call__(self):
        for mod in sys.modules.values():
            self.check(mod)
            
    def check(self, mod):
        try: 
            mtime = os.stat(mod.__file__).st_mtime
        except (AttributeError, OSError, IOError):
            return
        if mod.__file__.endswith('.pyc') and os.path.exists(mod.__file__[:-1]):
            mtime = max(os.stat(mod.__file__[:-1]).st_mtime, mtime)
            
        if mod not in self.mtimes:
            self.mtimes[mod] = mtime
        elif self.mtimes[mod] < mtime:
            try: 
                reload(mod)
                self.mtimes[mod] = mtime
            except ImportError: 
                pass
                
if __name__ == "__main__":
    import doctest
    doctest.testmod()
