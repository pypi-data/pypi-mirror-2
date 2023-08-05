#
# Unit Tests for component/core
#

import os
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__)))+os.sep+".."+os.sep+"..")
currdir = dirname(abspath(__file__))+os.sep

import re
from nose.tools import nottest
import pyutilib.th as unittest
from pyutilib.component.core import *
import pyutilib.misc

PluginGlobals.push_env(PluginEnvironment("testing"))

class IDebug1(Interface):
    """An example interface"""

class IDebug2(Interface):
    """An example interface"""

class IDebug3(Interface):
    """An example interface"""

class IDebug4(Interface):
    """An example interface that provides default implementations of the api"""

    def __init__(self):
        self.x=0

    def f1(self):
        self.x=1

    def f2(self):
        self.x=2


class Plugin1(Plugin):
    implements(IDebug1)

class Plugin2(Plugin):
    implements(IDebug1)

class Plugin3(Plugin):
    implements(IDebug2)

class Plugin4(Plugin):
    implements(IDebug1)
    implements(IDebug2)

class Plugin5(Plugin):
    implements(IDebug3)

class Plugin6(Plugin,PluginEnvironment):
    implements(IDebug3)

    def __init__(self, **kwds):
        Plugin.__init__(self,**kwds)
        PluginEnvironment.__init__(self,**kwds)

class Plugin7(Plugin):
    implements(IDebug1)

    def enabled(self):
        return self.id % 2 == 0

class Plugin8(Plugin5):
    implements(IDebug2)

class Plugin9(Plugin5):
    implements(IDebug3)

class Service1(PluginEnvironment):

    def is_service_enabled(self, cls):
        return False

class Plugin10(Plugin):
    implements(IDebug1, "tmpenv")

class Plugin11a(Plugin):
    implements(IDebug4)

    def __init__(self):
        self.x=4

    def f1(self):
        self.x=5

class Plugin11b(Plugin):
    implements(IDebug4, inherit=True)

    def __init__(self):
        #IDebug4.__init__(self)
        self.x=0

PluginGlobals.pop_env()


class TestExtensionPoint(unittest.TestCase):

    def setUp(self):
        PluginGlobals.clear()
        PluginGlobals.push_env(PluginEnvironment("testing"))

    def tearDown(self):
        PluginGlobals.pop_env()

    def test_interface_decl(self):
        try:
            class IDebug1(Interface):
                pass
            self.fail("expected failure")
        except PluginError:
            pass
    
    def test_ep_init(self):
        """Test ExtensionPoint construction"""
        ep = ExtensionPoint(IDebug1)
        self.failUnlessEqual(IDebug1,ep.interface)
        try:
            ExtensionPoint()
            self.fail("error expected")
        except PluginError:
            pass

    def test_ep_string(self):
        """Test ExtensionPoint registration"""
        ep = ExtensionPoint(IDebug1)
        self.failUnlessEqual(str(ep),"<ExtensionPoint IDebug1 env=testing>")
        self.failUnlessEqual(len(ep.extensions()),0)
        s0 = Plugin1()
        self.failUnlessEqual(len(ep.extensions()),1)
        s1 = Plugin1()
        self.failUnlessEqual(len(ep.extensions()),2)

    def test_ep_registration(self):
        """Test ExtensionPoint registration"""
        ep = ExtensionPoint(IDebug1)
        self.failUnlessEqual(ep.extensions(),set())
        s1 = Plugin1()
        s2 = Plugin2()
        s3 = Plugin3()
        s4 = Plugin4()
        s5 = Plugin5()
        self.failUnlessEqual(PluginGlobals.services(),set([s1,s2,s3,s4,s5]))
        self.failUnlessEqual(set(ep.extensions()),set([s1,s2,s4]))
        self.failUnlessEqual(set(ep.extensions()),set([s1,s2,s4]))

    def test_ep_call(self):
        """Test ExtensionPoint __call__"""
        ep = ExtensionPoint(IDebug1)
        s1 = Plugin1(name="p1")
        s2 = Plugin2(name="p2")
        s3 = Plugin4(name="p3")
        s4 = Plugin4(name="p3")
        s5 = Plugin3(name="p4")
        self.failUnlessEqual(set(ep()),set([s1,s2,s3,s4]))
        try:
            ep(0)
            self.fail("expected failure")
        except PluginError:
            pass
        self.failUnlessEqual(ep("p1"),set([s1]))
        self.failUnlessEqual(ep("p3"),set([s3,s4]))

    def test_ep_service(self):
        """Test ExtensionPoint service()"""
        ep = ExtensionPoint(IDebug1)
        s1 = Plugin1()
        s2 = Plugin2()
        s3 = Plugin3()
        s4 = Plugin4()
        try:
            ep.service()
            self.fail("expected failure")
        except PluginError:
            pass

    def test_ep_namespace1(self):
        """Test the semantics of the use of namespaces in interface decl"""
        env=PluginEnvironment("tmpenv")
        s1=Plugin10()
        s2=Plugin1()
        self.failUnlessEqual( ExtensionPoint(IDebug1).extensions(), set([s2,s1]))
        self.failUnlessEqual( ExtensionPoint(IDebug1,env).extensions(), set([s1,s2]))

