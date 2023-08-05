# -*- coding: utf-8 -*-
"""
    webapp2
    =======

    Taking Google App Engine's webapp to the next level!

    :copyright: 2010 by tipfy.org.
    :license: Apache Sotware License, see LICENSE for details.
"""
import logging
import re
import urllib
import urlparse

from google.appengine.ext.webapp import Request
from google.appengine.ext.webapp.util import run_bare_wsgi_app, run_wsgi_app

import webob
import webob.exc

#: Base HTTP exception, set here as public interface.
HTTPException = webob.exc.HTTPException

#: Allowed request methods.
_ALLOWED_METHODS = frozenset(['GET', 'POST', 'HEAD', 'OPTIONS', 'PUT',
    'DELETE', 'TRACE'])

#: Regex for URL definitions.
_ROUTE_REGEX = re.compile(r'''
    \<            # The exact character "<"
    (\w*)         # The optional variable name (restricted to a-z, 0-9, _)
    (?::([^>]*))? # The optional :regex part
    \>            # The exact character ">"
    ''', re.VERBOSE)

#: Value used for required arguments.
REQUIRED_VALUE = object()


class Response(webob.Response):
    """Abstraction for an HTTP response.

    Implements all of ``webapp.Response`` interface, except ``wsgi_write()``
    as the response itself is returned by the WSGI application.
    """
    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)

        # webapp uses self.response.out.write(...)
        self.out = self.body_file

    def set_status(self, code, message=None):
        """Sets the HTTP status code of this response.

        :param message:
            The HTTP status string to use
        :param message:
            A status string. If none is given, uses the default from the
            HTTP/1.1 specification.
        """
        if message:
            self.status = '%d %s' % (code, message)
        else:
            self.status = code

    def clear(self):
        """Clears all data written to the output stream so that it is empty."""
        self.app_iter = []

    @staticmethod
    def http_status_message(code):
        """Returns the default HTTP status message for the given code.

        :param code:
            The HTTP code for which we want a message.
        """
        message = webob.statusreasons.status_reasons.get(code, None)
        if not message:
            raise KeyError('Invalid HTTP status code: %d' % code)

        return message


