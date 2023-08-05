from Acquisition import aq_base
from Products.CMFPlone.CatalogTool import CatalogTool

from Products.LinguaPlone import config
from Products.LinguaPlone.tests.base import LinguaPloneTestCase


class TestPatchesSetup(LinguaPloneTestCase):

    def testCatalogPatch(self):
        if config.I18NAWARE_CATALOG:
            self.failUnless(hasattr(CatalogTool, '__lp_old_searchResults'))
        else:
            self.failIf(hasattr(CatalogTool, '__lp_old_searchResults'))


class TestInstallSetup(LinguaPloneTestCase):

    def testTools(self):
        # Check all tools are installed
        portal = aq_base(self.portal)
        self.failUnless(hasattr(portal, 'archetype_tool'))
        self.failUnless(hasattr(portal, 'portal_languages'))

    def testPortalTypes(self):
        # Check all content types are installed
        types = aq_base(self.portal.portal_types)
        self.failUnless(hasattr(types, 'SimpleType'))
        self.failUnless(hasattr(types, 'DerivedType'))
        self.failUnless(hasattr(types, 'SimpleFolder'))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPatchesSetup))
    suite.addTest(makeSuite(TestInstallSetup))
    return suite
