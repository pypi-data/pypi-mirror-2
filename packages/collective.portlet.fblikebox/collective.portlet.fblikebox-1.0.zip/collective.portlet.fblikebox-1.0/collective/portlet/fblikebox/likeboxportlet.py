from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base


from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.fblikebox import LikeBoxPortletMessageFactory as _


class ILikeBoxPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    fb_page_id = schema.TextLine(
        title=_(u"Facebook Page ID"),
        description=_(u"The ID of the Facebook Page for this Like box."),
        required=True)

    box_width = schema.Int(
        title=_(u'Display width'),
        description=_(u'Pixel width of like box.'),
        required=True,
        default=150)

    box_height = schema.Int(
        title=_(u'Display height'),
        description=_(u'Pixel height of like box.'),
        required=True,
        default=500)

    show_header = schema.Bool(
        title=_(u"Show header"),
        description=_(u"Show the 'Find us on Facebook' bar at top. Only shown when either stream or connections are present."),
        required=True,
        default=True)

    show_stream = schema.Bool(
        title=_(u"Show stream"),
        description=_(u"Show the profile stream for the public profile."),
        required=True,
        default=True)

    connections = schema.Int(
        title=_(u"Connections"),
        description=_(u"Show a sample of this many users who have liked this Page."),
        required=True,
        default=10)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ILikeBoxPortlet)

    # some_field = u""
    fb_page_id = u"185550966885"
    box_width = 150
    box_height = 500
    show_header = True
    show_stream = True
    connections = 10
    

    def __init__(
                self,
                fb_page_id=u"185550966885", 
                box_width=150, 
                box_height=500, 
                show_header=True,
                show_stream=True,
                connections=10):
                        
        self.fb_page_id = fb_page_id
        self.box_width = box_width
        self.box_height = box_height
        self.show_header = show_header
        self.show_stream = show_stream
        self.connections = connections

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Like-Box portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('likeboxportlet.pt')


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ILikeBoxPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ILikeBoxPortlet)