class RequestHandler(object):
    """Base HTTP request handler. Clients should subclass this class.

    Subclasses should override get(), post(), head(), options(), etc to handle
    different HTTP methods.

    Implements most of ``webapp.RequestHandler`` interface.
    """
    def __init__(self, app, request, response):
        """Initializes the handler.

        :param app:
            A :class:`WSGIApplication` instance.
        :param request:
            A ``webapp.Request`` instance.
        :param response:
            A :class:`Response` instance.
        """
        self.app = app
        self.request = request
        self.response = response

    def __call__(self, _method, *args, **kwargs):
        """Dispatches the requested method.

        :param _method:
            The method to be dispatched: the request method in lower case
            (e.g., 'get', 'post', 'head', 'put' etc).
        :param args:
            Positional arguments to be passed to the method, coming from the
            matched :class:`Route`.
        :param kwargs:
            Keyword arguments to be passed to the method, coming from the
            matched :class:`Route`.
        :returns:
            None.
        """
        method = getattr(self, _method, None)
        if method is None:
            # 405 Method Not Allowed.
            # The response MUST include an Allow header containing a
            # list of valid methods for the requested resource.
            # http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.6
            valid = ', '.join(get_valid_methods(self))
            self.abort(405, headers=[('Allow', valid)])

        # Execute the method.
        method(*args, **kwargs)

    def error(self, code):
        """Clears the response output stream and sets the given HTTP error
        code. This doesn't stop code execution; the response is still
        available to be filled.

        :param code:
            HTTP status error code (e.g., 501).
        """
        self.response.set_status(code)
        self.response.clear()

    def abort(self, code, *args, **kwargs):
        """Raises an :class:`HTTPException`. This stops code execution,
        leaving the HTTP exception to be handled by an exception handler.

        :param code:
            HTTP status error code (e.g., 404).
        :param args:
            Positional arguments to be passed to the exception class.
        :param kwargs:
            Keyword arguments to be passed to the exception class.
        """
        abort(code, *args, **kwargs)

    def redirect(self, uri, permanent=False):
        """Issues an HTTP redirect to the given relative URL.

        :param uri:
            A relative or absolute URI (e.g., '../flowers.html').
        :param permanent:
            If True, uses a 301 redirect instead of a 302 redirect.
        """
        if permanent:
            self.response.set_status(301)
        else:
            self.response.set_status(302)

        absolute_url = urlparse.urljoin(self.request.uri, uri)
        self.response.headers['Location'] = str(absolute_url)
        self.response.clear()

    def redirect_to(self, _name, _secure=False, _anchor=None, _permanent=False,
        **kwargs):
        """Convenience method mixing :meth:`redirect` and :meth:`url_for`:
        Issues an HTTP redirect to a named URL built using :meth:`url_for`.

        :param _name:
            The route name to redirect to.
        :param _secure:
            If True, redirects to a URL using `https` scheme.
        :param _anchor:
            An anchor to append to the end of the redirected URL.
        :param _permanent:
            If True, uses a 301 redirect instead of a 302 redirect.
        :param kwargs:
            Keyword arguments to build the URL.
        """
        uri = self.url_for(_name, _secure=_secure, _anchor=_anchor, **kwargs)
        self.redirect(uri, permanent=_permanent)

    def url_for(self, _name, _full=False, _secure=False, _anchor=None,
        **kwargs):
        """Builds and returns a URL for a named :class:`Route`.

        .. seealso:: :meth:`Router.build`.
        """
        return self.app.router.build(_name, _full=_full, _secure=_secure,
            _anchor=_anchor, _request=self.request, **kwargs)

    def get_config(self, module, key=None, default=REQUIRED_VALUE):
        """Returns a configuration value for a module.

        .. seealso:: :meth:`Config.load_and_get`.
        """
        return self.app.config.load_and_get(module, key=key, default=default)

    def handle_exception(self, exception, debug_mode):
        """Called if this handler throws an exception during execution.

        The default behavior is to raise the exception to be handled by
        :meth:`WSGIApplication.handle_exception`.

        :param exception:
            The exception that was thrown.
        :param debug_mode:
            True if the web application is running in debug mode.
        """
        raise


class RedirectHandler(RequestHandler):
    """Redirects to the given URL for all GET requests. This is meant to be
    used when defining URL routes. You must provide at least the keyword
    argument *url* in the route default values. Example::

        def get_redirect_url(handler, *args, **kwargs):
            return handler.url_for('new-route-name')

        app = WSGIApplication([
            (Route(r'/old-url', defaults={'url': '/new-url'}), RedirectHandler),
            (Route(r'/other-old-url', defaults={'url': get_redirect_url}), RedirectHandler),
        ])

    Based on idea from `Tornado`_.
    """
    def get(self, *args, **kwargs):
        """Performs the redirect. Two keyword arguments can be passed through
        the URL route:

        - *url*: A URL string or a callable that returns a URL. The callable
          is called passing ``(handler, *args, **kwargs)`` as arguments.
        - *permanent*: If False, uses a 301 redirect instead of a 302 redirect
          Default is True.
        """
        url = kwargs.get('url', '/')

        if callable(url):
            url = url(self, *args, **kwargs)

        self.redirect(url, permanent=kwargs.get('permanent', True))


class SimpleRoute(object):
    """A route that is compatible with webapp's routing. URL building is not
    implemented as webapp has rudimentar support for it, and this is the most
    unknown webapp feature anyway.
    """
    #: Route name, used to build URLs. Always None for this route class.
    name = None
    #: This route can't be built, so it is always used for matching.
    build_only = False

    def __init__(self, template):
        """Initializes a URL route.

        :param template:
            A route regex to be matched.
        """
        self.template = template
        self._regex = None

    @property
    def regex(self):
        if self._regex is None:
            if not self.template.startswith('^'):
                self.template = '^' + self.template

            if not self.template.endswith('$'):
                self.template += '$'

            self._regex = re.compile(self.template)

        return self._regex

    def match(self, request):
        """Matches this route against the current request.

        :param request:
            A ``webapp.Request`` instance.
        :returns:
            A tuple ``(route, args, kwargs)`` if the route matches, or None.
        """
        match = self.regex.match(request.path)
        if match:
            return self, match.groups(), {}

    def build(self, *args, **kwargs):
        raise NotImplementedError()

    def __repr__(self):
        return 'SimpleRoute(%r)' % self.template

    __str__ = __repr__


