from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase


class CU3ERViewlet(ViewletBase):
    index = ViewPageTemplateFile('templates/cu3er.pt')

    def available(self):
        schema = getattr(self.context, 'Schema', None)
        if schema is None:
            return None
        field = schema().getField('cu3er_enabled')
        if field is None:
            return None
        return field.get(self.context)

    def get_height(self):
        schema = getattr(self.context, 'Schema', None)
        if schema is None:
            return None
        field = schema().getField('cu3er_height')
        if field is None:
            return None
        return field.get(self.context)

    def get_width(self):
        schema = getattr(self.context, 'Schema', None)
        if schema is None:
            return None
        field = schema().getField('cu3er_width')
        if field is None:
            return None
        return field.get(self.context)

    def get_js_config(self):
        return """var flashvars = {};
            flashvars.xml = "collective.cu3er.config.xml";
            var attributes = {};
            attributes.wmode = "transparent";
            attributes.id = "slider";
            swfobject.embedSWF("++resource++collective.cu3er.cu3er.swf", "cu3er-object", "%(width)s", "%(height)s", "9", "++resource++collective.cu3er.expressInstall.swf", flashvars, attributes);""" % dict(
                height = self.get_height(),
                width = self.get_width(),
            )

    def get_css_config(self):
        return """#cu3er-object {width: %(width)spx; outline:0;}""" % dict(
                width = self.get_width(),
            )
