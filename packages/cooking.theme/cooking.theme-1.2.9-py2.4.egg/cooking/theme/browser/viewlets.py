from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

# Sample code for a basic viewlet (In order to use it, you'll have to):
# - Un-comment the following useable piece of code (viewlet python class).
# - Rename the viewlet template file ('browser/viewlet.pt') and edit the
#   following python code accordingly.
# - Edit the class and template to make them suit your needs.
# - Make sure your viewlet is correctly registered in 'browser/configure.zcml'.
# - If you need it to appear in a specific order inside its viewlet manager,
#   edit 'profiles/default/viewlets.xml' accordingly.
# - Restart Zope.
# - If you edited any file in 'profiles/default/', reinstall your package.
# - Once you're happy with your viewlet implementation, remove any related
#   (unwanted) inline documentation  ;-p

from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from Products.CMFPlone.utils import safe_unicode
from cgi import escape

class SimpleTitleViewlet(common.TitleViewlet):
    def index(self):
        portal_title = safe_unicode(self.portal_title())
        page_title = safe_unicode(self.page_title())
        return u"<title>%s</title>" % (escape(portal_title))


class SiteTitleViewlet(common.ViewletBase):
    """A custom version of the path bar (breadcrumbs) viewlet, which
    uses slightly different markup.
    """
    render = ViewPageTemplateFile('templates/site_title.pt')
    # The update() method, inherited from the base class, takes care
    # of initializing various variables used in the template

class SiteDomainViewlet(common.ViewletBase):
    """A viewlet to display current site domain name"""
    render = ViewPageTemplateFile('templates/site_domain.pt')    
    
class SiteHeaderViewlet(common.ViewletBase):
    """A custom version of the path bar (breadcrumbs) viewlet, which
    uses slightly different markup.
    """
    render = ViewPageTemplateFile('templates/site_header.pt')
    # The update() method, inherited from the base class, takes care
    # of initializing various variables used in the template

