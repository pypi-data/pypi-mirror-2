"""Integration test for seobatching_view
"""
import unittest

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

from collective.seobatching.tests.base import TestCase
from collective.seobatching.config import SHEET_ID, PROP_ID


class TestSEOBatchingView(TestCase):
    """Test SEOBatchingView class"""

    def afterSetUp(self):
        self.view = self.portal.restrictedTraverse('@@seobatching_view')
        props = getToolByName(self.portal, 'portal_properties')
        self.sheet = getattr(props, SHEET_ID)
        self.batch = Batch(range(35), 10)
        self.portal_url = self.portal.absolute_url()

    def test_no_properties_tool(self):
        """Test the case when we haven't found proper info in properties_tool"""
        # backup property and delete afterwards
        backup = self.sheet.getProperty(PROP_ID)
        self.sheet.manage_delProperties(ids=[PROP_ID])
        
        self.assertEquals(self.portal_url,
                          self.view.pageurl(self.batch, b_start=10))
                          
        # restore property
        self.sheet.manage_addProperty(PROP_ID, backup, 'string')

    def test_pageurl(self):
        method = self.view.pageurl
        self.assertEquals(self.portal_url, method(self.batch))
        self.assertEquals('page2/batch-10',
                          method(self.batch, url='page2', b_start=10))
        self.assertEquals('%s/batch-20' % self.portal_url,
                          method(self.batch, pagenumber=3))

    def test_navurls(self):
        method = self.view.navurls
        self.assertEquals([
            (1, self.portal_url),
            (2, '%s/batch-10' % self.portal_url),
            (3, '%s/batch-20' % self.portal_url),
            (4, '%s/batch-30' % self.portal_url)], method(self.batch))
        self.assertEquals([(1, 'page1'), (2, 'page1/batch-10')],
                          method(self.batch, 'page1', [1,2]))

    def test_prevurls(self):
        method = self.view.prevurls
        self.assertEquals([], method(self.batch))
        self.assertEquals([(1, 'page1')],
                          method(Batch(range(30), 10, start=10), url='page1'))

    def test_nexturls(self):
        method = self.view.nexturls
        self.assertEquals([
            (2, '%s/batch-10' % self.portal_url),
            (3, '%s/batch-20' % self.portal_url),
            (4, '%s/batch-30' % self.portal_url)], method(self.batch))
        self.assertEquals([
            (2, 'page1/batch-10'),
            (3, 'page1/batch-20'),
            (4, 'page1/batch-30')], method(self.batch, url='page1'))


def test_suite():
    """Collects above tests into test suite."""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSEOBatchingView))
    return suite
