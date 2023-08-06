#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Example showing how to override the 
  :py:class:`~weblayer.interfaces.IPathRouter` component.
  
  Note that despite the ``Hello`` request handler being mapped to all request
  paths in the ``mapping``, the :py:class:`LazyPathRouter` will always return
  ``None, None, None``, resulting in a 404 response.
"""

from zope.interface import implements
from weblayer import Bootstrapper, RequestHandler, WSGIApplication
from weblayer.interfaces import IPathRouter

class LazyPathRouter(object):
    """ Never even bothers trying.
    """
    
    implements(IPathRouter)
    
    def match(self, path):
        return None, None, None
    


class Hello(RequestHandler):
    def get(self, world):
        return u'hello %s' % world
    


mapping = [(r'/(.*)', Hello)]

config = {
    'cookie_secret': '...', 
    'static_files_path': '/var/www/static',
    'template_directories': ['templates']
}

bootstrapper = Bootstrapper(settings=config, url_mapping=mapping)
application = WSGIApplication(*bootstrapper(path_router=LazyPathRouter()))

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8080, application).serve_forever()
