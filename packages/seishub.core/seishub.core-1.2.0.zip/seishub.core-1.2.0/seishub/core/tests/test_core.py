# -*- coding: utf-8 -*-
#
"""Core test suite mainly adopted from Trac."""


# Copyright (C) 2005 Edgewall Software
# Copyright (C) 2005 Christopher Lenz <cmlenz@gmx.de>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://trac.edgewall.org/log/.
#
# Author: Christopher Lenz <cmlenz@gmx.de>

from seishub.core.exceptions import SeisHubError
from seishub.core.core import Interface, Component, implements

import unittest


class ITest(Interface):
    def test(self):
        """Dummy function."""


class ComponentTestCase(unittest.TestCase):

    def setUp(self):
        from seishub.core.core import ComponentManager, ComponentMeta
        self.compmgr = ComponentManager()

        # Make sure we have no external components hanging around in the
        # component registry
        self.old_registry = ComponentMeta._registry
        ComponentMeta._registry = {}

    def tearDown(self):
        # Restore the original component registry
        from seishub.core.core import ComponentMeta
        ComponentMeta._registry = self.old_registry

    def test_base_class_not_registered(self):
        """
        Make sure that the Component base class does not appear in the component
        registry.
        """
        from seishub.core.core import ComponentMeta
        assert Component not in ComponentMeta._components
        self.assertRaises(SeisHubError, self.compmgr.__getitem__, Component)

    def test_abstract_component_not_registered(self):
        """
        Make sure that a Component class marked as abstract does not appear in
        the component registry.
        """
        from seishub.core.core import ComponentMeta
        class AbstractComponent(Component):
            abstract = True
        assert AbstractComponent not in ComponentMeta._components
        self.assertRaises(SeisHubError, self.compmgr.__getitem__,
                          AbstractComponent)

    def test_unregistered_component(self):
        """
        Make sure the component manager refuses to manage classes not derived
        from `Component`.
        """
        class NoComponent(object): pass
        self.assertRaises(SeisHubError, self.compmgr.__getitem__, NoComponent)

    def test_component_registration(self):
        """
        Verify that classes derived from `Component` are managed by the
        component manager.
        """
        class ComponentA(Component):
            pass
        assert self.compmgr[ComponentA]
        assert ComponentA(self.compmgr)

    def test_component_identity(self):
        """
        Make sure instantiating a component multiple times just returns the
        same instance again.
        """
        class ComponentA(Component):
            pass
        c1 = ComponentA(self.compmgr)
        c2 = ComponentA(self.compmgr)
        assert c1 is c2, 'Expected same component instance'
        c2 = self.compmgr[ComponentA]
        assert c1 is c2, 'Expected same component instance'

    def test_component_initializer(self):
        """
        Makes sure that a components' `__init__` method gets called.
        """
        class ComponentA(Component):
            def __init__(self):
                self.data = 'test'
        self.assertEqual('test', ComponentA(self.compmgr).data)
        ComponentA(self.compmgr).data = 'newtest'
        self.assertEqual('newtest', ComponentA(self.compmgr).data)

    def test_inherited_component_initializer(self):
        """
        Makes sure that a the `__init__` method of a components' super-class
        gets called if the component doesn't override it.
        """
        class ComponentA(Component):
            def __init__(self):
                self.data = 'foo'
        class ComponentB(ComponentA):
            def __init__(self):
                self.data = 'bar'
        class ComponentC(ComponentB):
            pass
        self.assertEqual('bar', ComponentC(self.compmgr).data)
        ComponentC(self.compmgr).data = 'baz'
        self.assertEqual('baz', ComponentC(self.compmgr).data)

    def test_implements_called_outside_classdef(self):
        """
        Verify that calling implements() outside a class definition raises an
        `AssertionError`.
        """
        try:
            implements()
            self.fail('Expected AssertionError')
        except AssertionError:
            pass

    def test_implements_called_twice(self):
        """
        Verify that calling implements() twice in a class definition raises an
        `AssertionError`.
        """
        try:
            class ComponentA(Component):
                implements()
                implements()
            self.fail('Expected AssertionError')
        except TypeError:
            # Zope Interfaces
            pass
        except AssertionError:
            # SeisHub Interfaces
            pass

    def test_attribute_access(self):
        """
        Verify that accessing undefined attributes on components raises an
        `AttributeError`.
        """
        class ComponentA(Component):
            pass
        comp = ComponentA(self.compmgr)
        try:
            comp.foo
            self.fail('Expected AttributeError')
        except AttributeError:
            pass

    def test_inherited_implements(self):
        """
        Verify that a component with a super-class implementing an extension
        point interface is also registered as implementing that interface.
        """
        class BaseComponent(Component):
            implements(ITest)
            abstract = True
        class ConcreteComponent(BaseComponent):
            pass
        from seishub.core.core import ComponentMeta
        assert ConcreteComponent in ComponentMeta._registry[ITest]

    def test_instantiation_doesnt_enable(self):
        """
        Make sure that a component disabled by the ComponentManager is not
        implicitly enabled by instantiating it directly.
        """
        from seishub.core.core import ComponentManager
        class DisablingComponentManager(ComponentManager):
            def isComponentEnabled(self, cls):
                return False
        class ComponentA(Component):
            pass
        mgr = DisablingComponentManager()
        ComponentA(mgr)
        self.assertEqual(None, mgr[ComponentA])


def suite():
    return unittest.makeSuite(ComponentTestCase, 'test')


if __name__ == '__main__':
    unittest.main()
