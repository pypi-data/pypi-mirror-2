## -*- coding: utf-8 -*-

import unittest

class Base(object):
    def setUp(self):
        from repoze.bfg.configuration import Configurator
        self.config = Configurator()
        self.config.begin()
        import os
        here = os.path.abspath(os.path.dirname(__file__))
        self.templates_dir = os.path.join(here, 'templates')

    def tearDown(self):
        self.config.end()

    def _registerUtility(self, utility, iface, name=''):
        from zope.component import getSiteManager
        sm = getSiteManager()
        sm.registerUtility(utility, iface, name=name)
        return sm

class Test_renderer_factory(Base, unittest.TestCase):
    def _callFUT(self, path):
        from repoze.bfg.mako import renderer_factory
        return renderer_factory(path)

    def test_no_directories(self):
        from repoze.bfg.exceptions import ConfigurationError
        self.assertRaises(ConfigurationError, self._callFUT, 'path')

    def test_no_lookup(self):
        from repoze.bfg.mako import IMakoLookup
        self.config.add_settings({'mako.directories':self.templates_dir})
        renderer = self._callFUT('helloworld.mak')
        lookup = self.config.registry.getUtility(IMakoLookup)
        self.assertEqual(lookup.directories, [self.templates_dir])
        self.assertEqual(lookup.filesystem_checks, False)
        self.assertEqual(renderer.path, 'helloworld.mak')
        self.assertEqual(renderer.lookup, lookup)

    def test_composite_directories_path(self):
        from repoze.bfg.mako import IMakoLookup
        twice = self.templates_dir + '\n' + self.templates_dir
        self.config.add_settings({'mako.directories':twice})
        self._callFUT('helloworld.mak')
        lookup = self.config.registry.getUtility(IMakoLookup)
        self.assertEqual(lookup.directories, [self.templates_dir]*2)

    def test_with_lookup(self):
        from repoze.bfg.mako import IMakoLookup
        lookup = dict()
        self.config.registry.registerUtility(lookup, IMakoLookup)
        renderer = self._callFUT('helloworld.mak')
        self.assertEqual(renderer.lookup, lookup)
        self.assertEqual(renderer.path, 'helloworld.mak')

class MakoLookupTemplateRendererTests(Base, unittest.TestCase):
    def _getTargetClass(self):
        from repoze.bfg.mako import MakoLookupTemplateRenderer
        return MakoLookupTemplateRenderer

    def _makeOne(self, *arg, **kw):
        klass = self._getTargetClass()
        return klass(*arg, **kw)

    def test_instance_implements_ITemplate(self):
        from zope.interface.verify import verifyObject
        from repoze.bfg.interfaces import ITemplateRenderer
        verifyObject(ITemplateRenderer, self._makeOne(None, None))

    def test_class_implements_ITemplate(self):
        from zope.interface.verify import verifyClass
        from repoze.bfg.interfaces import ITemplateRenderer
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
        
class Test_render_template(Base, unittest.TestCase):
    def _callFUT(self, name, **kw):
        from repoze.bfg.mako import render_template
        return render_template(name, **kw)

    def test_it(self):
        self.config.add_settings({'mako.directories':self.templates_dir})
        result = self._callFUT('helloworld.mak')
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, u'\nHello föö\n')

class Test_render_template_to_response(Base, unittest.TestCase):
    def _callFUT(self, name, **kw):
        from repoze.bfg.mako import render_template_to_response
        return render_template_to_response(name, **kw)

    def test_it(self):
        self.config.add_settings({'mako.directories':self.templates_dir})
        result = self._callFUT('helloworld.mak')
        from webob import Response
        self.failUnless(isinstance(result, Response))
        self.assertEqual(result.app_iter, [u'\nHello föö\n'.encode('utf-8')])
        self.assertEqual(result.status, '200 OK')
        self.assertEqual(len(result.headerlist), 2)

    def test_iresponsefactory_override(self):
        self.config.add_settings({'mako.directories':self.templates_dir})
        from webob import Response
        class Response2(Response):
            pass
        from repoze.bfg.interfaces import IResponseFactory
        self._registerUtility(Response2, IResponseFactory)
        result = self._callFUT('helloworld.mak')
        self.failUnless(isinstance(result, Response2))

class Test_get_renderer(Test_renderer_factory, unittest.TestCase):
    def _callFUT(self, name):
        from repoze.bfg.mako import get_renderer
        return get_renderer(name)

class Test_get_template(Base, unittest.TestCase):
    def _callFUT(self, name):
        from repoze.bfg.mako import get_template
        return get_template(name)

    def test_it(self):
        self.config.add_settings({'mako.directories':self.templates_dir})
        impl = self._callFUT('helloworld.mak')
        result = impl.render_unicode()
        self.failUnless(isinstance(result, unicode))
        self.assertEqual(result, u'\nHello föö\n')

class Test_resolve_resource_spec(unittest.TestCase):
    def _callFUT(self, spec, package_name='__main__'):
        from repoze.bfg.mako import resolve_resource_spec
        return resolve_resource_spec(spec, package_name)

    def test_abspath(self):
        import os
        here = os.path.dirname(__file__)
        path = os.path.abspath(here)
        package_name, filename = self._callFUT(path, 'apackage')
        self.assertEqual(filename, path)
        self.assertEqual(package_name, None)

    def test_rel_spec(self):
        pkg = 'repoze.bfg.mako.tests'
        path = 'test_resource.py'
        package_name, filename = self._callFUT(path, pkg)
        self.assertEqual(package_name, 'repoze.bfg.mako.tests')
        self.assertEqual(filename, 'test_resource.py')
        
    def test_abs_spec(self):
        pkg = 'repoze.bfg.mako.tests'
        path = 'repoze.bfg.mako.nottests:test_resource.py'
        package_name, filename = self._callFUT(path, pkg)
        self.assertEqual(package_name, 'repoze.bfg.mako.nottests')
        self.assertEqual(filename, 'test_resource.py')

    def test_package_name_is_None(self):
        pkg = None
        path = 'test_resource.py'
        package_name, filename = self._callFUT(path, pkg)
        self.assertEqual(package_name, None)
        self.assertEqual(filename, 'test_resource.py')
        
class Test_abspath_from_resource_spec(unittest.TestCase):
    def _callFUT(self, spec, pname='__main__'):
        from repoze.bfg.mako import abspath_from_resource_spec
        return abspath_from_resource_spec(spec, pname)

    def test_pname_is_None_before_resolve_resource_spec(self):
        result = self._callFUT('abc', None)
        self.assertEqual(result, 'abc')

    def test_pname_is_None_after_resolve_resource_spec(self):
        result = self._callFUT('/abc', '__main__')
        self.assertEqual(result, '/abc')

    def test_pkgrelative(self):
        import os
        here = os.path.dirname(__file__)
        path = os.path.abspath(here)
        result = self._callFUT('abc', 'repoze.bfg.mako.tests')
        self.assertEqual(result, os.path.join(path, 'abc'))


class DummyLookup(object):
    def get_template(self, path):
        self.path = path
        return self

    def render_unicode(self, **values):
        self.values = values
        return u'result'
        
