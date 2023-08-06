
==========
User Guide
==========

:ref:`weblayer` is made up of a number of components.  You can use them "out of
the box", as shown by the :ref:`helloworld` example, or you can pick and choose
from and override them, as introduced in the :ref:`Components` section.

You can then take advantage of the :ref:`request handler api` when writing your
web application.


.. _helloworld:

Hello World
===========

`helloworld.py`_ shows how to start writing a web application using 
:ref:`weblayer`'s default configuration:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 7-

Let's walk through it.  First up, we import 
:py:class:`~weblayer.bootstrap.Bootstrapper`, 
:py:class:`~weblayer.request.RequestHandler` and 
:py:class:`~weblayer.wsgi.WSGIApplication`:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 7

Handling Requests
-----------------

We then see ``Hello``, a simple request handler (aka "view") that subclasses
the :py:class:`~weblayer.request.RequestHandler` class we imported:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 9-13

``Hello`` defines a single method: ``get``, which will be called when ``Hello``
receives an `HTTP GET request`_.

.. note::

    By default, request handlers accept GET and HEAD requests (i.e.: they are
    theoretically read only).  You can explicitly specify which methods of
    each request handler should be exposed using the ``__all__`` property.
    
    For example, to handle HEAD, GET, POST and DOFOO requests, you might write
    something like::
    
        class Hello2(RequestHandler):
            """ I explicitly accept only HEAD, GET, POST and DOFOO requests.
            """
            
            __all__ = ('head', 'get', 'post', 'dofoo')
            
            def get(self):
                form = u'<form method="post"><input name="name" /></form>'
                return u'What is your name? %s' % form
            
            def post(self):
                return u'Hello %s!' % self.request.params.get('name')
            
            def dofoo(self):
                return u'I just did foo!'
            
        
    

.. note::
    
    In the above example, HEAD requests will be handled by the ``def get()``
    method.  This special case is carried through from the underlying 
    `webob.Response`_ implementation (and is documented in
    :py:meth:`~weblayer.method.ExposedMethodSelector.select_method`).  In most
    cases, the trick is simply to remember to include ``'head'`` in your 
    ``__all__`` list of exposed methods wherever you expose ``'get'``.

