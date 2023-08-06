## come on python gimme some of that sweet, sweet -*- coding: utf-8 -*-

import unittest

class Base(object):
    def setUp(self):
        from pyramid.configuration import Configurator
        self.config = Configurator()
        self.config.begin()
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        self.templates_dir = os.path.join(here, 'fixtures')

    def tearDown(self):
        self.config.end()

class Test_renderer_factory(Base, unittest.TestCase):
    def _callFUT(self, info):
        from pyramid.mako_templating import renderer_factory
        return renderer_factory(info)

    def test_no_directories(self):
        from pyramid.exceptions import ConfigurationError
        info = DummyRendererInfo({
            'name':'helloworld.mak',
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            })
        self.assertRaises(ConfigurationError, self._callFUT, info)

    def test_no_lookup(self):
        from pyramid.mako_templating import IMakoLookup
        settings = {'mako.directories':self.templates_dir}
        info = DummyRendererInfo({
            'name':'helloworld.mak',
            'package':None,
            'registry':self.config.registry,
            'settings':settings,
            })
        renderer = self._callFUT(info)
        lookup = self.config.registry.getUtility(IMakoLookup)
        self.assertEqual(lookup.directories, [self.templates_dir])
        self.assertEqual(lookup.filesystem_checks, False)
        self.assertEqual(renderer.path, 'helloworld.mak')
        self.assertEqual(renderer.lookup, lookup)

    def test_composite_directories_path(self):
        from pyramid.mako_templating import IMakoLookup
        twice = self.templates_dir + '\n' + self.templates_dir
        settings = {'mako.directories':twice}
        info = DummyRendererInfo({
            'name':'helloworld.mak',
            'package':None,
            'registry':self.config.registry,
            'settings':settings,
            })
        self._callFUT(info)
        lookup = self.config.registry.getUtility(IMakoLookup)
        self.assertEqual(lookup.directories, [self.templates_dir]*2)

    def test_with_lookup(self):
        from pyramid.mako_templating import IMakoLookup
        lookup = dict()
        self.config.registry.registerUtility(lookup, IMakoLookup)
        info = DummyRendererInfo({
            'name':'helloworld.mak',
            'package':None,
            'registry':self.config.registry,
            'settings':{},
            })
        renderer = self._callFUT(info)
        self.assertEqual(renderer.lookup, lookup)
        self.assertEqual(renderer.path, 'helloworld.mak')

class MakoLookupTemplateRendererTests(Base, unittest.TestCase):
    def _getTargetClass(self):
        from pyramid.mako_templating import MakoLookupTemplateRenderer
        return MakoLookupTemplateRenderer

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def test_instance_implements_ITemplate(self):
        from zope.interface.verify import verifyObject
        from pyramid.interfaces import ITemplateRenderer
        verifyObject(ITemplateRenderer, self._makeOne(None, None))

    def test_class_implements_ITemplate(self):
        from zope.interface.verify import verifyClass
        from pyramid.interfaces import ITemplateRenderer
        verifyClass(ITemplateRenderer, self._getTargetClass())

    def test_call(self):
        lookup = DummyLookup()
        instance = self._makeOne('path', lookup)
        result = instance({}, {'system':1})
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, u'result')

    def test_call_with_system_context(self):
        # lame
        lookup = DummyLookup()
        instance = self._makeOne('path', lookup)
        result = instance({}, {'context':1})
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, u'result')
        self.assertEqual(lookup.values, {'_context':1})

    def test_call_with_tuple_value(self):
        lookup = DummyLookup()
        instance = self._makeOne('path', lookup)
        result = instance(('fub', {}), {'context':1})
        self.assertEqual(lookup.deffed, 'fub')
        self.assertEqual(result, u'result')
        self.assertEqual(lookup.values, {'_context':1})

    def test_call_with_nondict_value(self):
        lookup = DummyLookup()
        instance = self._makeOne('path', lookup)
        self.assertRaises(ValueError, instance, None, {})

    def test_implementation(self):
        lookup = DummyLookup()
        instance = self._makeOne('path', lookup)
        result = instance.implementation().render_unicode()
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, u'result')
        
