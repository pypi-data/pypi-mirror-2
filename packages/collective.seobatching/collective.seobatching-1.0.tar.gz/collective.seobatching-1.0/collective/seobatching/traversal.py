import re
import sys
import types
import logging

from ZPublisher.BaseRequest import DefaultPublishTraverse

from Products.CMFCore.utils import getToolByName

from collective.seobatching.config import SHEET_ID, PROP_ID, BATCH_PLACEHOLDER


logger = logging.getLogger('collective.seobatching')
def logException(msg, context=None):
    logger.exception(msg)
    if context is not None:
        error_log = getattr(context, 'error_log', None)
        if error_log is not None:
            error_log.raising(sys.exc_info())

# make this as a separate function for easier usage in other custom traversers
def getBatchStartFromPath(context, name):
    props_tool = getToolByName(context, 'portal_properties')
    if SHEET_ID in props_tool.objectIds():
        value = getattr(props_tool, SHEET_ID).getProperty(PROP_ID, None)
        if isinstance(value, types.StringTypes) and BATCH_PLACEHOLDER in value:
            try:
                pattern = re.compile('^%s$' % value.strip().replace(
                                        BATCH_PLACEHOLDER, '(\d+)'))
            except Exception, e:
                # invalid pattern entered in properties tool
                logException(u"Invalid pattern entered in %s property "
                                u"inside properties_tool!" % PROP_ID, context)
            else:
                match = pattern.findall(name)
                if len(match) > 0:
                    b_start = None

                    # we need to proper handle cases when site administrator
                    # entered more than one BATCH_PLACEHOLDER placeholder
                    # into batch pattern inside portal_properties tool
                    if isinstance(match[0], (types.ListType, types.TupleType)):
                        if len(match[0]) > 0:
                            b_start = match[0][0]
                    else:
                        b_start = match[0]
                    
                    if b_start:
                        return b_start
    return None

class SEOBatchingTraverser(DefaultPublishTraverse):
    """Tests batch pattern set in portal_properties against current lookup name
    and inserts batch start argument into request on success.
    """

    def publishTraverse(self, request, name):
        # get b_start from path
        b_start = getBatchStartFromPath(self.context, name)
        if b_start is not None:
            request.set('b_start', b_start)
            return self.context
        return super(SEOBatchingTraverser, self).publishTraverse(request, name)
