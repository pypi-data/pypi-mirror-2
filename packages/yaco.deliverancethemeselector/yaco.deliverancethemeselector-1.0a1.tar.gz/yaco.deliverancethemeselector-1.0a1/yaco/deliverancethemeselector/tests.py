# -*- coding: utf-8 -*-

import unittest

#from zope.testing import doctestunit
#from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """Set up the package and its dependencies."""

    fiveconfigure.debug_mode = True
    import yaco.deliverancethemeselector
    zcml.load_config('configure.zcml', yaco.deliverancethemeselector)
    fiveconfigure.debug_mode = False

setup_product()
ptc.setupPloneSite(products=['yaco.deliverancethemeselector'])

def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='yaco.deliverancethemeselector',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='yaco.deliverancethemeselector.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'README.txt', package='yaco.deliverancethemeselector',
            test_class=ptc.FunctionalTestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='yaco.deliverancethemeselector',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
