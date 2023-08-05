from zope.component import getMultiAdapter

from Products.Five.browser import BrowserView


class CU3ERXML(BrowserView):
    """XML configuration."""

    def __call__(self, request=None, response=None):
        """Returns config.xml for CU3ER."""
        self.request.response.setHeader("Content-type", "text/xml")
        self.parent_context = None

        cstate = getMultiAdapter((self.context, self.request), name='plone_context_state')

        # if we have a default page use it as context
        if not cstate.is_default_page() and self.context.getDefaultPage():
            self.parent_context = self.context
            self.context = self.context[self.context.getDefaultPage()]
        
        # check if the default page has a valid configuration
        schema = getattr(self.context, 'Schema', None)
        if schema is None:
            return None
        field = schema().getField('cu3er_config')
        if field is None:
            return None

        # We need to return raw here, otherwise the xml will be filtered.
        return field.getRaw(self.context)
