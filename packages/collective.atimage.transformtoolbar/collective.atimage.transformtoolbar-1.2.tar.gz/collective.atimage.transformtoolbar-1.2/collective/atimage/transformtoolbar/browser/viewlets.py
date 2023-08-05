from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class TransformToolbarViewlet(common.ViewletBase):
    """ Viewlet to display the icon-toolbar with transformations for ATImage
    """
            
    index = ViewPageTemplateFile('templates/toolbar.pt')


