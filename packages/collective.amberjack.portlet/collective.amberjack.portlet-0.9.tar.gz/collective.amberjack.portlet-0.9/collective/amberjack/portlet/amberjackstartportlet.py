from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope.schema.vocabulary import getVocabularyRegistry

from collective.amberjack.portlet import AmberjackPortletMessageFactory as _


class IAmberjackStartPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    tourId = schema.Choice(title=_(u"Tour identifier"),
                              description=_(u"Indicate the tour's identifier you want to run on this portlet"),
                              vocabulary="collective.amberjack.core.tours",
                              required=True)
    

    skinId = schema.Choice(title=_(u"Choose the skin"),
                              description=_(u"Indicate the tour's window layout"),
                              vocabulary="collective.amberjack.skins",
                              default="model_t")
    
    

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IAmberjackStartPortlet)

    def __init__(self, tourId="", skinId="model_t"):
        self.tourId = tourId
        self.skinId = skinId

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Amberjack start portlet ${tourId}/${skinId}", mapping={'tourId': self.tourId, 'skinId': self.skinId})


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('amberjackstartportlet.pt')
    
    def __init__(self, context, request, view, manager, data): 
        self.context = context 
        self.request = request 
        self.view = view 
        self.manager = manager 
        self.data = data
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()

    @property
    def available(self):
        registry = getVocabularyRegistry()
        vocab = registry.get(self.context, "collective.amberjack.core.tours")
        try:
            term = vocab.getTermByToken(self.data.tourId)
            return True
        except LookupError:
            return False
            
    def tour(self):
        return '%s?tourId=%s&skinId=%s' % (self.navigation_root_url, self.data.tourId, self.data.skinId)

    def image(self):
        return '%s/amberjack.png' % self.navigation_root_url

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IAmberjackStartPortlet)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IAmberjackStartPortlet)
