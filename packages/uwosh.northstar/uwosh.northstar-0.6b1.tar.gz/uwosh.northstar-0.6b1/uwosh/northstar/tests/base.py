import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

from zope.app import zapi
from zope.configuration import xmlconfig

from cStringIO import StringIO

import sys

ztc.installProduct('uwosh.northstar')
ptc.setupPloneSite(products=('uwosh.northstar',))

class PTGTestCase(ptc.PloneTestCase):
    """
    """
    
    def afterSetUp(self):
        self.setRoles(('Manager',))
        
        self.pw = self.portal.portal_workflow
    
