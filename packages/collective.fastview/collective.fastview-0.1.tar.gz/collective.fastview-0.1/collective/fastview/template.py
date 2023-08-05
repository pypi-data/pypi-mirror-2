import zope.interface

from zope.publisher.interfaces.browser import IBrowserRequest

from collective.fastview.interfaces import IGlobalDefineFreeRender

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class PageTemplate(ZopeTwoPageTemplateFile):
    """ Enhanched page template handler for Plone.

    These templates assume that the template is rendered without global defines.
    This makes it suitable for anonymous resource rendering where the speed
    is issue.
    """

    def getRequest(self):
        """
        @return: The current HTTP request object
        """
        try:
            root = self.getPhysicalRoot()
        except AttributeError:
            try:
                root = self.context.getPhysicalRoot()
            except AttributeError:
                root = None

        request = getattr(root, 'REQUEST', None)

        assert request != None, "HTTP request object was not available for a view. Is acquisition chain set-up properly?"

        return request

    def __call__(self, *args, **kwargs):

        # Set flag that we don't need global defines
        request = self.getRequest()
        zope.interface.alsoProvides(request, IGlobalDefineFreeRender)

        # Render template normally
        return ZopeTwoPageTemplateFile.__call__(self, *args, **kwargs)