class TestPlugin(unittest.TestCase):

    def setUp(self):
        PluginGlobals.clear()
        PluginGlobals.push_env(PluginEnvironment("testing"))

    def tearDown(self):
        PluginGlobals.pop_env()

    def test_init1(self):
        """Test the behavior of a plugin that is a service manager"""
        s1 = Plugin6()
        self.failUnlessEqual(isinstance(s1,PluginEnvironment),True)
        self.failUnlessEqual(isinstance(s1,Plugin),True)
        self.failUnlessEqual(set(s1.__interfaces__.keys()),set([IDebug3]))

    #def test_init2(self):
        #"""Test that a plugin sets up the registry appropriately"""
        #s1 = Plugin4()
        #s2 = Plugin5()
        #self.failUnlessEqual(s1 in PluginGlobals.interface_registry[IDebug1], True)
        #self.failUnlessEqual(s1 in PluginGlobals.interface_registry[IDebug2], True)
        #self.failUnlessEqual(not s1 in PluginGlobals.extension_points(IDebug3), True)

    def test_init4(self):
        """Verify that base classes are also captured"""
        s1 = Plugin8()
        self.failUnlessEqual(set(s1.__interfaces__.keys()),set([IDebug3,IDebug2]))
        s1 = Plugin9()
        self.failUnlessEqual(set(s1.__interfaces__.keys()),set([IDebug3]))
        
    def test_init5(self):
        PluginEnvironment("test")
        try:
            PluginEnvironment("test")
            self.fail("expected error")
        except PluginError:
            pass

    def test_repr(self):
        """Test the string representation generated"""
        s1 = Plugin1()
        s2 = Plugin2()
        s3 = Plugin3()
        s4 = Plugin1()
        s5 = Plugin3()
        self.failUnlessEqual(str(s1),"<Plugin Plugin1 'Plugin.1'>")
        self.failUnlessEqual(str(s2),"<Plugin Plugin2 'Plugin.2'>")
        self.failUnlessEqual(str(s3),"<Plugin Plugin3 'Plugin.3'>")
        self.failUnlessEqual(str(s4),"<Plugin Plugin1 'Plugin.4'>")
        self.failUnlessEqual(str(s5),"<Plugin Plugin3 'Plugin.5'>")

    def test_enabled(self):
        """Test control of enabled()"""
        ep = ExtensionPoint(IDebug1)
        self.failUnlessEqual(ep.extensions(),set())
        s1 = Plugin1()
        s2 = Plugin2()
        s3 = Plugin3()
        s4 = Plugin4()
        s5 = Plugin5()
        s7a = Plugin7()
        s7b = Plugin7()
        s7c = Plugin7()
        s7d = Plugin7()
        s7e = Plugin7()
        #
        # Only s7b, and s7d will be returned from the exensions() calls
        #
        #PluginGlobals.pprint()
        self.failUnlessEqual(PluginGlobals.services(),set([s1,s2,s3,s4,s5,s7a,s7b,s7c,s7d,s7e]))
        self.failUnlessEqual(set(ep.extensions()),set([s1,s2,s4,s7a,s7c,s7e]))

    def test_implements1(self):
        p1 = Plugin11a()
        self.failUnlessEqual(p1.x,4)
        p1.f1()
        self.failUnlessEqual(p1.x,5)
        try:
            p1.f2()
            self.fail("Expected AttributeError")
        except AttributeError:
            pass

    def test_implements2(self):
        p1 = Plugin11b()
        self.failUnlessEqual(p1.x,0)
        p1.f1()
        self.failUnlessEqual(p1.x,1)
        p1.f2()
        self.failUnlessEqual(p1.x,2)


