import os
import unittest

from pyramid.wsgi import wsgiapp
from pyramid.view import view_config
from pyramid.view import static

from zope.interface import Interface

from pyramid import testing

class INothing(Interface):
    pass

@view_config(for_=INothing)
@wsgiapp
def wsgiapptest(environ, start_response):
    """ """
    return '123'

class WGSIAppPlusViewConfigTests(unittest.TestCase):
    def test_it(self):
        from venusian import ATTACH_ATTR
        import types
        self.failUnless(getattr(wsgiapptest, ATTACH_ATTR))
        self.failUnless(type(wsgiapptest) is types.FunctionType)
        context = DummyContext()
        request = DummyRequest()
        result = wsgiapptest(context, request)
        self.assertEqual(result, '123')

    def test_scanned(self):
        from pyramid.interfaces import IRequest
        from pyramid.interfaces import IView
        from pyramid.interfaces import IViewClassifier
        from pyramid.configuration import Configurator
        from pyramid.tests import test_integration
        config = Configurator()
        config.scan(test_integration)
        reg = config.registry
        view = reg.adapters.lookup(
            (IViewClassifier, IRequest, INothing), IView, name='')
        self.assertEqual(view, wsgiapptest)

here = os.path.dirname(__file__)
staticapp = static(os.path.join(here, 'fixtures'))

class TestStaticApp(unittest.TestCase):
    def test_it(self):
        from webob import Request
        context = DummyContext()
        from StringIO import StringIO
        request = Request({'PATH_INFO':'',
                           'SCRIPT_NAME':'',
                           'SERVER_NAME':'localhost',
                           'SERVER_PORT':'80',
                           'REQUEST_METHOD':'GET',
                           'wsgi.version':(1,0),
                           'wsgi.url_scheme':'http',
                           'wsgi.input':StringIO()})
        request.subpath = ['minimal.pt']
        result = staticapp(context, request)
        self.assertEqual(result.status, '200 OK')
        self.assertEqual(
            result.body,
            open(os.path.join(here, 'fixtures/minimal.pt'), 'r').read())

class TwillBase(unittest.TestCase):
    root_factory = None
    def setUp(self):
        import sys
        import twill
        from pyramid.configuration import Configurator
        config = Configurator(root_factory=self.root_factory)
        config.load_zcml(self.config)
        twill.add_wsgi_intercept('localhost', 6543, config.make_wsgi_app)
        if sys.platform is 'win32': # pragma: no cover
            out = open('nul:', 'wb')
        else:
            out = open('/dev/null', 'wb')
        twill.set_output(out)
        testing.setUp(registry=config.registry)

    def tearDown(self):
        import twill
        import twill.commands
        twill.commands.reset_browser()
        twill.remove_wsgi_intercept('localhost', 6543)
        twill.set_output(None)
        testing.tearDown()

class TestFixtureApp(TwillBase):
    config = 'pyramid.tests.fixtureapp:configure.zcml'
    def test_it(self):
        import twill.commands
        browser = twill.commands.get_browser()
        browser.go('http://localhost:6543/another.html')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'fixture')
        browser.go('http://localhost:6543')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'fixture')
        browser.go('http://localhost:6543/dummyskin.html')
        self.assertEqual(browser.get_code(), 404)
        browser.go('http://localhost:6543/error.html')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'supressed')
        browser.go('http://localhost:6543/protected.html')
        self.assertEqual(browser.get_code(), 401)

class TestCCBug(TwillBase):
    # "unordered" as reported in IRC by author of
    # http://labs.creativecommons.org/2010/01/13/cc-engine-and-web-non-frameworks/
    config = 'pyramid.tests.ccbugapp:configure.zcml'
    def test_it(self):
        import twill.commands
        browser = twill.commands.get_browser()
        browser.go('http://localhost:6543/licenses/1/v1/rdf')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'rdf')
        browser.go('http://localhost:6543/licenses/1/v1/juri')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'juri')

