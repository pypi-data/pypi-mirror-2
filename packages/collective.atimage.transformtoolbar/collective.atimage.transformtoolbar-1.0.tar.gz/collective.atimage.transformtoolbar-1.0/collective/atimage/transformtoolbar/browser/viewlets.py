from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from Acquisition import aq_inner
from Products.ATContentTypes.interface import IATImage

class TransformToolbarViewlet(common.ViewletBase):
    """ Viewlet to display the icon-toolbar with transformations for ATImage
    """
            
    index = ViewPageTemplateFile('templates/toolbar.pt')