class Route(object):
    """A URL route definition. A route template contains regular expressions
    enclosed by ``<>`` and is used to match requested URLs. Here are some
    examples::

        route = Route(r'/article/<id:[\d]+>')
        route = Route(r'/wiki/<page_name:\w+>')
        route = Route(r'/blog/<year:\d{4}>/<month:\d{2}>/<day:\d{2}>/<slug:\w+>')

    Based on `Another Do-It-Yourself Framework`_, by Ian Bicking. We added
    URL building, non-keyword variables and other improvements.
    """
    def __init__(self, template, name=None, defaults=None, build_only=False):
        """Initializes a URL route.

        :param template:
            A route template to be matched. A route template contains parts
            enclosed by ``<>`` that can have only a name, only a regular
            expression or both:

              =============================  ==================================
              Format                         Example
              =============================  ==================================
              ``<name>``                     ``r'/<year>/<month>'``
              ``<:regular expression>``      ``r'/<:\d{4}>/<:\d{2}>'``
              ``<name:regular expression>``  ``r'/<year:\d{4}>/<month:\d{2}>'``
              =============================  ==================================

            If the name is set, the value of the matched regular expression
            is passed as keyword argument to the :class:`RequestHandler`.
            Otherwise it is passed as positional argument.

            The same template can mix parts with name, regular expression or
            both.
        :param name:
            The name of this route, used to build URLs based on it.
        :param defaults:
            Default or extra keywords to be returned by this route. Values
            also present in the route variables are used to build the URL
            when they are missing.
        :param build_only:
            If True, this route never matches and is used only to build URLs.
        """
        self.template = template
        self.name = name
        self.defaults = defaults or {}
        self.build_only = build_only
        # Lazy properties.
        self._regex = None
        self._variables = None
        self._reverse_template = None

    def _parse_template(self):
        self._variables = {}
        last = count = 0
        regex = template = ''
        for match in _ROUTE_REGEX.finditer(self.template):
            part = self.template[last:match.start()]
            name = match.group(1)
            expr = match.group(2) or '[^/]+'
            last = match.end()

            if not name:
                name = '__%d__' % count
                count += 1

            template += '%s%%(%s)s' % (part, name)
            regex += '%s(?P<%s>%s)' % (re.escape(part), name, expr)
            self._variables[name] = re.compile('^%s$' % expr)

        regex = '^%s%s$' % (regex, re.escape(self.template[last:]))
        self._regex = re.compile(regex)
        self._reverse_template = template + self.template[last:]
        self.has_positional_variables = count > 0

    @property
    def regex(self):
        if self._regex is None:
            self._parse_template()

        return self._regex

    @property
    def variables(self):
        if self._variables is None:
            self._parse_template()

        return self._variables

    @property
    def reverse_template(self):
        if self._reverse_template is None:
            self._parse_template()

        return self._reverse_template

    def match(self, request):
        """Matches this route against the current request.

        :param request:
            A ``webapp.Request`` instance.
        :returns:
            A tuple ``(route, args, kwargs)`` if the route matches, or None.
        """
        match = self.regex.match(request.path)
        if match:
            kwargs = self.defaults.copy()
            kwargs.update(match.groupdict())
            if self.has_positional_variables:
                args = tuple(value[1] for value in sorted((int(key[2:-2]), \
                    kwargs.pop(key)) for key in \
                    kwargs.keys() if key.startswith('__')))
            else:
                args = ()

            return self, args, kwargs

    def build(self, *args, **kwargs):
        """Builds a URL for this route. Examples:

        >>> route = Route(r'/blog')
        >>> route.build()
        /blog
        >>> route.build(page='2', format='atom')
        /blog?page=2&format=atom
        >>> route = Route(r'/blog/archive/<year:\d{4}>')
        >>> route.build(year=2010)
        /blog/2010
        >>> route = Route(r'/blog/archive/<year:\d{4}>/<month:\d{2}>/<slug:\w+>')
        >>> route.build(year='2010', month='07', slug='my_blog_post')
        /blog/2010/07/my_blog_post
        >>> route = Route(r'/blog/archive/<:\d{4}>/<:\d{2}>/<slug:\w+>')
        >>> route.build('2010', '07', slug='my_blog_post')
        /blog/2010/07/my_blog_post

        :param args:
            Positional arguments to build the URL. All positional variables
            defined in the route must be passed and must conform to the
            format set in the route. Extra arguments are ignored.
        :param kwargs:
            Keyword arguments to build the URL. All variables not set in the
            route default values must be passed and must conform to the format
            set in the route. Extra keywords are appended as URL arguments.
        :returns:
            A formatted URL.
        """
        variables = self.variables
        if self.has_positional_variables:
            for index, value in enumerate(args):
                key = '__%d__' % index
                if key in variables:
                    kwargs[key] = value

        values = {}
        for name, regex in variables.iteritems():
            value = kwargs.pop(name, self.defaults.get(name))
            if not value:
                if name.startswith('__'):
                    name = name[2:-2]

                raise KeyError('Missing argument "%s" to build URL.' % name)

            if not isinstance(value, basestring):
                value = str(value)

            value = url_escape(value)

            if not regex.match(value):
                if name.startswith('__'):
                    name = name[2:-2]

                raise ValueError('URL buiding error: Value "%s" is not '
                    'supported for argument "%s".' % (value, name))

            values[name] = value

        url = self.reverse_template % values

        # Cleanup and encode extra kwargs.
        kwargs = [(to_utf8(k), to_utf8(v)) for k, v in kwargs.iteritems() \
            if isinstance(v, basestring)]

        if kwargs:
            # Append extra keywords as URL arguments.
            url += '?%s' % urllib.urlencode(kwargs)

        return url

    def __repr__(self):
        return 'Route(%r, name=%r, defaults=%s, build_only=%s)' % \
            (self.template, self.name, self.defaults, self.build_only)

    __str__ = __repr__


