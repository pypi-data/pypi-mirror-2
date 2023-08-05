from base import *
from zope.component import getSiteManager
from archetypes.schemaextender.interfaces import ISchemaExtender


class TestGoogleSitemapsInstallation(TestCase):

    def testType(self):
        pt = self.portal.portal_types
        self.assert_('Sitemap' in pt.objectIds(), 
            'No "Sitemap" type after installation')
        #Test views
        views = pt.getTypeInfo('Sitemap').view_methods
        self.assert_('sitemap.xml' in views, 
            'No "sitemap.xml" view for Sitemap type')
        self.assert_('mobile-sitemap.xml' in views, 
            'No "mobile-sitemap.xml" view for Sitemap type')
        self.assert_('news-sitemap.xml' in views, 
            'No "news-sitemap.xml" view for Sitemap type')

    def testGSMProperties(self):
        pp = self.portal.portal_properties

        # Test types_not_searched
        self.assert_("Sitemap" in pp['site_properties'].getProperty('types_not_searched'), 
            'No "Sitemap" added to types not searched on installation')
        # Test metaTypesNotToList
        self.assert_("Sitemap" in pp['navtree_properties'].getProperty('metaTypesNotToList'), 
            'No "Sitemap" added to types not to list on installation')

        # Test 'googlesitemap_properties'
        self.assert_('googlesitemap_properties' in pp.objectIds(), 
            'No "googlesitemap_properties" after installation')
        qsmprops = pp['googlesitemap_properties']
        self.assert_(qsmprops.hasProperty('verification_filenames'),
            'No "verification_filenames" property added on installation')

    def testSkins(self):
        ps = self.portal.portal_skins
        self.assert_('plonegooglesitemaps' in ps.objectIds(), 
            'No "plonegooglesitemaps" skin layer in portal_skins')
        self.assert_('plonegooglesitemaps' in ps.getSkinPath(ps.getDefaultSkin()),
            'No "plonegooglesitemaps" skin layer in default skin')

    def testConfiglet(self):
        cp = self.portal.portal_controlpanel
        self.assert_([1 for ai in cp.listActionInfos() if ai['id']=='GoogleSitemaps'], 
            'No "GoogleSitemaps" configlet added to plone control panel')

    def testNewsSchemaExtenderRegistered(self):
        lsm = getSiteManager(self.portal)
        news = self.portal.invokeFactory("News Item", id="test_news")
        news = getattr(self.portal, "test_news")
        self.assertNotEqual(lsm.queryAdapter(news, interface=ISchemaExtender), None)


class TestGoogleSitemapsUninstallation(TestCase):

    def afterSetUp(self):
        super(TestGoogleSitemapsUninstallation, self).afterSetUp()
        self.portal.portal_quickinstaller.uninstallProducts(
            products=['quintagroup.plonegooglesitemaps',])
        self._refreshSkinData()

    def testNewsSchemaExtenderUnregistered(self):
        lsm = getSiteManager(self.portal)
        news = self.portal.invokeFactory("News Item", id="test_news")
        news = getattr(self.portal, "test_news")
        self.assertEqual(lsm.queryAdapter(news, interface=ISchemaExtender), None)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGoogleSitemapsInstallation))
    suite.addTest(makeSuite(TestGoogleSitemapsUninstallation))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
#    framework()
