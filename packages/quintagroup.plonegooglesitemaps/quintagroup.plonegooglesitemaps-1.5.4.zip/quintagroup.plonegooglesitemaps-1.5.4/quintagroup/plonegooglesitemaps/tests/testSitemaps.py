#
# Tests related to general Sitemap type.
#
from base import *
from DateTime import DateTime
from zope.interface import alsoProvides
from zope.publisher.browser import TestRequest

from Products.Archetypes import atapi
from Products.CMFPlone.utils import _createObjectByType

from quintagroup.plonegooglesitemaps.browser.sitemapview import SitemapView
from quintagroup.plonegooglesitemaps.browser.newssitemapview import NewsSitemapView
from quintagroup.plonegooglesitemaps.browser.mobilesitemapview import MobileSitemapView


class TestSitemapType(FunctionalTestCase):

    def afterSetUp(self):
        super(TestSitemapType, self).afterSetUp()
        self.contentSM = _createObjectByType('Sitemap', self.portal, id='google-sitemaps')

    def testFields(self):
        field_ids = map(lambda x:x.getName(), self.contentSM.Schema().fields())
        # test old Sitemap settings fields
        self.assert_('id' in field_ids)
        self.assert_('portalTypes' in field_ids)
        self.assert_('states' in field_ids)
        self.assert_('blackout_list' in field_ids)
        self.assert_('urls' in field_ids)
        self.assert_('pingTransitions' in field_ids)
        # test new sitemap type field
        self.assert_('sitemapType' in field_ids)

    def testSitemapTypes(self):
        sitemap_types = self.contentSM.getField('sitemapType').Vocabulary().keys()
        self.assert_('content' in sitemap_types)
        self.assert_('mobile' in sitemap_types)
        self.assert_('news' in sitemap_types)

    def testAutoSetLayout(self):
        response = self.publish('/%s/createObject?type_name=Sitemap' % \
                                self.portal.absolute_url(1), basic=self.auth)
        location = response.getHeader('location')
        newurl = location[location.find('/'+self.portal.absolute_url(1)):]

        msm_id = 'mobile_sitemap'
        form = {'id': msm_id,
                'sitemapType':'mobile',
                'portalTypes':['Document',],
                'states':['published'],
                'form_submit':'Save',
                'form.submitted':1,
                }
        post_data = StringIO(urlencode(form))
        response = self.publish(newurl, request_method='POST', stdin=post_data, basic=self.auth)
        msitemap = getattr(self.portal, msm_id)

        self.assertEqual(msitemap.defaultView(), 'mobile-sitemap.xml')

    def txestPingSetting(self):
        pwf = self.workflow['plone_workflow']
        self.assertEqual(self.contentSM.getPingTransitions(), ())

        self.contentSM.setPingTransitions(('plone_workflow#publish',))
        self.assertEqual(self.contentSM.getPingTransitions(), ('plone_workflow#publish',))
        self.assert_(ping_googlesitemap in pwf.scripts.keys(),"Not add wf script")

    def testWorkflowStates(self):
        wfstates = self.contentSM.getWorkflowStates()
        self.assertEqual(isinstance(wfstates, atapi.DisplayList), True)
        self.assertEqual("published" in wfstates.keys(), True)

    def testWorkflowStates(self):
        wftrans = self.contentSM.getWorkflowTransitions()
        self.assertEqual(isinstance(wftrans, atapi.DisplayList), True)
        self.assertEqual("simple_publication_workflow#publish" in wftrans.keys(), True)