class Router(object):
    """A simple URL router used to match the current URL, dispatch the handler
    and build URLs for other resources.
    """
    #: Default class used when the route is a string, compatible with webapp.
    route_class = SimpleRoute

    def __init__(self, routes=None):
        """Initializes the router.

        :param routes:
            A list of tuples ``(route, handler)`` to initialize the router.
        """
        self.routes = []
        self.route_map = {}
        if routes:
            for route, handler in routes:
                self.add(route, handler)

    def add(self, route, handler):
        """Adds a route to this router.

        :param route:
            A :class:`Route` instance, or a string used to instantiate
            :attr:`route_class`.
        :param handler:
            A :class:`RequestHandler` class or dotted name for a class to be
            lazily imported, e.g., ``my.module.MyHandler``.
        """
        if isinstance(route, basestring):
            # Simple route, compatible with webapp.
            route = self.route_class(route)

        if isinstance(handler, basestring):
            # Auto import the handler when needed.
            handler = LazyObject(handler)

        if not route.build_only:
            self.routes.append((route, handler))
        elif not route.name:
            raise ValueError("Route %s is build_only but doesn't have name." %
                route.__repr__())

        if route.name:
            self.route_map[route.name] = route

    def match(self, request):
        """Matches all routes against the current request. The first one that
        matches is returned.

        :param request:
            A ``webapp.Request`` instance.
        :returns:
            A tuple ``(handler, route, args, kwargs)``.
        """
        for route, handler in self.routes:
            match = route.match(request)
            if match:
                return (handler,) + match

        return None

    def dispatch(self, app, request, response):
        """Dispatches a request. This matches the current request against
        registered routes and calls the matched :class:`RequestHandler`.

        :param app:
            A :class:`WSGIApplication` instance.
        :param request:
            A ``webapp.Request`` instance.
        :param response:
            A :class:`Response` instance.
        """
        request.router_match = match = self.match(request)

        if match:
            handler_class, route, args, kwargs = match
            handler = handler_class(app, request, response)
            try:
                handler(request.method.lower(), *args, **kwargs)
            except Exception, e:
                # If the handler implements exception handling,
                # let it handle it.
                handler.handle_exception(e, app.debug)
        else:
            # 404 Not Found.
            raise webob.exc.HTTPNotFound()

    def build(self, _name, _full=False, _secure=False, _anchor=None,
        _request=None, **kwargs):
        """Builds and returns a URL for a named :class:`Route`.

        For example, if you have these routes registered in the application::

            app = WSGIApplication([
                (Route(r'/', 'home/main'), 'handlers.HomeHandler'),
                (Route(r'/wiki', 'wiki/start'), WikiHandler),
                (Route(r'/wiki/<page>', 'wiki/page'), WikiHandler),
            ])

        Here are some examples of how to generate URLs for them:

        >>> url = app.router.build('home/main')
        /
        >>> url = app.router.build('home/main', _full=True, _request=Request.blank('/'))
        http://localhost:8080/
        >>> url = app.router.build('wiki/start')
        /wiki
        >>> url = app.router.build('wiki/start', _full=True, _request=Request.blank('/'))
        http://localhost:8080/wiki
        >>> url = app.router.build('wiki/start', _full=True, _anchor='my-heading', _request=Request.blank('/'))
        http://localhost:8080/wiki#my-heading
        >>> url = app.router.build('wiki/page', page='my-first-page')
        /wiki/my-first-page

        :param _name:
            The route name.
        :param _full:
            If True, returns an absolute URL. Otherwise returns a relative one.
        :param _secure:
            If True, returns an absolute URL using `https` scheme.
        :param _anchor:
            An anchor to append to the end of the URL.
        :param _request:
            The current ``Request`` object.
        :param kwargs:
            Keyword arguments to build the URL. All route variables that are
            not set as defaults must be passed, and they must conform to the
            format set in the route. Extra keywords are appended as URL
            arguments.
        :returns:
            An absolute or relative URL.
        """
        route = self.route_map.get(_name, None)
        if not route:
            raise KeyError('Route "%s" is not defined.' % _name)

        url = route.build(**kwargs)

        if _full or _secure:
            if _request is None:
                raise ValueError('A Request object must be passed to build '
                    'absolute URLs.')

            scheme = 'http'
            if _secure:
                scheme += 's'

            url = '%s://%s%s' % (scheme, _request.host, url)

        if _anchor:
            url += '#%s' % url_escape(_anchor)

        return url

    def __repr__(self):
        routes = self.routes + [v for k, v in self.route_map.iteritems() if \
            v not in self.routes]

        return 'Router(%r)' % routes

    __str__ = __repr__


