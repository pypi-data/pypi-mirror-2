"""Integration test for SEO Batching traverser
"""
import unittest

from Products.CMFCore.utils import getToolByName

from collective.seobatching.tests.base import TestCase
from collective.seobatching.traversal import SEOBatchingTraverser
from collective.seobatching.config import SHEET_ID, PROP_ID

class TestRequest(dict):
    
    def __init__(self, **kw):
        self.update(kw)

    def set(self, key, value):
        self[key] = value
    
class TestSEOBatchingTraverser(TestCase):
    """Test SEOBatchingView class"""

    def afterSetUp(self):
        self.portal_url = self.portal.absolute_url()
        self.request = TestRequest(URL=self.portal_url)
        self.traverser = SEOBatchingTraverser(self.portal, self.request)
        self.method = self.traverser.publishTraverse
        props = getToolByName(self.portal, 'portal_properties')
        self.sheet = getattr(props, SHEET_ID)

    def _updateProperty(self, value):
        """Helper method to update batch pattern property"""
        self.sheet.manage_changeProperties(**{PROP_ID: value})

    def test_no_properties_tool(self):
        """Case when there is no portal_properties property installed properly
        """
        # delete property
        self.sheet.manage_delProperties(ids=[PROP_ID])
        
        self.assertRaises(KeyError, self.method, self.request, 'batch-10')
        
    def test_valid_pattern(self):
        self.assertEquals(self.portal, self.method(self.request, 'batch-10'))
        self.assertEquals('10', self.request.get('b_start'))
        
    def test_multiple_placeholders(self):
        """Check the case when we have more than one ${num} placeholder in
        batch pattern
        """
        self._updateProperty('${num}-batch-${num}')
        self.assertEquals(self.portal, self.method(self.request, '20-batch-20'))
        self.assertEquals('20', self.request.get('b_start'))

    def test_no_placeholder(self):
        """Check the case when we don't have any ${num} placeholder in batch
        pattern
        """
        self._updateProperty('batch')
        self.assertRaises(KeyError, self.method, self.request, 'batch-10')

    def test_invalid_pattern(self):
        """Set invalid batch pattern in propeties tool and see if traerser
        wont' break
        """
        # make it invalid for regular expression
        self._updateProperty('batch-${num}[')
        self.assertRaises(KeyError, self.method, self.request, 'batch-10')

def test_suite():
    """Collects above tests into test suite."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSEOBatchingTraverser))
    return suite