.. note::
    
    In order to protect against XSRF attacks, POST Requests (that are not
    XMLHttpRequest requests) are validated to check for the presence and value
    of an ``_xsrf`` parameter.  You can include this in your forms using the
    :py:attr:`~weblayer.request.RequestHandler.xsrf_input` (available as
    ``xrsf_input`` in your templates, e.g.::
    
        <form>
          ${xsrf_input}
        </form>
    
    You can disable XSRF validation using an application level
    :py:mod:`~weblayer.settings`, specifically the ``check_xsrf`` setting,
    or by overriding the ``check_xsrf``
    :py:class:`~weblayer.request.RequestHandler` class attribute, e.g.::
    
        class Hello3(RequestHandler):
            """ I don't validate POST requests against XSRF request forgery.
            """
            
            check_xsrf = False
            
        
    

Handlers are mapped to incoming requests using the incoming request path.
This mapping takes the form of a list of tuples where the first item in the
tuple is a `regular expression`_ and the second is a
:py:class:`~weblayer.request.RequestHandler` class.

In this case, we map ``Hello`` to all incoming requests:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 15

The `groups`_ in the `regular expression`_ (i.e.: the parts with parenthesis
around them) that match the request path are passed to the appropriate method
of the request handler as arguments.  So, in this case, an `HTTP GET request`_
to ``/foo`` will yield one match group, ``'foo'`` which is passed into 
``Hello.get`` as the positional argument ``world``, resulting in the response
``u'hello foo'``.

You can see this for yourself by running::

    weblayer-demo

And then opening http://localhost:8080/foo in a web browser.

.. note::

    The pattern of using an explicit, ordered mapping of regular expressions
    to request handlers is used by many frameworks, including Google App
    Engine's `webapp`_ framework.  Other common patterns include `routes`_ and
    `traversal`_, sometimes used in tandem with `declarative configuration`_
    and  / or `decorators`_.  
    
    :ref:`weblayer` avoids declarative configuration by default.  Decorators
    are not explicit and can introduce problems, as `explained here`_.
    
    Regular expressions are preferred over `routes`_ as they are both more
    powerful and an essential part of any Python developer's toolbox.  It seems
    strange to invent another tool for the job when such a good one already
    exists.  
    
    Finally, `traversal`_ implies there is an object graph to traverse, which
    is not always the case.
    
    You may, of course, disagree with this analysis and 
    :ref:`override <components>` the 
    :py:class:`~weblayer.interfaces.IPathRouter` implementation as you see fit.

Bootstrapping
-------------

Carrying on through the example, we next hardcode three configuration settings
that are required by default:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 17-21

We then initialise a :py:class:`~weblayer.bootstrap.Bootstrapper` with these
configuration settings and the url mapping we made earlier and use it to
bootstrap a :py:class:`~weblayer.wsgi.WSGIApplication`:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 23-24

.. note::
    
    The :py:class:`~weblayer.bootstrap.Bootstrapper` is similar to `repoze.bfg's Configurator`_ in that it allows for imperative configuration of components.

.. note::
    
    :py:mod:`~weblayer.settings` implements a pattern of optional explicit
    declaration of settings that is inspired by `tornado.options`_.  
    Explicitly requiring settings allows the application to throw an error
    on initialisation, rather than further down the line (e.g.: when a 
    request happens to come in).
    
    If you choose to, you can explicitly require your own settings by calling
    :py:func:`~weblayer.settings.require_setting` at module level.  For
    example, the ``cookie_secret`` requirement is defined at the top of
    :py:mod:`weblayer.cookie` using:
    
    .. literalinclude:: ../src/weblayer/cookie.py
       :lines: 42
    
    Because :py:func:`~weblayer.settings.require_setting` works in tandem with
    a `venusian scan`_ to prevent `duplicate import issues`_, to require your
    own settings, you must tell :ref:`weblayer` to scan the modules you've
    required them in.
    
    This can be done most simply by passing in a list of
    dotted names of modules or packages using the ``packages`` keyword argument
    to :py:meth:`Bootstrapper.__call__ <weblayer.bootstrap.Bootstrapper.__call__>`.
    For example, to require all settings declared using 
    :py:func:`~weblayer.settings.require_setting` in modules in the ``my.webapp``
    and ``some.dependency`` packages, use::
    
        application = WSGIApplication(
            *bootstrapper(packages=['my.webapp', 'some.dependency',])
        )
    

Serving
-------

Finally, the remainder of the example takes care of serving the example
application on http://localhost:8080:

.. literalinclude:: ../src/weblayer/examples/helloworld.py
   :lines: 26-

For more realistic setups, see the :ref:`Deployment` recipes.


.. _components:

Components
==========

Architecture
------------

:ref:`weblayer` uses the `Zope Component Architecture`_ under
the hood.  Individual components are said to `implement`_ one of 
:py:mod:`weblayer.interfaces`, listed in ``weblayer.interfaces.__all__``:

.. literalinclude:: ../src/weblayer/interfaces.py
   :lines: 12-25

For example, :py:class:`~weblayer.route.RegExpPathRouter`::
    
    class RegExpPathRouter(object):
        """ Routes paths to request handlers using regexp patterns.
        """
        
        implements(IPathRouter)
        
        # ``__init__`` method removed from this example for brevity
        
        def match(self, path):
            
            for regexp, handler_class in self._mapping:
                match = regexp.match(path)
                if match:
                    return handler_class, match.groups(), {}
                
            return None, None, None
            
        
    

Is one particular implementation of 
:py:class:`~weblayer.interfaces.IPathRouter`::

    class IPathRouter(Interface):
        """ Maps incoming requests to request handlers using the request path.
        """
        
        def match(path):
            """ Return ``handler, args, kwargs`` from ``path``.
            """
            
        
    

Default Implementations
-----------------------

The default implementations are as follows:

* :py:class:`~weblayer.interfaces.IAuthenticationManager` is implemented by
  :py:class:`~weblayer.auth.TrivialAuthenticationManager`
* :py:class:`~weblayer.interfaces.IMethodSelector` is implemented by
  :py:class:`~weblayer.method.ExposedMethodSelector`
* :py:class:`~weblayer.interfaces.IPathRouter` is implemented by
  :py:class:`~weblayer.route.RegExpPathRouter`
* :py:class:`~weblayer.interfaces.IRequest` is implemented by
  :py:class:`~weblayer.base.Request`
* :py:class:`~weblayer.interfaces.IRequestHandler` is implemented by
  :py:class:`~weblayer.request.RequestHandler`
* :py:class:`~weblayer.interfaces.IResponse` is implemented by
  :py:class:`~weblayer.base.Response`
* :py:class:`~weblayer.interfaces.IResponseNormaliser` is implemented by
  :py:class:`~weblayer.normalise.DefaultToJSONResponseNormaliser`
* :py:class:`~weblayer.interfaces.ISecureCookieWrapper` is implemented by
  :py:class:`~weblayer.cookie.SignedSecureCookieWrapper`
* :py:class:`~weblayer.interfaces.ISettings` is implemented by
  :py:class:`~weblayer.settings.RequirableSettings`
* :py:class:`~weblayer.interfaces.IStaticURLGenerator` is implemented by
  :py:class:`~weblayer.static.MemoryCachedStaticURLGenerator`
* :py:class:`~weblayer.interfaces.ITemplateRenderer` is implemented by
  :py:class:`~weblayer.template.MakoTemplateRenderer`
* :py:class:`~weblayer.interfaces.IWSGIApplication` is implemented by
  :py:class:`~weblayer.wsgi.WSGIApplication`

Workflow
--------

Each application requires an :py:class:`~weblayer.interfaces.ISettings`
implementation and an :py:class:`~weblayer.interfaces.IPathRouter`.  These are
passed in to your :py:class:`~weblayer.interfaces.IWSGIApplication` when it is 
initialised, most commonly using the 
:py:class:`~weblayer.bootstrap.Bootstrapper`.

When HTTP requests come in to your application,
:py:class:`~weblayer.interfaces.IWSGIApplication` uses the
:py:class:`~weblayer.interfaces.IPathRouter` to map the incoming requests to an
:py:class:`~weblayer.interfaces.IRequestHandler` that is instantiated with an
:py:class:`~weblayer.interfaces.IRequest`, 
:py:class:`~weblayer.interfaces.IResponse` and the
:py:class:`~weblayer.interfaces.ISettings`.

The :py:class:`~weblayer.interfaces.IRequestHandler` then uses the
:py:class:`~weblayer.interfaces.IMethodSelector` to select which of its methods
(``def get()``, ``def post()`` etc.) to call to handle the request.  The method
is then called with ``*args`` and ``**kwargs`` derived from the incoming
request path by the :py:class:`~weblayer.interfaces.IPathRouter`.

When writing :py:class:`~weblayer.interfaces.IRequestHandler` code, you can 
take advantage of the :ref:`request handler api` to access your
:py:class:`~weblayer.interfaces.IStaticURLGenerator` at ``self.static``, your
:py:class:`~weblayer.interfaces.IAuthenticationManager` at ``self.auth`` and
your :py:class:`~weblayer.interfaces.ISecureCookieWrapper` at ``self.cookies``.
Your :py:class:`~weblayer.interfaces.ITemplateRenderer` is available through 
``self.render()``.

The return value of your handler method is passed to your
:py:class:`~weblayer.interfaces.IResponseNormaliser`, which uses it to either
replace or update the :py:class:`~weblayer.interfaces.IResponse` originally
passed in to your :py:class:`~weblayer.interfaces.IRequestHandler` before the
:py:class:`~weblayer.interfaces.IResponse` is called to provide a `WSGI`_
compliant response from your application.

Overriding
----------

Alternative component implementations need to declare that they implement the
appropriate interface and provide the attributes and methods that the
interface specifies.  For example, an alternative 
:py:class:`~weblayer.interfaces.IPathRouter` implementation needs to provide
a ``match(path)`` method, e.g.::

    class LazyPathRouter(object):
        """ Never even bothers trying.
        """
        
        implements(IPathRouter)
        
        def match(self, path):
            return None, None, None
        
    

The simplest way to then register this component is using the
:py:class:`~weblayer.bootstrap.Bootstrapper` when bootstrapping the
:py:class:`~weblayer.wsgi.WSGIApplication`.  The `override/path_router.py`_
example shows how:

.. literalinclude:: ../src/weblayer/examples/override/path_router.py
   :lines: 12-

If you then run this, all requests will meet with a 404 response::

    $ python src/weblayer/examples/override_path_router.py 
    ... "GET / HTTP/1.1" 404 0
    ... "GET /foo HTTP/1.1" 404 0

You can see two further examples at `override/authentication_manager.py`_
and `override/template_renderer.py`_

.. note::

    Using the :py:class:`~weblayer.bootstrap.Bootstrapper` to register
    components is entirely optional.  You can register components manually
    using (or even by monkey patching) the :py:mod:`weblayer.component` 
    ``registry``.


.. _`request handler api`:

Request Handler API
===================

:py:class:`~weblayer.request.RequestHandler` provides the following useful
attributes and methods:

* ``self.request`` is an :py:class:`~weblayer.interfaces.IRequest` instance
  encapsulating the incoming HTTP request
* ``self.response`` is an :py:class:`~weblayer.interfaces.IResponse` instance
  you can choose to manipulate and return (or update indirectly through the
  :py:class:`~weblayer.interfaces.IResponseNormaliser`)
* ``self.settings`` is an :py:class:`~weblayer.interfaces.ISettings` instance
  that provides dictionary-like access to your :py:mod:`~weblayer.settings`
* ``self.auth`` is an :py:class:`~weblayer.interfaces.IAuthenticationManager`
  instance that provides 
  :py:attr:`~weblayer.interfaces.IAuthenticationManager.is_authenticated` and
  :py:attr:`~weblayer.interfaces.IAuthenticationManager.current_user`
  properties
* ``self.cookies`` is an :py:class:`~weblayer.interfaces.ISecureCookieWrapper`
  instance that provides methods to 
  :py:meth:`~weblayer.interfaces.ISecureCookieWrapper.set` and
  :py:meth:`~weblayer.interfaces.ISecureCookieWrapper.get` secure cookies
* ``self.static`` is an an :py:class:`~weblayer.interfaces.IStaticURLGenerator`
  instance that provides a 
  :py:meth:`~weblayer.interfaces.IStaticURLGenerator.get_url` method to
  generate static URLs
* ``self.xsrf_input`` is an html ``<input />`` element you can include in forms
  to protect against XSRF attacks
* return ``self.error()`` to return an HTTP error
* return ``self.redirect()`` to redirect the request
* return ``self.render()`` to return a rendered template

.. note::
    
    When you use ``self.render()``, it passes through any keyword arguments
    you provide, along with ``self.request`` as ``request``, 
    ``self.auth.current_user`` as ``current_user``, ``self.static.get_url()``
    as ``get_static_url()`` and ``self.xsrf_input`` as ``xsrf_input`` to the
    template namespace (along with any built-ins your 
    :py:class:`~weblayer.interfaces.ITemplateRenderer` implementation 
    provides).


.. _`helloworld.py`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/helloworld.py
.. _`override/path_router.py`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/override/path_router.py
.. _`override/authentication_manager.py`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/override/authentication_manager.py
.. _`override/template_renderer.py`: http://github.com/thruflo/weblayer/tree/master/src/weblayer/examples/override/template_renderer.py

.. _`webob.Response`: http://pythonpaste.org/webob/reference.html#id2
.. _`HTTP GET request`: http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.3
.. _`regular expression`: http://docs.python.org/library/re.html
.. _`groups`: http://docs.python.org/library/re.html#re.MatchObject.groups

.. _`webapp`: http://code.google.com/appengine/docs/python/tools/webapp/
.. _`routes`: http://routes.groovie.org/
.. _`traversal`: http://docs.repoze.org/bfg/narr/traversal.html
.. _`declarative configuration`: http://docs.repoze.org/bfg/1.2/narr/configuration.html
.. _`decorators`: http://bottle.paws.de/docs/dev/tutorial.html#routing
.. _`explained here`: http://docs.repoze.org/bfg/current/designdefense.html#application-programmers-don-t-control-the-module-scope-codepath-import-time-side-effects-are-evil
.. _`duplicate import issues`: http://docs.repoze.org/bfg/current/designdefense.html#application-programmers-don-t-control-the-module-scope-codepath-import-time-side-effects-are-evil
.. _`tornado.options`: https://github.com/facebook/tornado/blob/master/tornado/options.py

.. _`venusian scan`: http://docs.repoze.org/venusian/
.. _`repoze.bfg's Configurator`: http://docs.repoze.org/bfg/narr/configuration.html
.. _`deployment`: recipes#deployment

.. _`implement`: http://pypi.python.org/pypi/zope.interface#declaring-implemented-interfaces

.. _`wsgi`: http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
.. _`zope component architecture`: http://pypi.python.org/pypi/zope.component