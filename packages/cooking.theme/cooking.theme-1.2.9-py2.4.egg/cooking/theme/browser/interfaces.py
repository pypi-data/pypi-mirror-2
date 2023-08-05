from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from plone.portlets.interfaces import IPortletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "Ameria Cooking theme" theme, this interface must be its layer
       (in theme/viewlets/configure.zcml).
    """

class ISimpleTitleViewlet(IViewletManager):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "Ameria Cooking theme" theme, this interface must be its layer
       (in theme/viewlets/configure.zcml).
    """

class IPortalSiteHeader(IViewletManager):
    """A viewlet manager that sits above all content in left column, normally used to hold
    the content views (tabs) and associated actions.
    """
            
class IPortalUpperRightColumn(IViewletManager):
    """A viewlet manager that sits above all content in right column.
    """