class Config(dict):
    """A simple configuration dictionary keyed by module name. This is a
    dictionary of dictionaries. It requires all values to be dictionaries
    and applies updates and default values to the inner dictionaries instead
    of the first level one.

    The configuration object is available as a ``config`` attribute of the
    :class:`WSGIApplication`. If is instantiated and populated when the app is
    built::

        config = {}

        config['my.module'] = {
            'foo': 'bar',
            'baz': 'ding',
        }

        config['my.other.module'] = {
            'secret_key': 'try to guess me!',
        }

        app = WSGIApplication(config=config)

    Then to read configuration values, use :meth:`RequestHandler.get_config`::

        class MyHandler(RequestHandler):
            def get(self):
                foo = self.get_config('my.module', 'foo')

                secret_key = self.get_config('my.other.module', 'secret_key')

                # ...
    """
    #: Loaded module configurations.
    loaded = None

    def __init__(self, value=None, default=None, loaded=None):
        """Initializes the configuration object.

        :param value:
            A dictionary of configuration dictionaries for modules.
        :param default:
            A dictionary of configuration dictionaries for default values.
        :param loaded:
            A list of modules to be marked as loaded.
        """
        self.loaded = loaded or []
        if value is not None:
            assert isinstance(value, dict)
            for module in value.keys():
                self.update(module, value[module])

        if default is not None:
            assert isinstance(default, dict)
            for module in default.keys():
                self.setdefault(module, default[module])

    def __setitem__(self, module, value):
        """Sets a configuration for a module, requiring it to be a dictionary.

        :param module:
            A module name for the configuration, e.g.: 'webapp2.plugins.i18n'.
        :param value:
            A dictionary of configurations for the module.
        """
        assert isinstance(value, dict)
        super(Config, self).__setitem__(module, value)

    def update(self, module, value):
        """Updates the configuration dictionary for a module.

        >>> cfg = Config({'webapp2.plugins.i18n': {'locale': 'pt_BR'})
        >>> cfg.get('webapp2.plugins.i18n', 'locale')
        pt_BR
        >>> cfg.get('webapp2.plugins.i18n', 'foo')
        None
        >>> cfg.update('webapp2.plugins.i18n', {'locale': 'en_US', 'foo': 'bar'})
        >>> cfg.get('webapp2.plugins.i18n', 'locale')
        en_US
        >>> cfg.get('webapp2.plugins.i18n', 'foo')
        bar

        :param module:
            The module to update the configuration, e.g.:
            'webapp2.plugins.i18n'.
        :param value:
            A dictionary of configurations for the module.
        :returns:
            None.
        """
        assert isinstance(value, dict)
        if module not in self:
            self[module] = {}

        self[module].update(value)

    def setdefault(self, module, value):
        """Sets a default configuration dictionary for a module.

        >>> cfg = Config({'webapp2.plugins.i18n': {'locale': 'pt_BR'})
        >>> cfg.get('webapp2.plugins.i18n', 'locale')
        pt_BR
        >>> cfg.get('webapp2.plugins.i18n', 'foo')
        None
        >>> cfg.setdefault('webapp2.plugins.i18n', {'locale': 'en_US', 'foo': 'bar'})
        >>> cfg.get('webapp2.plugins.i18n', 'locale')
        pt_BR
        >>> cfg.get('webapp2.plugins.i18n', 'foo')
        bar

        :param module:
            The module to set default configuration, e.g.:
            'webapp2.plugins.i18n'.
        :param value:
            A dictionary of configurations for the module.
        :returns:
            None.
        """
        assert isinstance(value, dict)
        if module not in self:
            self[module] = {}

        for key in value.keys():
            self[module].setdefault(key, value[key])

    def get(self, module, key=None, default=None):
        """Returns a configuration value for given key in a given module.

        >>> cfg = Config({'webapp2.plugins.i18n': {'locale': 'pt_BR'})
        >>> cfg.get('webapp2.plugins.i18n')
        {'locale': 'pt_BR'}
        >>> cfg.get('webapp2.plugins.i18n', 'locale')
        pt_BR
        >>> cfg.get('webapp2.plugins.i18n', 'invalid-key')
        None
        >>> cfg.get('webapp2.plugins.i18n', 'invalid-key', 'default-value')
        default-value

        :param module:
            The module to get a configuration from, e.g.:
            'webapp2.plugins.i18n'.
        :param key:
            The key from the module configuration.
        :param default:
            A default value to return in case the configuration for
            the module/key is not set.
        :returns:
            The configuration value.
        """
        if module not in self:
            return default

        if key is None:
            return self[module]
        elif key not in self[module]:
            return default

        return self[module][key]

    def load_and_get(self, module, key=None, default=REQUIRED_VALUE):
        """Returns a configuration value for a module. If it is not already
        set, loads a ``default_config`` variable from the given module,
        updates the app configuration with those default values and returns
        the value for the given key. If the key is still not available,
        returns the provided default value or raises an exception if no
        default was provided.

        Every module that allows some kind of configuration sets a
        ``default_config`` global variable that is loaded by this function,
        cached and used in case the requested configuration was not defined
        by the user.

        :param module:
            The configured module.
        :param key:
            The config key.
        :param default:
            A default value to return in case the configuration for
            the module/key is not set.
        :returns:
            A configuration value.
        """
        if module not in self.loaded:
            # Load default configuration and update config.
            values = import_string(module + '.default_config', silent=True)
            if values:
                self.setdefault(module, values)

            self.loaded.append(module)

        value = self.get(module, key, default)
        if value is not REQUIRED_VALUE:
            return value

        if key is None:
            raise KeyError('Module %s is not configured.' % module)
        else:
            raise KeyError('Module %s requires the config key "%s" to be '
                'set.' % (module, key))


