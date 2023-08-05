from Products.PloneTestCase.PloneTestCase import PloneTestCase
from zope.testing import doctestunit
from zope.component import testing, getMultiAdapter
from Testing import ZopeTestCase as ztc
from cStringIO import StringIO
import zope.app.publisher.browser
from Products.Five.testbrowser import Browser
from base import NorthStarTestCase
from zope.publisher.browser import TestRequest
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import alsoProvides

class TestWorkflowActions(NorthStarTestCase):
    """
    """

    def setUp(self):
        self.portal = self.layer.portal
        self.pw = self.portal.portal_workflow

    def test_workflow_state_added(self):
        pass
        #fw = self.pw['folder_workflow']
        
        #self.failUnless('new' not in fw.states)
        
        #req = TestRequest(form={
        #    'selected-workflow' : fw.id,
        #    'state-name' :  'new'
        #})
        #alsoProvides(req, IAttributeAnnotatable)
        #view = getMultiAdapter((self.portal, req), name=u'northstar-submit-new-state')
        #view()
        
        #self.failUnless('new' in fw.states)




def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowActions))
    
    return suite