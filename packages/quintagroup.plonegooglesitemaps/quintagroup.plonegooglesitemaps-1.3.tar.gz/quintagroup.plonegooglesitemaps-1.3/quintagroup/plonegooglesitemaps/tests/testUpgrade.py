#
# Tests for quintagroup.plonegooglesitemaps upgrading
#

from base import *
from zope.component import getSiteManager

from Products.CMFPlone.utils import _createObjectByType
from Products.GenericSetup.upgrade import _upgrade_registry
from archetypes.schemaextender.interfaces import ISchemaExtender
from quintagroup.plonegooglesitemaps import config
from quintagroup.plonegooglesitemaps import upgrades as gsm_upgrades
from quintagroup.canonicalpath.interfaces import ICanonicalPath
from quintagroup.canonicalpath.interfaces import ICanonicalLink
from quintagroup.plonegooglesitemaps.content.newsextender import NewsExtender

class TestUpgrade(TestCase):

    def afterSetUp(self):
        self.setup = self.portal.portal_setup
        self.profile = "quintagroup.plonegooglesitemaps:default"

    def getUpgradeStep(self, sortkey):
        upgrades = self.setup.listUpgrades(self.profile, show_old=True)
        upgrade_id = upgrades[sortkey-1]["id"]
        step = _upgrade_registry.getUpgradeStep(self.profile, upgrade_id)
        return step

    def test_upgradeStepsRegistration(self):
        # Test upgrade steps
        upgrades = self.setup.listUpgrades(self.profile, show_old=True)
        self.assertEqual(len(upgrades), 3)
        self.assertEqual(upgrades[0]["title"].endswith("1.0 to 1.1"), True)
        self.assertEqual(upgrades[1]["title"].endswith("1.1 to 1.2"), True)
        self.assertEqual(upgrades[2]["title"].endswith("1.2 to 1.3"), True)

    def test_upgradeSetupRegistration(self):
        # Test registered upgrade profiles
        pids = [i['id'] for i in self.setup.listProfileInfo()]
        self.assertEqual("quintagroup.plonegooglesitemaps:upgrade_1_0_to_1_1" in pids, True)
        self.assertEqual("quintagroup.plonegooglesitemaps:upgrade_1_1_to_1_2" in pids, True)
        self.assertEqual("quintagroup.plonegooglesitemaps:upgrade_1_2_to_1_3" in pids, True)

    def test_step_1_0_to_1_1(self):
        # Prepare testing data
        catalog = self.portal.portal_catalog
        if "canonical_path" in catalog._catalog.names:
            catalog.delColumn("canonical_path")
        # Upgrade to 1.1 version
        step = self.getUpgradeStep(1)
        if step is not None:
            step.doStep(self.setup)
        # Canonical_path column must be added to portal_catalog
        self.assertEqual("canonical_path" in catalog._catalog.names, True)

    def test_step_1_1_to_1_2(self):
        # Prepare testing data
        catalog = self.portal.portal_catalog
        # Create container folder, update its canonical path
        folder = _createObjectByType('Folder', self.portal, id='test_folder')
        fldr_cpath = "/my_test_home_folder"
        fldr_clink = self.portal.absolute_url() + fldr_cpath
        ICanonicalPath(folder).canonical_path = fldr_cpath
        # Create inner document, update its canonical_path
        doc = _createObjectByType('Document', folder, id='test_doc')
        doc_cpath = "/test_folder/my_test_doc"
        doc_clink = self.portal.absolute_url() + doc_cpath
        ICanonicalPath(doc).canonical_path = doc_cpath
        # Add canonical_path column in catalog
        if not "canonical_path" in catalog._catalog.names:
            catalog.addColumn("canonical_path")
        # Upgrade to 1.2 versionb
        step = self.getUpgradeStep(2)
        if step is not None:
            step.doStep(self.setup)
        # canonical_link column replace canonical_path one in the portal_catalog
        self.assertEqual("canonical_link" in catalog._catalog.names, True)
        self.assertEqual("canonical_path" in catalog._catalog.names, False)
        # canonical_link property refactored from canonical_path one for inner doc
        self.assertNotEqual(ICanonicalPath(doc).canonical_path, doc_cpath)
        self.assertEqual(ICanonicalLink(doc).canonical_link, doc_clink)
        # canonical_link property refactored from canonical_path one for home folder
        self.assertNotEqual(ICanonicalPath(folder).canonical_path, fldr_cpath)
        self.assertEqual(ICanonicalLink(folder).canonical_link, fldr_clink)
        # canonical_link brain must contains updated canonical_link data
        brain = catalog(id="test_doc")[0]
        self.assertEqual(brain.canonical_link, doc_clink)
        brain = catalog(id="test_folder")[0]
        self.assertEqual(brain.canonical_link, fldr_clink)

    def test_step_1_2_to_1_3(self):
        # Prepare testing data
        cols = ["Language", "gsm_access", "gsm_genres", "gsm_stock"]
        lsm = getSiteManager(self.portal)
        catalog = self.portal.portal_catalog
        # Remove tested columns, if its exists
        [catalog.delColumn(col) for col in cols if col in catalog._catalog.names]
        # Remove schema extender adapter from local component registry, if its exists
        for r in tuple(lsm.registeredAdapters()):
            if r.factory == NewsExtender:
                lsm.unregisterAdapter(factory=r.factory, name=r.name,
                    required=r.required, provided=r.provided)
        # Upgrade to 1.3 version
        step = self.getUpgradeStep(3)
        if step is not None:
            step.doStep(self.setup)
        # Test if columns added to portal_catalog
        for col in cols:
            self.assertEqual(col in catalog._catalog.names, True)
        # Test if schema extender adapter added into local component registry
        factories = [r.factory for r in tuple(lsm.registeredAdapters())]
        self.assertEqual(NewsExtender in factories, True)

    def testUpgradeCallOnQIReinstall(self):
        # Get upgrade steps
        upgrades = _upgrade_registry.getUpgradeStepsForProfile(self.profile)
        upgrades = dict([(u.sortkey, u) for u in upgrades.values()])
        try:
            # Replace original handlers with patched ones for test calls
            called = []
            upgrades[1].handler = lambda st:called.append("1.0 to 1.1")
            upgrades[2].handler = lambda st:called.append("1.1 to 1.2")
            upgrades[3].handler = lambda st:called.append("1.2 to 1.3")
            # Run reinstallation
            self.portal.portal_quickinstaller.reinstallProducts(products=config.PROJECTNAME)
            # Test upgrades call
            self.assertEqual("1.0 to 1.1" in called, True)
            self.assertEqual("1.1 to 1.2" in called, True)
            self.assertEqual("1.2 to 1.3" in called, True)
        finally:
            # Restore original upgrade handlers
            upgrades[1].handler = gsm_upgrades.upgrade_1_0_to_1_1
            upgrades[2].handler = gsm_upgrades.upgrade_1_1_to_1_2
            upgrades[3].handler = gsm_upgrades.upgrade_1_2_to_1_3

        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUpgrade))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
