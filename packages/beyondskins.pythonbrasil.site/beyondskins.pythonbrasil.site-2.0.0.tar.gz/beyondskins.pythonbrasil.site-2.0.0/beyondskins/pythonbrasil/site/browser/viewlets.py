from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase, LogoViewlet as LogoViewletBase
from zope.component import getMultiAdapter

class LogoViewlet(LogoViewletBase):
    render = ViewPageTemplateFile('templates/logo.pt')

    def update(self):
        super(LogoViewlet, self).update()
        tools = getMultiAdapter((self.context, self.request),
                                  name=u'plone_tools')
        portal_url = tools.url()
        portal = self.portal_state.portal()
        contentpath = portal_url.getRelativeContentPath(self.context)
        if contentpath:
            # Exemplo: 2010-logo.jpg
            logoName = '%s-%s' % (contentpath[0],portal.restrictedTraverse('base_properties').logoName)
            try:
                logo_tag = portal.restrictedTraverse(logoName).tag()
            except:
                logo_tag = self.logo_tag
            self.logo_tag = logo_tag
                

