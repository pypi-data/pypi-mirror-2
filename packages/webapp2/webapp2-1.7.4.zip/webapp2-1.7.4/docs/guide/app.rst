.. _guide.app:

The WSGI application
====================
The WSGI application receives requests and dispatches the appropriate handler,
returning a response to the client. It stores the URI routes that the app will
accept, configuration variables and registered objects that can be shared
between requests. The WSGI app is also responsible for handling uncaught
exceptions, avoiding that stack traces "leak" to the client when in production.
Let's take a look at it more deeply now.


Initialization
--------------
The :class:`webapp2.WSGIApplication` class is initialized with three optional
arguments:

- ``routes``: a list of route definitions as described in :ref:`guide.routing`.
- ``debug``: a boolean flag that enables debug mode.
- ``config``: a dictionary of configuration values for the application.

Compared to webapp, only config was added; it is used as a standard way to
configure extra modules (sessions, internationalization, templates or your
own app configuration values).

Everything is pretty straighforward::

    import webapp2

    routes = [
        (r'/', 'handlers.HelloWorldHandler'),
    ]

    config = {}
    config['webapp2_extras.sessions'] = {
        'secret_key': 'something-very-very-secret',
    }

    app = webapp2.WSGIApplication(routes=routes, debug=True, config=config)


Getting the current app
-----------------------
The active ``WSGIApplication`` instance can be accessed at any place of your
app using the function :func:`webapp2.get_app`. This is useful, for example, to
access the app registry or configuration values::

    import webapp2

    app = webapp2.get_app()
    config_value = app.config.get('my-config-key')

The application instance is stored as a class attribute, which is fine on App
Engine because there are no concurrent requests for the same Python interpreter
instance. For threaded environments, an application that supports threads must
be used as described in the :ref:`tutorials.quickstart.nogae` tutorial.


.. _guide.app.router:

Router
------
:ref:`guide.routing` is a central piece in webapp2, and its main component is
the :class:`webapp2.Router` class, available in the application as the
:attr:`webapp2.WSGIApplication.router` attribute.

Using the ``router`` attribute you can, for example, add new routes to the
application after initialization using the ``add()`` method::

    import webapp2

    app = webapp2.WSGIApplication()
    app.router.add((r'/', 'handlers.HelloWorldHandler'))

The router also has several methods that allows you to override how URIs are
matched, dispatched or built without even requiring subclassing. Check the
:class:`Router API documentation <webapp2.Router>` for a description of the
methods :meth:`webapp2.Router.set_matcher`,
:meth:`webapp2.Router.set_dispatcher` and :meth:`webapp2.Router.set_builder`.


.. _guide.app.config:

Config
------
When instantiating the app, you can pass a configuration dictionary which is
then accessible through the :attr:`webapp2.WSGIApplication.config` attribute.
A convention is to define configuration keys for each module, to avoid name
clashes, but you can define them as you wish, really, unless the module
requires a specific setup. First you define a configuration::

    import webapp2

    config = {'foo': 'bar'}

    app = webapp2.WSGIApplication(routes=[
        (r'/', 'handlers.MyHandler'),
    ], config=config)

Then access it as you need. Inside a ``RequestHandler``, for example::

    import webapp2

    class MyHandler(webapp2.RequestHandler):
        def get(self):
            foo = self.app.config.get('foo')
            self.response.write('foo value is %s' % foo)


.. _guide.app.registry:

Registry
--------
A simple dictionary is available in the application to register instances that
are shared between requests: it is the :attr:`webapp2.WSGIApplication.registry`
attribute. It can be used by anything that your app requires and the intention
is to avoid global variables in modules, so that you can have multiple app
instances using different configurations: each app has its own extra instances
for any kind of object that is shared between requests. A simple example that
registers a fictitious ``MyParser`` instance if it is not yet registered::

    import webapp2

    def get_parser():
        app = webapp2.get_app()
        # Check if the instance is already registered.
        my_parser = app.registry.get('my_parser')
        if not my_parser:
            # Import the class lazily.
            cls = webapp2.import_string('my.module.MyParser')
            # Instantiate the imported class.
            my_parser = cls()
            # Register the instance in the registry.
            app.registry['my_parser'] = my_parser

        return my_parser

The registry can be used to lazily instantiate objects when needed, and keep a
reference in the application to be reused.


Error handlers
--------------
As described in :ref:`guide.exceptions`, a dictionary is available in the app
to register error handlers as the :attr:`webapp2.WSGIApplication.error_handlers`
attribute. They will be used as a last resource if exceptions are not caught
by handlers. It is a good idea to set at least error handlers for 404 and 500
status codes::

    import logging

    import webapp2

    def handle_404(request, response, exception):
        logging.exception(exception)
        response.write('Oops! I could swear this page was here!')
        response.set_status(404)

    def handle_500(request, response, exception):
        logging.exception(exception)
        response.write('A server error occurred!')
        response.set_status(500)

    app = webapp2.WSGIApplication([
        webapp2.Route(r'/', handler='handlers.HomeHandler', name='home')
    ])
    app.error_handlers[404] = handle_404
    app.error_handlers[500] = handle_500


Debug flag
----------
A debug flag is passed to the WSGI application on instantiation and is
available as the :attr:`webapp2.WSGIApplication.debug` attribute. When in
debug mode, any exception that is now caught is raised and the stack trace is
displayed to the client, which helps debugging. When not in debug mode, a
'500 Internal Server Error' is displayed instead.

You can use that flag to set special behaviors for the application during
development.

For App Engine, it is possible to detect if the code is running using the SDK
or in production checking the 'SERVER_SOFTWARE' environ variable::

    import os

    import webapp2

    debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

    app = webapp2.WSGIApplication(routes=[
        (r'/', 'handlers.HelloWorldHandler'),
    ], debug=debug)


Thread-safe application
-----------------------
:class:`webapp2_extras.local_app.WSGIApplication` is a special class to be used
in threaded environments, e.g., outside App Engine. It uses thread-locals to
store request and app references, instead of simple class attributes which are
fine for App Engine. See in the :ref:`tutorials.quickstart.nogae` tutorial a
complete explanation about how to use it.


Running the app
---------------
The application is executed in a CGI environment using the method
:meth:`webapp2.WSGIApplication.run`. When using App Engine, it uses
the functions ``run_bare_wsgi_app`` or ``run_wsgi_app`` from
``google.appengine.ext.webapp.util``. Outside of App Engine, it uses the
:py:mod:`wsgiref.handlers` module. Here's the simplest example::

    import webapp2

    class HelloWebapp2(webapp2.RequestHandler):
        def get(self):
            self.response.write('Hello, webapp2!')

    app = webapp2.WSGIApplication([
        ('/', HelloWebapp2),
    ], debug=True)

    def main():
        app.run()

    if __name__ == '__main__':
        main()


Unit testing
------------
As described in :ref:`guide.testing`, the application has a convenience method
to test handlers: :meth:`webapp2.WSGIApplication.get_response`. It
receives the same parameters as ``Request.blank()`` to build a request and call
the application, returning the resulting response from a handler::

    class HelloHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write('Hello, world!')

    app = webapp2.WSGIapplication([('/', HelloHandler)])

    # Test the app, passing parameters to build a request.
    response = app.get_response('/')
    assert response.status == '200 OK'
    assert response.body == 'Hello, world!'
