from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class PiwikPagesViewlet(ViewletBase):
    render = ViewPageTemplateFile('viewlet.pt')

