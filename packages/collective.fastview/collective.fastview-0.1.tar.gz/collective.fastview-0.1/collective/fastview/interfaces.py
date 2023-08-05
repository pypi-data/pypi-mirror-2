
import zope.interface

from zope.publisher.interfaces.browser import IBrowserRequest

class IGlobalDefineFreeRender(IBrowserRequest):
    """ Marker interface applied for HTTP request object to notify that global defines should not be resolved.
    """
