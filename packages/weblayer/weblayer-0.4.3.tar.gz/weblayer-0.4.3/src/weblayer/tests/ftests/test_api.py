#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Functional tests for a :ref:`weblayer` application using the 
  :ref:`request handler api`.
"""

import unittest

class TestBasics(unittest.TestCase):
    """ Sanity check the basics of hooking up a request handler and returning
      a simple response.
    """
    
    def make_app(self, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'check_xsrf': False,
            'cookie_secret': '...',
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_hello_world(self):
        """ Can we hook up a request handler with a positional argument
          from the request path and return a simple response?
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, world):
                return u'hello %s' % world
            
        
        
        mapping = [(r'/(.*)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/world')
        
        self.assertTrue(res.body == 'hello world')
        
    
    def test_unicode_response(self):
        """ Can we return unicode characters?
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self):
                return u'hello Ð'
            
        
        
        mapping = [(r'/', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/')
        
        self.assertTrue(res.unicode_body == u'hello Ð')
        
    
    def test_mapping(self):
        """ Can we hook up multiple handlers?
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return 'a'
            
        
        class B(RequestHandler):
            def get(self):
                return 'b'
            
        
        
        mapping = [(
                r'/a',
                A
            ), (
                r'/.*',
                B
            )
        ]
        
        app = self.make_app(mapping)
        
        res = app.get('/a')
        self.assertTrue(res.body == 'a')
        
        res = app.get('/foobar')
        self.assertTrue(res.body == 'b')
        
    
    def test_groups(self):
        """ Each group in the request path should be passed as to the handler
          method as a positional argument.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self, *args):
                return ''.join(args)
            
        
        
        mapping = [(r'/(.)/(.)/(.)', Handler)]
        
        app = self.make_app(mapping)
        res = app.get('/a/b/c')
        
        self.assertTrue(res.body == 'abc')
        
    
    def test_head_method(self):
        """ HEAD requests should use ``Hander.get`` iff ``'head'`` is exposed,
          ``get()`` is defined and ``head()`` isn't.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            def get(self):
                return 'hello'
            
        
        
        mapping = [(r'/', Handler)]
        
        app = self.make_app(mapping)
        res = app.head('/')
        
        self.assertTrue(res.headers['Content-Length'] == '5')
        
    
    def test_form_post(self):
        """ POST requests should call ``Hander.post``.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            
            __all__ = ('get', 'post')
            
            def get(self):
                form = u'<form method="post"><input name="name" /></form>'
                return u'What is your name? %s' % form
                
            
            def post(self):
                return u'Hello %s!' % self.request.params.get('name')
                
            
            
        
        
        mapping = [(r'/', Handler)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        form = res.form
        form['name'] = 'Brian'
        
        res = form.submit()
        self.assertTrue(res.body == 'Hello Brian!')
        
    
    

class TestResponse(unittest.TestCase):
    """ Sanity check response generation.
    """
    
    def make_app(self, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'cookie_secret': '...',
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_return_basestring(self):
        """ Returning a ``basestring`` from a request handler method should
          update the ``response.body``.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return 'hello'
            
        
        class B(RequestHandler):
            def get(self):
                return u'hellö'
            
        
        
        mapping = [(r'/a', A), (r'/b', B)]
        app = self.make_app(mapping)
        
        res = app.get('/a')
        self.assertTrue(res.body == 'hello')
        
        res = app.get('/b')
        self.assertTrue(res.unicode_body == u'hellö')
        
    
    def test_return_none(self):
        """ Returning ``None`` should fallback on ``self.response``.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                self.response.body = 'elephants'
                return None
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        self.assertTrue(res.body == 'elephants')
        
    
    def test_return_response(self):
        """ Returning an :py:class:`~weblayer.interfaces.IResponse` from a
          request handler method should overwrite and use ``self.response``.
        """
        
        from weblayer import RequestHandler
        from weblayer.base import Response
        
        class A(RequestHandler):
            def get(self):
                response = Response(body='fandango', request=self.request)
                response.environ['weblayer.test_return_response'] = 1
                return response
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/', extra_environ={'weblayer.test_return_response': 0})
        self.assertTrue(res.body == 'fandango')
        self.assertTrue(res.environ['weblayer.test_return_response'])
        
    
    def test_return_data(self):
        """ Returning something other than a ``basestring``, ``None`` or
          :py:class:`~weblayer.interfaces.IResponse`` should JSON encode it.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return {'a': 'b'}
            
        
        
        class B(RequestHandler):
            def get(self):
                return {'a': u'ß'}
            
        
        
        mapping = [(r'/a', A), (r'/b', B)]
        app = self.make_app(mapping)
        
        res = app.get('/a')
        self.assertTrue(res.body == '{"a": "b"}')
        
        res = app.get('/b')
        self.assertTrue(res.unicode_body == u'{"a": "ß"}')
        
    
    

class TestSettings(unittest.TestCase):
    """ Sanity check ``self.settings``.
    """
    
    def make_app(self, config, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_required_settings_misses_raises_error(self):
        """ You must provide required settings by default.
        """
        
        from weblayer import RequestHandler
        
        config = {}
        mapping = [(r'/', RequestHandler)]
        
        self.assertRaises(
            KeyError,
            self.make_app,
            config, 
            mapping
        )
        
        
    
    def test_settings_available(self):
        """ Settings are available as self.settings.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return '%s %s' % (
                    self.settings['cookie_secret'],
                    self.settings.get('not_present', None)
                )
            
        
        
        config = {
            'cookie_secret': '...',
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        mapping = [(r'/', A)]
        
        app = self.make_app(config, mapping)
        res = app.get('/')
        
        self.assertTrue(res.body == '... None')
        
    
    

class TestAuth(unittest.TestCase):
    """ Sanity check ``self.auth``.
    """
    
    def make_app(self, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'cookie_secret': '...',
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_unauthenticated(self):
        """ If there's no ``environ['REMOTE_USER']``, 
          ``self.auth.is_authenticated`` is ``False`` and 
          ``self.auth.current_user`` is ``None``.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return '%s %s' % (
                    self.auth.is_authenticated,
                    self.auth.current_user
                )
            
        
        
        mapping = [(r'/', A)]
        
        app = self.make_app(mapping)
        res = app.get('/')
        
        self.assertTrue(res.body == 'False None')
        
    
    def test_authenticated(self):
        """ If there is a ``environ['REMOTE_USER']``, 
          ``self.auth.is_authenticated`` is ``True`` and 
          ``self.auth.current_user`` is ``environ['REMOTE_USER']``.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return '%s %s' % (
                    self.auth.is_authenticated,
                    self.auth.current_user
                )
            
        
        
        mapping = [(r'/', A)]
        
        app = self.make_app(mapping)
        res = app.get('/', extra_environ={'REMOTE_USER': '123456'})
        
        self.assertTrue(res.body == 'True 123456')
        
    
    

class TestCookies(unittest.TestCase):
    """ Sanity check ``self.cookies``.
    """
    
    def make_app(self, cookie_secret, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'cookie_secret': cookie_secret,
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_set_and_get(self):
        """ We can set and get a cookie.
        """
        
        from weblayer import RequestHandler
        
        class SetCookie(RequestHandler):
            def get(self):
                self.cookies.set('name', 'value')
            
        
        class GetCookie(RequestHandler):
            def get(self):
                return self.cookies.get('name')
            
        
        mapping = [(r'/set', SetCookie), (r'/get', GetCookie)]
        app = self.make_app('abc', mapping)
        
        app.get('/set')
        res = app.get('/get')
        self.assertTrue(res.body == 'value')
        
    
    def test_forged_returns_none(self):
        """ If we set the value of the cookie without using 
          ``self.cookies.set()``, ``self.cookies.get()`` returns None.
        """
        
        from weblayer import RequestHandler
        
        class SetCookie(RequestHandler):
            def get(self):
                self.response.set_cookie('name', value='value')
            
        
        class GetCookie(RequestHandler):
            def get(self):
                return '%s' % self.cookies.get('name')
            
        
        mapping = [(r'/set', SetCookie), (r'/get', GetCookie)]
        app = self.make_app('abc', mapping)
        
        app.get('/set')
        res = app.get('/get')
        self.assertTrue(res.body == 'None')
        
    
    

class TestStatic(unittest.TestCase):
    """ Sanity check ``self.static``.
    """
    
    def setUp(self):
        """ Make sure ``./static/foo.js`` contains only::
          
              var foo = {};
          
        """
        
        from os.path import dirname, join as join_path
        file_path = join_path(dirname(__file__), 'static', 'foo.js')
        sock = open(file_path, 'w')
        sock.write('var foo = {};')
        sock.close()
        
    
    def tearDown(self):
        """ Make sure ``./static/foo.js`` contains only::
          
              var foo = {};
          
        """
        
        from os.path import dirname, join as join_path
        file_path = join_path(dirname(__file__), 'static', 'foo.js')
        sock = open(file_path, 'w')
        sock.write('var foo = {};')
        sock.close()
        
    
    def make_app(self, mapping, **extra_config):
        from os.path import dirname, join as join_path
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'cookie_secret': '...',
            'static_files_path': join_path(dirname(__file__), 'static'),
            'template_directories': ['templates']
        }
        config.update(extra_config)
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_no_qs_if_file_doesnt_exist(self):
        """ If the file doesn't exist, don't add a ``v=...`` part to the
          query string.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.static.get_url('not_there.js')
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        self.assertTrue(res.body == 'http://localhost/static/not_there.js')
        
    
    def test_qs_if_file_exists(self):
        """ If the file does exist, add the first few chars of a hash digest of
          of the file contents to the query string.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.static.get_url('foo.js')
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        self.assertTrue(res.body == 'http://localhost/static/foo.js?v=fc075b5')
        
    
    def test_qs_cached_in_memory_despite_file_content_changing(self):
        """ The hexdigest snippet is cached in memory and doesn't automatically
          update when the underlying file changes.
        """
        
        from os.path import dirname, join as join_path
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.static.get_url('foo.js')
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        self.assertTrue(res.body == 'http://localhost/static/foo.js?v=fc075b5')
        
        # change the file
        file_path = join_path(dirname(__file__), 'static', 'foo.js')
        sock = open(file_path, 'w')
        sock.write('var foo = {\'changed\': true};')
        sock.close()
        
        # the qs *hasn't* changed
        res = app.get('/')
        self.assertTrue(res.body == 'http://localhost/static/foo.js?v=fc075b5')
        
    
    def test_qs_changed_when_cache_cleared(self):
        """ If we clear the cache, then the underlying file content change
          is reflected in the query string.
        """
        
        from os.path import dirname, join as join_path
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.static.get_url('foo.js')
            
        
        class B(RequestHandler):
            def get(self):
                """ n.b.: this hack only clears the cache for this process.
                  Don't do this in real code.
                """
                
                static_files = self.settings['static_files_path']
                file_path = join_path(static_files, 'foo.js')
                
                del self.static._cache[file_path]
                
            
        
        
        mapping = [(r'/a', A), (r'/b', B)]
        app = self.make_app(mapping)
        
        res = app.get('/a')
        self.assertTrue(res.body == 'http://localhost/static/foo.js?v=fc075b5')
        
        # change the file
        file_path = join_path(dirname(__file__), 'static', 'foo.js')
        sock = open(file_path, 'w')
        sock.write('var foo = {\'changed\': true};')
        sock.close()
        
        # clear the cache
        res = app.get('/b')
        
        # the qs *has* changed
        res = app.get('/a')
        self.assertTrue(res.body == 'http://localhost/static/foo.js?v=114b07a')
        
        # clear the cache
        res = app.get('/b')
        
    
    def test_host_url(self):
        """ Uses the host url of the request.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.static.get_url('foo.js')
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/', extra_environ={'HTTP_HOST': 'foo.com:1234'})
        self.assertTrue(
            res.body == 'http://foo.com:1234/static/foo.js?v=fc075b5'
        )
        
    
    def test_static_host_url(self):
        """ Unless ``settings['static_host_url']`` is provided.
        """
        
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.static.get_url('foo.js')
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping, static_host_url='http://static.foo.com')
        
        res = app.get('/')
        self.assertTrue(
            res.body == 'http://static.foo.com/static/foo.js?v=fc075b5'
        )
        
        res = app.get('/', extra_environ={'HTTP_HOST': 'foo.com:1234'})
        self.assertTrue(
            res.body == 'http://static.foo.com/static/foo.js?v=fc075b5'
        )
        
    
    

class TestXSRF(unittest.TestCase):
    """ Sanity check validating against XSRF attacks.
    """
    
    def make_app(self, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'cookie_secret': '...',
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_form_post_using_xsrf_input(self):
        """ If ``self.xsrf_input`` is included in the form POST it validates.
        """
        
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            
            __all__ = ('get', 'post')
            
            def get(self):
                inputs = u'%s<input name="name" />' % self.xsrf_input
                form = u'<form method="post">%s</form>' % inputs
                return u'What is your name? %s' % form
                
            
            def post(self):
                return u'Hello %s!' % self.request.params.get('name')
                
            
            
        
        
        mapping = [(r'/', Handler)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        form = res.form
        form['name'] = 'Brian'
        
        res = form.submit()
        self.assertTrue(res.body == 'Hello Brian!')
        
    
    def test_form_post_without_xsrf_input(self):
        """ If ``self.xsrf_input`` is not included in the form POST it,
          fails to validate.
        """
        
        from webtest import AppError
        from weblayer import RequestHandler
        
        class Handler(RequestHandler):
            
            __all__ = ('get', 'post')
            
            def get(self):
                form = u'<form method="post"><input name="name" /></form>'
                return u'What is your name? %s' % form
                
            
            def post(self):
                """ Never gets called
                """
                
            
            
        
        
        mapping = [(r'/', Handler)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        form = res.form
        form['name'] = 'Brian'
        
        self.assertRaisesRegexp(AppError, '403 Forbidden', form.submit)
        
    
    

class TestError(unittest.TestCase):
    """ Sanity check ``self.error()``.
    """
    
    def make_app(self, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'cookie_secret': '...',
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_return_vanilla_error(self):
        """ Returning ``self.error()`` results in a 500 response.
        """
        
        from webtest import AppError
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.error()
            
        
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        self.assertRaisesRegexp(
            AppError, 
            '500 Internal Server Error', 
            app.get, 
            '/'
        )
        
    
    def test_return_specific_error(self):
        """ Returning a specific error results in an appropriate response.
        """
        
        from webtest import AppError
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.error(status=501)
            
        
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        self.assertRaisesRegexp(
            AppError, 
            '501 Not Implemented',
            app.get, 
            '/'
        )
        
    
    

class TestRedirect(unittest.TestCase):
    """ Sanity check ``self.redirect()``.
    """
    
    def make_app(self, mapping):
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'cookie_secret': '...',
            'static_files_path': 'static',
            'template_directories': ['templates']
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_redirect(self):
        """ Returning ``self.redirect(url)`` results in a 302 response.
        """
        
        from webtest import AppError
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.redirect('/b')
            
        
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        status = app.get('/').status
        self.assertTrue(status == '302 Found')
        
    
    def test_redirect_location(self):
        """ Returning ``self.redirect(url)`` uses either the host url or full
          url if provided.
        """
        
        from webtest import AppError
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.redirect('/b')
            
        
        
        class B(RequestHandler):
            def get(self):
                return self.redirect('http://foo.com/c')
            
        
        
        mapping = [(r'/a', A), (r'/b', B)]
        app = self.make_app(mapping)
        
        res = app.get('/a').follow()
        self.assertTrue(res.headers['location'] == 'http://foo.com/c')
        
    
    def test_permanent_redirect(self):
        """ Returning ``self.redirect(url, permanent=True)`` returns a 301.
        """
        
        from webtest import AppError
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                return self.redirect('/b', permanent=True)
            
        
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        status = app.get('/').status
        self.assertTrue(status == '301 Moved Permanently')
        
    

class TestRender(unittest.TestCase):
    """ Sanity check ``self.render()``.
    """
    
    def make_app(self, mapping):
        from os.path import dirname, join as join_path
        from webtest import TestApp
        from weblayer import Bootstrapper, WSGIApplication
        config = {
            'cookie_secret': '...',
            'static_files_path': join_path(dirname(__file__), 'static'),
            'template_directories': [join_path(dirname(__file__), 'templates')]
        }
        bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
        application = WSGIApplication(*bootstrapper())
        return TestApp(application)
        
    
    def test_builtins(self):
        """ Returning ``self.render(tmpl_name)`` renders ``tmpl_name``, passing
          through keyword arguments to the template's global namespace, along
          with the builtins defined in :py:mod:`~weblayer.template`.
        """
        
        import datetime
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            def get(self):
                kwargs = {
                    'url': 'http://foo.com/b ar',
                    'data': {'a': u'b'},
                }
                return self.render('builtins.tmpl', **kwargs)
            
        
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/')
        self.assertTrue('{&quot;a&quot;: &quot;b&quot;}' in res)
        self.assertTrue('http%3A%2F%2Ffoo.com%2Fb+ar' in res)
        self.assertTrue(datetime.datetime.min in res)
        
    
    def test_request_variables(self):
        """ Returning ``self.render(tmpl_name)`` renders ``tmpl_name``, passing
          through the ``request``, ``current_user``, ``get_static_url`` and 
          ``xsrf_input``.
        """
        
        from webtest import AppError
        from weblayer import RequestHandler
        
        class A(RequestHandler):
            __all__ = ('get', 'post')
            
            def get(self):
                return self.render('request.tmpl')
            
            
            def post(self):
                return u'Hello %s!' % self.request.params.get('name')
            
        
        mapping = [(r'/', A)]
        app = self.make_app(mapping)
        
        res = app.get('/?foo=bar', extra_environ={'REMOTE_USER': 'brian'})
        
        self.assertTrue('foo: bar' in res)
        self.assertTrue('user: brian' in res)
        self.assertTrue(
            'static url: http://localhost/static/not_present.js' in res
        )
        
        form = res.form
        form['name'] = 'Brian'
        
        res = form.submit()
        self.assertTrue(res.body == 'Hello Brian!')
        
    
    

