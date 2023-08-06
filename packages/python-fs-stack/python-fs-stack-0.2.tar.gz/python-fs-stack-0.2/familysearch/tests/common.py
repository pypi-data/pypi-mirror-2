"""Common functions used by tests in multiple test suites"""

import unittest
import wsgi_intercept

try:
    import pkg_resources
    def load_sample(filename):
        return pkg_resources.resource_string(__name__, filename)
except ImportError:
    import os.path
    data_dir = os.path.dirname(__file__)
    def load_sample(filename):
        return open(os.path.join(data_dir, filename)).read()

default_headers = {'Content-Type': 'application/json'}

def add_request_intercept(response, out_environ=None, status='200 OK',
                          host='www.dev.usys.org', port=80,
                          headers=default_headers):
    """Globally install a request intercept returning the provided response."""
    if out_environ is None:
        out_environ = {}
    def mock_app(environ, start_response):
        out_environ.update(environ)
        start_response(status, dict(headers).items())
        return iter(response)
    wsgi_intercept.add_wsgi_intercept(host, port, lambda: mock_app)
    return out_environ

def clear_request_intercpets():
    """Remove all installed request intercepts."""
    wsgi_intercept.remove_wsgi_intercept()

if not hasattr(unittest.TestCase, 'assertIn'):
    unittest.TestCase.assertIn = lambda self, member, container, msg=None: unittest.TestCase.assertTrue(self, member in container, msg)
if not hasattr(unittest.TestCase, 'assertNotIn'):
    unittest.TestCase.assertNotIn = lambda self, member, container, msg=None: unittest.TestCase.assertTrue(self, member not in container, msg)
