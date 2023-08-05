import types

from Acquisition import aq_inner

from zope.interface import Interface, implements

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from collective.seobatching.config import SHEET_ID, PROP_ID, BATCH_PLACEHOLDER


class ISEOBatchingView(Interface):
    """View to provide seo batching urls"""

    def pageurl(batch, url=None, b_start=None, pagenumber=-1):
        """Returns pageurl from batch"""
    
    def navurls(batch, url=None, navlist=None):
        """Returns pageurls from batch for quantumleaps"""
    
    def prevurls(batch, url=None):
        """Returns prev navigation list from batch"""
    
    def nexturls(batch, url=None):
        """Returns next navigation list from batch"""


class SEOBatchingView(BrowserView):
    """See interface"""

    implements(ISEOBatchingView)

    def pageurl(self, batch, url=None, b_start=None, pagenumber=-1):
        """See interface"""
        if url is None:
            url = aq_inner(self.context).absolute_url()

        if pagenumber == -1:
            pagenumber = batch.pagenumber

        if b_start is None:
            b_start = pagenumber * (batch.size - batch.overlap) - batch.size

        # for the first page (b_start == 0) we return clear url w/o any subpath
        if b_start != 0:
            # get batch url pattern and fill in <num> placeholder
            pattern = self._getPattern()
            if pattern:
                if not isinstance(b_start, types.StringTypes):
                    b_start = str(b_start)
                return '%s/%s' % (url, pattern.replace(BATCH_PLACEHOLDER,
                                                       b_start))
        
        return url
    
    def navurls(self, batch, url=None, navlist=None):
        """See interface"""
        if url is None:
            url = self.context.absolute_url()

        if navlist is None:
            navlist = batch.navlist

        pu = self.pageurl
        return map(lambda x: (x, pu(batch, url, pagenumber=x)), navlist)
    
    def prevurls(self, batch, url=None):
        """See interface"""
        if url is None:
            url = self.context.absolute_url()
        return self.navurls(batch, url, batch.prevlist)
    
    def nexturls(self, batch, url=None):
        """See interface"""
        if url is None:
            url = self.context.absolute_url()
        return self.navurls(batch, url, batch.nextlist)

    @memoize
    def _getPattern(self, sheet_id=SHEET_ID, prop_id=PROP_ID):
        """Returns value of a given property"""
        props_tool = getToolByName(self.context, 'portal_properties')
        if sheet_id in props_tool.objectIds():
            value = getattr(props_tool, sheet_id).getProperty(prop_id, None)
            if isinstance(value, types.StringTypes) and value.strip():
                return value.strip()
        return None
