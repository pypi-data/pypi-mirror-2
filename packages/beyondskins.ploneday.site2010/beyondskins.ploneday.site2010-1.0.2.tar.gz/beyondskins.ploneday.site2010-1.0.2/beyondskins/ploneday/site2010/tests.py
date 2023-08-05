# -*- coding: utf-8 -*-
import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup
ptc.setupPloneSite()

import beyondskins.ploneday.site2010

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', beyondskins.ploneday.site2010)
    fiveconfigure.debug_mode = False

setup_product()
ptc.setupPloneSite(products=['beyondskins.ploneday.site2010'],
                   extension_profiles=['beyondskins.ploneday.site2010:default',])

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             beyondskins.ploneday.site2010)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='beyondskins.ploneday.site2010',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='beyondskins.ploneday.site2010.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='beyondskins.ploneday.site2010.doc',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'browser.txt', package='beyondskins.ploneday.site2010.doc',
            test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
