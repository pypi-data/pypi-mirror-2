from  plone.portlet.collection import collection 

from zope.formlib import form

from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from plone.portlet.collection import PloneMessageFactory as _

class ICollectionListPortlet(collection.ICollectionPortlet):
    """Collection portlet that handles collection as a list"""
    pass

class AddForm(collection.AddForm):
    """Portlet add form.
    
    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ICollectionListPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Add Collection List Portlet")
    description = _(u"This portlet display a listing of items from a Collection in a list.")
