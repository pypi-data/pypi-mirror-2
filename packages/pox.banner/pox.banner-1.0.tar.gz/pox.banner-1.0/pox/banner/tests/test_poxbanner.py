import sys
from IPython.Shell import IPShellEmbed

import unittest

#from zope.testing import doctestunit
#rom zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite, onsetup

import pox.banner

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', pox.banner)
    fiveconfigure.debug_mode = False
    ztc.installPackage('pox.banner')

setup_product()
ptc.setupPloneSite(products=['pox.banner',])

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             pox.banner)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def ipython(self, locals=None): 
        """Provides an interactive shell aka console inside your testcase. 
        Uses ipython for on steroids shell... 
    
        It looks exact like in a doctestcase and you can copy and paste 
        code from the shell into your doctest. The locals in the testcase are 
        available, becasue you are in the testcase. 
    
        In your testcase or doctest you can invoke the shell at any point by 
        calling:: 
    
            >>> self.ipython( locals() ) 
    
        locals -- passed to InteractiveInterpreter.__init__() 
        """ 
        savestdout = sys.stdout 
        sys.stdout = sys.stderr 
        sys.stderr.write('='*70) 
        embedshell = IPShellEmbed(argv=[], 
                                  banner=""" 
IPython Interactive Console
    
Note: You have the same locals available as in your test-case.
""", 
                                  exit_msg="""end of ZopeTestCase Interactive Console session""", 
                                  user_ns=locals) 
        embedshell() 
        sys.stdout.write('='*70+'\n') 
        sys.stdout = savestdout 


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='pox.banner',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='pox.banner.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'README.txt', package='pox.banner',
            test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'browser.txt', package='pox.banner',
            test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