class WSGIApplication(object):
    """Wraps a set of webapp RequestHandlers in a WSGI-compatible application.

    To use this class, pass a list of tuples ``(route, RequestHandler class)``
    to the constructor, and pass the class instance to a WSGI handler.
    Example::

        from webapp2 import RequestHandler, WSGIApplication

        class HelloWorldHandler(RequestHandler):
            def get(self):
                self.response.out.write('Hello, World!')

        app = WSGIApplication([
            (r'/', HelloWorldHandler),
        ])

        def main():
            app.run()

        if __name__ == '__main__':
            main()

    The URL mapping is first-match based on the list ordering. The route
    definition can be an object that implements the method ``match(request)``.
    The provided class :class:`Route` is a route implementation that allows
    reversible URLs and keyword arguments passed to the handler. Example::

        app = WSGIApplication([
            (Route(r'/articles', 'articles'), ArticlesHandler),
            (Route(r'/articles/<id:[\d]+>', 'article', {'id': '1'}), ArticleHandler),
        ])

    .. seealso:: :class:`Route`.
    """
    #: Default class used for the request object.
    request_class = Request
    #: Default class used for the response object.
    response_class = Response
    #: Default class used for the router object.
    router_class = Router
    #: Default class used for the config object.
    config_class = Config
    #: A dictionary mapping HTTP error codes to :class:`RequestHandler`
    #: classes used to handle them. The handler set for status 500 is used
    #: as default if others are not set.
    error_handlers = {}

    def __init__(self, routes=None, debug=False, config=None):
        """Initializes the WSGI application.

        :param routes:
            List of URL definitions as tuples ``(route, RequestHandler class)``.
        :param debug:
            True if this is debug mode, False otherwise.
        :param config:
            A configuration dictionary for the application.
        """
        self.debug = debug
        self.router = self.router_class(routes)
        self.config = self.config_class(config)

    def __call__(self, environ, start_response):
        """Called by WSGI when a request comes in. Calls :meth:`wsgi_app`."""
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        """This is the actual WSGI application.  This is not implemented in
        :meth:`__call__` so that middlewares can be applied without losing a
        reference to the class. So instead of doing this::

            app = MyMiddleware(app)

        It's a better idea to do this instead::

            app.wsgi_app = MyMiddleware(app.wsgi_app)

        Then you still have the original application object around and
        can continue to call methods on it.

        This idea comes from `Flask <http://flask.pocoo.org/>`_.

        :param environ:
            A WSGI environment.
        :param start_response:
            A callable accepting a status code, a list of headers and an
            optional exception context to start the response.
        """
        try:
            self.request = request = self.request_class(environ)
            response = self.response_class()

            if request.method not in _ALLOWED_METHODS:
                # 501 Not Implemented.
                raise webob.exc.HTTPNotImplemented()

            self.router.dispatch(self, request, response)
        except Exception, e:
            try:
                self.handle_exception(request, response, e)
            except webob.exc.WSGIHTTPException, e:
                # Use the exception as response.
                response = e
            except Exception, e:
                # Our last chance to handle the error.
                if self.debug:
                    raise

                # 500 Internal Server Error: nothing else to do.
                response = webob.exc.HTTPInternalServerError()
        finally:
            self.request = None

        return response(environ, start_response)

    def handle_exception(self, request, response, e):
        """Handles an exception. Searches :attr:`error_handlers` for a handler
        with the error code, if it is a :class:`HTTPException`, or the 500
        status code as fall back. Dispatches the handler if found, or re-raises
        the exception to be caught by :class:`WSGIApplication`.

        :param request:
            A ``webapp.Request`` instance.
        :param response:
            A :class:`Response` instance.
        :param e:
            The raised exception.
        """
        logging.exception(e)
        if self.debug:
            raise

        if isinstance(e, HTTPException):
            code = e.code
        else:
            code = 500

        handler = self.error_handlers.get(code) or self.error_handlers.get(500)
        if handler:
            # Handle the exception using a custom handler.
            handler(self, request, response)('get', exception=e)
        else:
            # No exception handler. Catch it in the WSGI app.
            raise

    def url_for(self, _name, _full=False, _secure=False, _anchor=None,
        **kwargs):
        """Builds and returns a URL for a named :class:`Route`.

        .. seealso:: :meth:`Router.build`.
        """
        return self.router.build(_name, _full=_full, _secure=_secure,
            _anchor=_anchor, _request=self.request, **kwargs)

    def get_config(self, module, key=None, default=REQUIRED_VALUE):
        """Returns a configuration value for a module.

        .. seealso:: :meth:`Config.load_and_get`.
        """
        return self.config.load_and_get(module, key=key, default=default)

    def run(self, bare=False):
        """Runs the app using ``google.appengine.ext.webapp.util.run_wsgi_app``.
        This is generally called inside a ``main()`` function of the file
        mapped in *app.yaml* to run the application::

            # ...

            app = WSGIApplication([
                (Route(r'/'), HelloWorldHandler),
            ])

            def main():
                app.run()

            if __name__ == '__main__':
                main()

        :param bare:
            If True, uses ``run_bare_wsgi_app`` instead of ``run_wsgi_app``,
            which doesn't add WSGI middleware.
        """
        if bare:
            run_bare_wsgi_app(self)
        else:
            run_wsgi_app(self)


