"""This is plone integration test checking if collective.seobatching package is
installed propertly.
"""
import unittest

from Products.CMFCore.utils import getToolByName

from collective.seobatching.tests.base import TestCase
from collective.seobatching.config import SHEET_ID, PROP_ID

class TestSetup(TestCase):
    """Test seo batching installation procedure"""

    def test_properties_tool(self):
        """Check if properties tool has all required info setup"""
        props = getToolByName(self.portal, 'portal_properties')
        self.failUnless(SHEET_ID in props.objectIds())
        self.assertEquals('batch-${num}',
                          getattr(props, SHEET_ID).getProperty(PROP_ID, None))
    
    def test_skins_tool(self):
        """Check if seo batching layer is inside skins tool"""
        skins = getToolByName(self.portal, 'portal_skins')
        # check skins layer
        self.failUnless('collective_seobatching' in skins.objectIds())
        
        # check if layer is added to skins selection
        for k, v in skins.getSkinPaths():
            layers = [l.strip() for l in v.split(',')]
            self.failUnless('collective_seobatching' in layers)

def test_suite():
    """Collects all above tests into suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
