
from collective.portlet.collectionmultiview.interfaces import ICollectionMultiViewBaseRenderer,ICollectionMultiViewRenderer
from zope.component import adapts
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize
from Acquisition import aq_inner
from plone.app.portlets.portlets import base

class BaseRenderer(object):
     adapts(ICollectionMultiViewBaseRenderer)
     implements(ICollectionMultiViewRenderer)

     def __init__(self,base):
         self.request = base.request
         self.context = aq_inner(base.context)
         self.data = base.data
         self.results = base.results
         self.collection_url = base.collection_url
         self.base = base
     
     def tag(self,obj,scale='tile',css_class='tileImage'):
         context = aq_inner(obj)
         # test for leadImage and normal image  
         
         for fieldname in ['leadImage','image']:
             field = context.getField(fieldname)
             if field is not None:
                if field.get_size(context) != 0:
                   return field.tag(context, scale=scale, css_class=css_class)
         return ''

class CollectionList(BaseRenderer):
    """Adapter that displays CollectionMultiViewPortlet in a list mode"""
    render = ViewPageTemplateFile('skins/cooking_theme_custom_templates/collection_list.pt')

class CollectionDetails(BaseRenderer):
    """Adapter that displays CollectionMultiViewPortlet in a list mode"""
    render = ViewPageTemplateFile('skins/cooking_theme_custom_templates/collection_details.pt')