class TestSettings(FunctionalTestCase):

    def afterSetUp(self):
        super(TestSettings, self).afterSetUp()
        self.gsm_props = self.portal.portal_properties['googlesitemap_properties']
        self.contentSM = _createObjectByType('Sitemap', self.portal, id='google-sitemaps')
        self.sitemapUrl = '/'+self.portal.absolute_url(1) + '/google-sitemaps'
        # Add testing document to portal
        self.my_doc = _createObjectByType('Document', self.portal, id='my_doc')
        self.my_doc.edit(text_format='plain', text='hello world')
        self.my_doc_url = self.my_doc.absolute_url()

    def testMetaTypeToDig(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

        self.contentSM.setPortalTypes([])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.contentSM.setPortalTypes(['Document'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def testStates(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        self.contentSM.setStates(['visible'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.contentSM.setStates(['published'])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def test_blackout_entries(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        self.contentSM.setBlackout_list((self.my_doc.getId(),))

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.my_doc_url))

        self.contentSM.setBlackout_list([])
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.my_doc_url))

    def test_regexp(self):
        self.workflow.doActionFor(self.my_doc, 'publish')
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(not hasURL(sitemap, self.portal.absolute_url()))

        regexp = "s/\/%s//"%self.my_doc.getId()
        self.contentSM.setReg_exp([regexp])

        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()
        self.assert_(hasURL(sitemap, self.portal.absolute_url()))

    def test_add_urls(self):
        self.contentSM.setUrls(['http://w1', 'w2', '/w3'])
        w1_url = 'http://w1'
        w2_url = self.portal.absolute_url() + '/w2'
        w3_url = self.portal.getPhysicalRoot().absolute_url() + '/w3'
        sitemap = self.publish(self.sitemapUrl, self.auth).getBody()

        self.assert_(hasURL(sitemap, w1_url))
        self.assert_(hasURL(sitemap, w2_url))
        self.assert_(hasURL(sitemap, w3_url))


class TestPinging(FunctionalTestCase):

    def afterSetUp(self):
        super(TestPinging, self).afterSetUp()
        self.workflow.setChainForPortalTypes(pt_names=('News Item','Document'),
                                             chain="simple_publication_workflow")
        self.gsm_props = self.portal.portal_properties['googlesitemap_properties']
        # Add sitemaps
        self.contentSM = _createObjectByType('Sitemap', self.portal, id='google-sitemaps')
        self.contentSM.setPingTransitions(('simple_publication_workflow#publish',))
        self.newsSM = _createObjectByType('Sitemap', self.portal, id='news-sitemaps')
        self.newsSM.setPortalTypes(('News Item','Document'))
        self.newsSM.setPingTransitions(('simple_publication_workflow#publish',))
        self.sitemapUrl = '/'+self.portal.absolute_url(1) + '/google-sitemaps'
        # Add testing document to portal
        self.my_doc = _createObjectByType('Document', self.portal, id='my_doc')
        self.my_news = _createObjectByType('News Item', self.portal, id='my_news')

    def testAutomatePinging(self):
        # 1. Check for pinging both sitemaps
        back_out, myout = sys.stdout, StringIO()
        sys.stdout = myout
        try:
            self.workflow.doActionFor(self.my_doc, 'publish')
            myout.seek(0)
            data = myout.read()
        finally:
            sys.stdout = back_out

        self.assert_('Pinged %s sitemap to Google' % self.contentSM.absolute_url() in data,
                     "Not pinged %s: '%s'" % (self.contentSM.id, data))
        self.assert_('Pinged %s sitemap to Google' % self.newsSM.absolute_url() in data,
                     "Not pinged %s: '%s'" % (self.newsSM.id, data))

        # 2. Check for pinging only news-sitemap sitemaps
        back_out, myout = sys.stdout, StringIO()
        sys.stdout = myout
        try:
            self.workflow.doActionFor(self.my_news, 'publish')
            myout.seek(0)
            data = myout.read()
        finally:
            sys.stdout = back_out

        self.assert_('Pinged %s sitemap to Google' % self.newsSM.absolute_url() in data,
                     "Not pinged %s: '%s'" % (self.newsSM.id, data))
        self.assert_(not 'Pinged %s sitemap to Google' % self.contentSM.absolute_url() in data,
                     "Pinged %s on news: '%s'" % (self.contentSM.id, data))

    def testPingingWithSetupForm(self):
        # Ping news and content sitemaps
        formUrl = '/'+self.portal.absolute_url(1) + '/prefs_gsm_settings'
        qs = 'smselected:list=%s&smselected:list=%s&form.button.Ping=1&form.submitted=1' % \
             (self.contentSM.id, self.newsSM.id)

        back_out, myout = sys.stdout, StringIO()
        sys.stdout = myout
        try:
            response = self.publish("%s?%s" % (formUrl, qs), basic=self.auth)
            myout.seek(0)
            data = myout.read()
        finally:
            sys.stdout = back_out

        self.assert_('Pinged %s sitemap to Google' % self.contentSM.absolute_url() in data,
                     "Not pinged %s: '%s'" % (self.contentSM.id, data))
        self.assert_('Pinged %s sitemap to Google' % self.newsSM.absolute_url() in data,
                     "Not pinged %s: '%s'" % (self.newsSM.id, data))


class TestContextSearch(TestCase):
    """ Test if sitemaps collect objects from the container,
        where it added to, but not from the portal root.
    """
    def prepareTestContent(self, smtype, ptypes, ifaces=()):
        # Create test folder
        tfolder = _createObjectByType("Folder", self.portal, id="test-folder")
        # Add SiteMap in the test folder
        self.sm = _createObjectByType("Sitemap", tfolder, id='sitemap',
                                      sitemapType=smtype, portalTypes=ptypes)
        self.sm.at_post_create_script()
        # Add content in root and in the test folder
        pubdate = (DateTime()+1).strftime("%Y-%m-%d")
        root_content = _createObjectByType(ptypes[0], self.portal, id='root-content')
        inner_content = _createObjectByType(ptypes[0], tfolder, id='inner-content')
        for obj in (root_content, inner_content):
            self.workflow.doActionFor(obj, 'publish')
            if ifaces:
                alsoProvides(obj, ifaces)
            obj.edit(effectiveDate=pubdate) # this also reindex object
        self.inner_path = '/'.join(inner_content.getPhysicalPath())
        
    def testGoogleSitemap(self):
        self.prepareTestContent("content", ("Document",))
        filtered = SitemapView(self.sm, TestRequest()).getFilteredObjects()
        self.assertEqual(map(lambda x:x.getPath(), filtered), [self.inner_path,])

    def testNewsSitemap(self):
        self.prepareTestContent("news", ("News Item",))
        filtered = NewsSitemapView(self.sm, TestRequest()).getFilteredObjects()
        self.assertEqual(map(lambda x:x.getPath(), filtered), [self.inner_path,])

    def testMobileSitemap(self):
        self.patchMobile()
        self.prepareTestContent("content", ("Document",), (IMobileMarker,))
        filtered = MobileSitemapView(self.sm, TestRequest()).getFilteredObjects()
        self.assertEqual(map(lambda x:x.getPath(), filtered), [self.inner_path,])


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSitemapType))
    suite.addTest(makeSuite(TestSettings))
    suite.addTest(makeSuite(TestPinging))
    suite.addTest(makeSuite(TestContextSearch))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
#    framework()