class LazyObject(object):
    """An object that is only imported when called.

    Example::

        handler_class = LazyObject('my.module.MyHandler')
        handler = handler_class(app, request, response)
    """
    def __init__(self, import_name):
        """Initializes a lazy object.

        :param import_name:
            The dotted name for the object to import, e.g.,
            ``my.module.MyClass``.
        """
        self.import_name = import_name
        self.obj = None

    def __call__(self, *args, **kwargs):
        if self.obj is None:
            self.obj = import_string(self.import_name)

        return self.obj(*args, **kwargs)


def abort(code, *args, **kwargs):
    """Raises an ``HTTPException``. The exception is instantiated passing
    *args* and *kwargs*.

    :param code:
        A valid HTTP error code from ``webob.exc.status_map``, a dictionary
        mapping status codes to subclasses of ``HTTPException``.
    :param args:
        Arguments to be used to instantiate the exception.
    :param kwargs:
        Keyword arguments to be used to instantiate the exception.
    """
    cls = webob.exc.status_map.get(code) or webob.exc.status_map.get(500)
    raise cls(*args, **kwargs)


def get_valid_methods(handler):
    """Returns a list of HTTP methods supported by a handler.

    :param handler:
        A :class:`RequestHandler` instance.
    :returns:
        A list of HTTP methods supported by the handler.
    """
    return [m for m in _ALLOWED_METHODS if getattr(handler, m.lower(), None)]


