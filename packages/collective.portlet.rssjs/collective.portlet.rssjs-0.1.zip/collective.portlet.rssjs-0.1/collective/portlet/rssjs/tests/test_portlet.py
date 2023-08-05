from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.rssjs import rssjsportlet

from collective.portlet.rssjs.tests.base import TestCase


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.rssjs.RSSJSPortlet')
        self.assertEquals(portlet.addview,
                          'collective.portlet.rssjs.RSSJSPortlet')

    def test_interfaces(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        portlet = rssjsportlet.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.rssjs.RSSJSPortlet')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add
        # form.
        # Note: if the portlet has a NullAddForm, simply call
        # addview() instead of the next line.
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   rssjsportlet.Assignment))

    def test_invoke_edit_view(self):
        # NOTE: This test can be removed if the portlet has no edit form
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = rssjsportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, rssjsportlet.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        # TODO: Pass any keyword arguments to the Assignment constructor
        assignment = rssjsportlet.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, rssjsportlet.Renderer))


class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        assignment = assignment or rssjsportlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render_more_link_contains_url(self):
        url = 'http://feeds.plone.org/plonenews'
        _renderer = self.renderer(context=self.portal,
                          assignment=rssjsportlet.Assignment(url=url))
        _renderer = _renderer.__of__(self.folder)
        _renderer.update()
        output = _renderer.render()
        self.failUnless('<a class="portletRssFeedMoreLink" href="http://feeds.plone.org/plonenews' in output)

    def test_render_more_link_contains_count(self):
        count = 4
        _renderer = self.renderer(context=self.portal,
                          assignment=rssjsportlet.Assignment(count=count))
        _renderer = _renderer.__of__(self.folder)
        _renderer.update()
        output = _renderer.render()
        self.failUnless('<a class="portletRssFeedMoreLink" href="" count="4"' in output)

    def test_render_more_link_contains_count(self):
        count = 4
        _renderer = self.renderer(context=self.portal,
                          assignment=rssjsportlet.Assignment(count=count))
        _renderer = _renderer.__of__(self.folder)
        _renderer.update()
        output = _renderer.render()
        self.failUnless('<a class="portletRssFeedMoreLink" href="" count="4"' in output)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
