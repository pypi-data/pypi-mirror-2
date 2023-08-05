from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form
from zope.interface import implements

from collective.amberjack.core.interfaces import ITourManager
from collective.amberjack.portlet import AmberjackPortletMessageFactory as _


class IAmberjackChoicePortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    user_title = schema.TextLine(
                        title=_(u"Describe this set of tours"),
                        description=_(u"This text will appear as portlet's title"),
                        required=False,
                        )

    tours = schema.List(
                title=_(u"Choose the tours"),
                description=_(u"Select the tours that can be choosen by an user on this portlet"),
                value_type=schema.Choice(
                              vocabulary="collective.amberjack.core.tours",
                              required=True)
                )


    skinId = schema.Choice(title=_(u"Choose the skin"),
                              description=_(u"Indicate the tour's window layout"),
                              vocabulary="collective.amberjack.skins",
                              default="model_t")
    

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IAmberjackChoicePortlet)

    def __init__(self, user_title=None, tours=None, skinId="model_t"):
        if tours is None:
            self.tours = []
        else:
            self.tours = tours
        self.skinId = skinId
        self.user_title = user_title

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Amberjack Choice portlet ${skinId}", mapping={'skinId': self.skinId})


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('amberjackchoiceportlet.pt')
    
    def __init__(self, context, request, view, manager, data): 
        self.context = context 
        self.request = request 
        self.view = view 
        self.manager = manager 
        self.data = data

    @property
    def available(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        navigation_root_url = portal_state.navigation_root_url()
        
        tour_manager = getUtility(ITourManager)
        available_tours = tour_manager.getTours(self.context)
        if self.data.tours:
            tour_ids = self.data.tours
            tours = [(tour_id, tour)
                     for tour_id, tour in available_tours
                     if tour_id in tour_ids]
        else:
            tours = available_tours
            
        selected_tours = []
        for tour_id, tour in tours:
            url ='%s?tourId=%s&skinId=%s' % (navigation_root_url,
                                             tour_id,
                                             self.data.skinId)
            selected_tours.append({'object': tour,
                                   'title': tour.title,
                                   'url': url})

        self.selected_tours = selected_tours
        return bool(self.selected_tours)
    
    def tours(self):
        return self.selected_tours

    def user_title(self):
        return self.data.user_title
    
    # TODO: return true if tour is completed
    def completed(self):
        return bool(1);
         

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IAmberjackChoicePortlet)

    def create(self, data):
        return Assignment(**data)
    

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IAmberjackChoicePortlet)
