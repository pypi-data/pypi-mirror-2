from zope.interface import Interface

class ISEOBatching(Interface):
    """Marker interface for objects which support traversal urls for
    batch macro instead of using query parameters.
    """