class TestHybridApp(TwillBase):
    # make sure views registered for a route "win" over views registered
    # without one, even though the context of the non-route view may
    # be more specific than the route view.
    config = 'pyramid.tests.hybridapp:configure.zcml'
    def test_it(self):
        import twill.commands
        browser = twill.commands.get_browser()
        browser.go('http://localhost:6543/')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'global')
        browser.go('http://localhost:6543/abc')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'route')
        browser.go('http://localhost:6543/def')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'route2')
        browser.go('http://localhost:6543/ghi')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'global')
        browser.go('http://localhost:6543/jkl')
        self.assertEqual(browser.get_code(), 404)
        browser.go('http://localhost:6543/mno/global2')
        self.assertEqual(browser.get_code(), 404)
        browser.go('http://localhost:6543/pqr/global2')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'global2')
        browser.go('http://localhost:6543/error')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'supressed')
        browser.go('http://localhost:6543/error2')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'supressed2')
        browser.go('http://localhost:6543/error_sub')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'supressed2')

class TestRestBugApp(TwillBase):
    # test bug reported by delijati 2010/2/3 (http://pastebin.com/d4cc15515)
    config = 'pyramid.tests.restbugapp:configure.zcml'
    def test_it(self):
        import twill.commands
        browser = twill.commands.get_browser()
        browser.go('http://localhost:6543/pet')
        self.assertEqual(browser.get_code(), 200)
        self.assertEqual(browser.get_html(), 'gotten')

class TestViewDecoratorApp(TwillBase):
    config = 'pyramid.tests.viewdecoratorapp:configure.zcml'
    def test_it(self):
        import twill.commands
        browser = twill.commands.get_browser()
        browser.go('http://localhost:6543/first')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('OK' in browser.get_html())

        browser.go('http://localhost:6543/second')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('OK2' in browser.get_html())

        browser.go('http://localhost:6543/third')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('OK3' in browser.get_html())

class TestViewPermissionBug(TwillBase):
    # view_execution_permitted bug as reported by Shane at http://lists.repoze.org/pipermail/repoze-dev/2010-October/003603.html
    config = 'pyramid.tests.permbugapp:configure.zcml'
    def test_it(self):
        import twill.commands
        browser = twill.commands.get_browser()
        browser.go('http://localhost:6543/test')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('ACLDenied' in browser.get_html())
        browser.go('http://localhost:6543/x')
        self.assertEqual(browser.get_code(), 401)

class TestDefaultViewPermissionBug(TwillBase):
    # default_view_permission bug as reported by Wiggy at http://lists.repoze.org/pipermail/repoze-dev/2010-October/003602.html
    config = 'pyramid.tests.defpermbugapp:configure.zcml'
    def test_it(self):
        import twill.commands
        browser = twill.commands.get_browser()
        browser.go('http://localhost:6543/x')
        self.assertEqual(browser.get_code(), 401)
        self.failUnless('failed permission check' in browser.get_html())
        browser.go('http://localhost:6543/y')
        self.assertEqual(browser.get_code(), 401)
        self.failUnless('failed permission check' in browser.get_html())
        browser.go('http://localhost:6543/z')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('public' in browser.get_html())

from pyramid.tests.exceptionviewapp.models import AnException, NotAnException
excroot = {'anexception':AnException(),
           'notanexception':NotAnException()}

class TestExceptionViewsApp(TwillBase):
    config = 'pyramid.tests.exceptionviewapp:configure.zcml'
    root_factory = lambda *arg: excroot
    def test_it(self):
        import twill.commands
        browser = twill.commands.get_browser()
        browser.go('http://localhost:6543/')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('maybe' in browser.get_html())

        browser.go('http://localhost:6543/notanexception')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('no' in browser.get_html())

        browser.go('http://localhost:6543/anexception')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('yes' in browser.get_html())
        
        browser.go('http://localhost:6543/route_raise_exception')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('yes' in browser.get_html())

        browser.go('http://localhost:6543/route_raise_exception2')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('yes' in browser.get_html())

        browser.go('http://localhost:6543/route_raise_exception3')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('whoa' in browser.get_html())

        browser.go('http://localhost:6543/route_raise_exception4')
        self.assertEqual(browser.get_code(), 200)
        self.failUnless('whoa' in browser.get_html())

class DummyContext(object):
    pass

class DummyRequest:
    subpath = ('__init__.py',)
    traversed = None
    environ = {'REQUEST_METHOD':'GET', 'wsgi.version':(1,0)}
    def get_response(self, application):
        return application(None, None)