class TestIntegration(unittest.TestCase):
    def setUp(self):
        import pyramid.mako_templating
        from pyramid.configuration import Configurator
        self.config = Configurator()
        self.config.begin()
        self.config.add_settings({'mako.directories':
                                  'pyramid.tests:fixtures'})
        self.config.add_renderer('.mak',
                                 pyramid.mako_templating.renderer_factory)

    def tearDown(self):
        self.config.end()

    def test_render(self):
        from pyramid.renderers import render
        result = render('helloworld.mak', {'a':1})
        self.assertEqual(result, u'\nHello föö\n')

    def test_render_from_fs(self):
        from pyramid.renderers import render
        self.config.add_settings({'reload_templates': True})
        result = render('helloworld.mak', {'a':1})
        self.assertEqual(result, u'\nHello föö\n')
    
    def test_render_inheritance(self):
        from pyramid.renderers import render
        result = render('helloinherit.mak', {})
        self.assertEqual(result, u'Layout\nHello World!\n')

    def test_render_inheritance_pkg_spec(self):
        from pyramid.renderers import render
        result = render('hello_inherit_pkg.mak', {})
        self.assertEqual(result, u'Layout\nHello World!\n')

    def test_render_to_response(self):
        from pyramid.renderers import render_to_response
        result = render_to_response('helloworld.mak', {'a':1})
        self.assertEqual(result.ubody, u'\nHello föö\n')

    def test_render_to_response_pkg_spec(self):
        from pyramid.renderers import render_to_response
        result = render_to_response('pyramid.tests:fixtures/helloworld.mak', {'a':1})
        self.assertEqual(result.ubody, u'\nHello föö\n')
    
    def test_render_with_abs_path(self):
        from pyramid.renderers import render
        result = render('/helloworld.mak', {'a':1})
        self.assertEqual(result, u'\nHello föö\n')

    def test_get_renderer(self):
        from pyramid.renderers import get_renderer
        result = get_renderer('helloworld.mak')
        self.assertEqual(result.implementation().render_unicode(),
                         u'\nHello föö\n')
    
    def test_template_not_found(self):
        from pyramid.renderers import render
        from mako.exceptions import TemplateLookupException
        self.assertRaises(TemplateLookupException, render,
                          'helloworld_not_here.mak', {})

class TestPkgResourceTemplateLookup(unittest.TestCase):
    def _makeOne(self, **kw):
        from pyramid.mako_templating import PkgResourceTemplateLookup
        return PkgResourceTemplateLookup(**kw)

    def get_fixturedir(self):
        import os
        import pyramid.tests
        return os.path.join(os.path.dirname(pyramid.tests.__file__), 'fixtures')

    def test_adjust_uri_not_resource_spec(self):
        inst = self._makeOne()
        result = inst.adjust_uri('a', None)
        self.assertEqual(result, '/a')

    def test_adjust_uri_resource_spec(self):
        inst = self._makeOne()
        result = inst.adjust_uri('a:b', None)
        self.assertEqual(result, 'a:b')

    def test_get_template_not_resource_spec(self):
        fixturedir = self.get_fixturedir()
        inst = self._makeOne(directories=[fixturedir])
        result = inst.get_template('helloworld.mak')
        self.failIf(result is None)
        
    def test_get_template_resource_spec_with_filesystem_checks(self):
        inst = self._makeOne(filesystem_checks=True)
        result = inst.get_template('pyramid.tests:fixtures/helloworld.mak')
        self.failIf(result is None)

    def test_get_template_resource_spec_missing(self):
        from mako.exceptions import TopLevelLookupException
        fixturedir = self.get_fixturedir()
        inst = self._makeOne(filesystem_checks=True, directories=[fixturedir])
        self.assertRaises(TopLevelLookupException, inst.get_template,
                          'pyramid.tests:fixtures/notthere.mak')

class DummyLookup(object):
    def get_template(self, path):
        self.path = path
        return self

    def get_def(self, path):
        self.deffed = path
        return self

    def render_unicode(self, **values):
        self.values = values
        return u'result'
        
class DummyRendererInfo(object):
    def __init__(self, kw):
        self.__dict__.update(kw)
        