class TestMisc(unittest.TestCase):

    def setUp(self):
        PluginGlobals.clear()
        PluginGlobals.push_env(PluginEnvironment("testing"))

    def tearDown(self):
        PluginGlobals.pop_env()

    def test_pprint(self):
        """Test the string representation generated"""
        class Plugin100(SingletonPlugin):
            implements(IDebug3)

        spx = Plugin100()
        PluginGlobals.push_env(PluginEnvironment("foo"))
        s1 = Plugin1()
        s2 = Plugin2()
        s3 = Plugin3()
        PluginGlobals.push_env(PluginEnvironment())
        s4 = Plugin1()
        s5 = Plugin3()
        s6 = Plugin11b()
        sp0 = Plugin100()
        self.failIf(re.match("<Plugin Plugin1",str(s1)) is None)
        self.failIf(re.match("<Plugin Plugin2",str(s2)) is None)
        self.failIf(re.match("<Plugin Plugin3",str(s3)) is None)
        self.failIf(re.match("<Plugin Plugin1",str(s4)) is None)
        self.failIf(re.match("<Plugin Plugin3",str(s5)) is None)
        pyutilib.misc.setup_redirect(currdir+"log1.out")
        PluginGlobals.pprint(plugins=False)
        pyutilib.misc.reset_redirect()
        self.failUnlessFileEqualsBaseline(currdir+"log1.out",currdir+"log1.txt")


class TestManager(unittest.TestCase):

    def setUp(self):
        PluginGlobals.clear()
        PluginGlobals.push_env(PluginEnvironment("testing"))

    def tearDown(self):
        PluginGlobals.pop_env()

    def test_init(self):
        """Test the behavior of a plugin that is a service manager"""
        s0 = Plugin1()
        self.failUnlessEqual(PluginGlobals.services(), set([s0]))
        env = PluginEnvironment()
        PluginGlobals.push_env(env)
        s1 = Plugin6()
        self.failUnless(s1 in PluginGlobals.env("testing"))
        #self.failUnlessEqual(s1.services, set([]))
        self.failUnlessEqual(PluginGlobals.services("testing"), set([s0,s1]))
        PluginGlobals.pop_env()
        s2 = Plugin6()
        self.failUnless(s2 in PluginGlobals.env())
        self.failUnlessEqual(env.services, set([]))
        self.failUnlessEqual(PluginGlobals.services("testing"), set([s0,s1,s2]))

    def test_get(self):
        env = PluginEnvironment()
        PluginGlobals.push_env(env)
        s0 = Plugin1()
        self.failIfEqual(env.active_services(IDebug1),[s0])
        self.failUnlessEqual(PluginGlobals.env("testing").active_services(IDebug1),[s0])
        try:
            env.active_services(s0)
            self.fail("Expected failure")
        except PluginError:
            pass
        PluginGlobals.pop_env()

    def test_get3(self):
        try:
            PluginGlobals.env("__unknown__")
            self.fail("expected error")
        except PluginError:
            pass

    def test_pop1(self):
        """Test that popping the environment doesn't remove the last env"""
        PluginGlobals.pop_env()
        PluginGlobals.pop_env()
        PluginGlobals.pop_env()
        self.failUnlessEqual(len(PluginGlobals.env_stack),1)
        
    def test_pop2(self):
        try:
            PluginGlobals.push_env("__unknown__", validate=True)
            self.fail("expected error")
        except PluginError:
            pass
        #
        # No error, because this environment is automatically created
        #
        PluginGlobals.push_env("__unknown__")
        self.failUnlessEqual(PluginGlobals.env().name,"__unknown__")

    def test_factory(self):
        PluginFactory("Plugin6",name="p6")
        PluginFactory("Plugin5",name="p5")
        PluginFactory("Plugin6")
        try:
            PluginFactory("__foo__")
            self.fail("expected error")
        except PluginError:
            pass
        pyutilib.misc.setup_redirect(currdir+"factory.out")
        PluginGlobals.pprint(plugins=False)
        #PluginGlobals.pprint()
        pyutilib.misc.reset_redirect()
        self.failUnlessFileEqualsBaseline(currdir+"factory.out",currdir+"factory.txt")


if __name__ == "__main__":
   unittest.main()
