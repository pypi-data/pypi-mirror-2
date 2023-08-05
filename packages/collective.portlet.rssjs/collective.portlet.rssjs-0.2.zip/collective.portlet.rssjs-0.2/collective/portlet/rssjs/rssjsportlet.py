from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.rssjs import RSSJSPortletMessageFactory as _


class IRSSJSPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    portlet_title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of the portlet.  If omitted, the title of the feed will be used.'),
        required=False,
        default=u''
        )

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)

    url = schema.TextLine(title=_(u'URL of RSS feed'),
                        description=_(u'Link of the RSS feed to display.'),
                        required=True,
                        default=u'')


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IRSSJSPortlet)

    portlet_title = u''

    @property
    def title(self):
        """return the title with RSS feed title or from URL"""
        return u'RSS: '+self.url[:20]

    def __init__(self, portlet_title=u'', count=5, url=u""):
        self.portlet_title = portlet_title
        self.count = count
        self.url = url


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('rssjsportlet.pt')

    @property 
    def url(self):
        return self.data.url

    @property 
    def count(self):
        return self.data.count

    @property
    def title(self):
        """return title of feed for portlet"""
        return getattr(self.data, 'portlet_title', '') or 'Feed'

    @property
    def customtitle(self):
        """Has a custom title been defined 
           in the assignment?
           returns yes or no
        """
        if getattr(self.data, 'portlet_title', ''):
            return 'yes'
        else:
            return 'no'


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IRSSJSPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IRSSJSPortlet)
