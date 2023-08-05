from Products.PloneTestCase.PloneTestCase import PloneTestCase
from zope.testing import doctestunit
from zope.component import testing, getMultiAdapter
from Testing import ZopeTestCase as ztc
from cStringIO import StringIO
import zope.app.publisher.browser
from Products.Five.testbrowser import Browser
from base import PTGTestCase
from zope.publisher.browser import TestRequest


class TestWorkflowActions(PTGTestCase):
    """
    """

    def test_workflow_state_added(self):
        fw = self.pw['folder_workflow']
        
        self.failUnless('new' not in fw.states)
        
        req = TestRequest(form={
            'selected-workflow' : fw.id,
            'state-name' :  'new'
        })
        #view = getMultiAdapter((self.portal, req), name=u'northstar-submit-new-state')
        #view()
        
        #self.failUnless('new' in fw.states)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestWorkflowActions))
    
    return suite