from Products.PloneTestCase.PloneTestCase import PloneTestCase
from zope.testing import doctestunit
from zope.component import testing, getMultiAdapter
from Testing import ZopeTestCase as ztc
from cStringIO import StringIO
import zope.app.publisher.browser
from Products.Five.testbrowser import Browser
from base import PTGTestCase
from zope.publisher.browser import TestRequest
from uwosh.northstar.utils import *
from uwosh.northstar.browser.controlpanel import UWOshProjectNorthStarActions


class TestUtils(PTGTestCase):
    """
    """
    
    pass
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUtils))
    
    return suite