def import_string(import_name, silent=False):
    """Imports an object based on a string. If `silent` is True the return
    value will be None if the import fails.

    Simplified version of the function with same name from
    `Werkzeug <http://werkzeug.pocoo.org/>`_.

    :param import_name:
        The dotted name for the object to import.
    :param silent:
        If True, import errors are ignored and None is returned instead.
    :returns:
        The imported object.
    """
    import_name = to_utf8(import_name)
    try:
        if '.' in import_name:
            module, obj = import_name.rsplit('.', 1)
        else:
            return __import__(import_name)

        return getattr(__import__(module, None, None, [obj]), obj)
    except (ImportError, AttributeError):
        if not silent:
            raise


def url_escape(value):
    """Returns a valid URL-encoded version of the given value.

    This function comes from `Tornado`_.

    :param value:
        A URL to be encoded.
    :returns:
        The encoded URL.
    """
    return urllib.quote_plus(to_utf8(value))


def url_unescape(value):
    """Decodes the given value from a URL.

    This function comes from `Tornado`_.

    :param value:
        A URL to be decoded.
    :returns:
        The decoded URL.
    """
    return to_unicode(urllib.unquote_plus(value))


def to_utf8(value):
    """Returns a string encoded using UTF-8.

    This function comes from `Tornado`_.

    :param value:
        A unicode or string to be encoded.
    :returns:
        The encoded string.
    """
    if isinstance(value, unicode):
        return value.encode('utf-8')

    assert isinstance(value, str)
    return value


def to_unicode(value):
    """Returns a unicode string from a string, using UTF-8 to decode if needed.

    This function comes from `Tornado`_.

    :param value:
        A unicode or string to be decoded.
    :returns:
        The decoded string.
    """
    if isinstance(value, str):
        return value.decode('utf-8')

    assert isinstance(value, unicode)
    return value
