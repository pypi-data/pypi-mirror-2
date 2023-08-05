from Products.PloneTestCase.PloneTestCase import PloneTestCase
from zope.testing import doctestunit
from zope.component import testing, getMultiAdapter
from Testing import ZopeTestCase as ztc
from cStringIO import StringIO
import zope.app.publisher.browser
from Products.Five.testbrowser import Browser
from base import PTGTestCase
from zope.publisher.browser import TestRequest
from uwosh.northstar.actions import MailerAction


class FakeScript(object):
    
    def body(self):
        return \
"""# /*---- VARIABLE DEFINITION ----*\\ _to
someone@gmail.com
# /*---- END VARIABLE DEFINITION ----*\\
# /*---- VARIABLE DEFINITION ----*\\ _from
# someoneelse@gmail.com
# /*---- END VARIABLE DEFINITION ----*\\
# /*---- VARIABLE DEFINITION ----*\\ subject
# Something interesting
# /*---- END VARIABLE DEFINITION ----*\\
# /*---- VARIABLE DEFINITION ----*\\ body
# Some information
# about something
# else...
# /*---- END VARIABLE DEFINITION ----*\\

# now the actual script
from Products.CMFCore.utils import getToolByName

"""

    @property
    def io_body(self):
        return StringIO(self.body())
    
    def read(self):
        return self.io_body.read()
        
    def write(self, value):
        b = StringIO(self.body())
        b.write(value)
        self.body = b.read()


class TestActions(PTGTestCase):
    """
    """

    def test_mailer_action_parses_to(self):
        script = FakeScript()
        action = MailerAction(script)
        self.assertEqual(action._to, 'someone@gmail.com')
        
    def test_mailer_action_parses_from(self):
        script = FakeScript()
        action = MailerAction(script)
        self.assertEqual(action._from, 'someoneelse@gmail.com')        
        
    def test_mailer_action_parses_subject(self):
        script = FakeScript()
        action = MailerAction(script)
        self.assertEqual(action.subject, 'Something interesting')
        
    def test_mailer_action_parses_body(self):
        script = FakeScript()
        action = MailerAction(script)
        self.assertTrue("Some information" in action.body)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestActions))
    
    return suite