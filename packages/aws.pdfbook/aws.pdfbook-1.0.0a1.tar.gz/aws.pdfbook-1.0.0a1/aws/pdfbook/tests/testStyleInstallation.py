#
# Unit Tests for the style install and uninstall methods
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase

from aws.pdfbook.config import *
from aws.pdfbook.Extensions.utils import getSkinsFolderNames
PROJECTNAME = 'PDFBook'

PloneTestCase.installProduct(PROJECTNAME)
PloneTestCase.setupPloneSite(products=[PROJECTNAME])

class testSkinsTool(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.tool = getattr(self.portal, 'portal_skins')

    def testSkinSelectionCreated(self):
        for skin_selection in SKINSELECTIONS:
            self.failUnless(
                skin_selection['name'] in self.tool.getSkinSelections())

    def testSkinPaths(self):
        skinsfoldernames = getSkinsFolderNames(GLOBALS)
        skins_dict = {}
        for skin in SKINSELECTIONS:
            skins_dict[skin['name']] = skin.get('layers', skinsfoldernames)
        for selection, layers in self.tool.getSkinPaths():
            if skins_dict.has_key(selection):
                for specific_layer in skins_dict[selection]:
                    self.failUnless(specific_layer in layers)
            else:
                for foldername in skinsfoldernames:
                    self.failIf(foldername in layers)

    def testSkinSelection(self):
        if SELECTSKIN:
            self.assertEqual(self.tool.getDefaultSkin(), DEFAULTSKIN)

    def testSkinFlexibility(self):
        self.assertEqual(self.tool.getAllowAny(), ALLOWSELECTION)

    def testCookiePersistance(self):
        self.assertEqual(bool(self.tool.getCookiePersistence()),
													PERSISTENTCOOKIE)

class testResourceRegistrations(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.csstool = getattr(self.portal, 'portal_css')
        self.jstool  = getattr(self.portal, 'portal_javascripts')

    def testStylesheetsInstalled(self):
        stylesheetids = self.csstool.getResourceIds()
        for css in STYLESHEETS:
            self.failUnless(css['id'] in stylesheetids)

    def testStylesheetProperties(self):
        for css in STYLESHEETS:
            res = self.csstool.getResource(css['id'])
            if css.has_key('enabled'):
                self.assertEqual(res.getEnabled(), css['enabled'])
            if css.has_key('title'):
                self.assertEqual(res.getTitle(), css['title'])
            if css.has_key('expression'):
                self.assertEqual(res.getExpression(), css['expression'])
            if css.has_key('cookable'):
                self.assertEqual(res.getCookable(), css['cookable'])
            if css.has_key('media'):
                self.assertEqual(res.getMedia(), css['media'])
            if css.has_key('rel'):
                self.assertEqual(res.getRel(), css['rel'])
            if css.has_key('rendering'):
                self.assertEqual(res.getRendering(), css['rendering'])

    def testJavascriptsInstalled(self):
        javascriptids = self.jstool.getResourceIds()
        for js in JAVASCRIPTS:
            self.failUnless(js['id'] in javascriptids)

    def testMemberStylesheetProperties(self):
        for js in JAVASCRIPTS:
            res = self.jstool.getResource(js)
            if css.has_key('enabled'):
                self.assertEqual(res.getEnabled(), p['enabled'])
            if css.has_key('expression'):
                self.assertEqual(res.getExpression(), p['expression'])
            if css.has_key('cookable'):
                self.assertEqual(res.getCookable(), p['cookable'])
            if css.has_key('inline'):
                self.assertEqual(res.getInline(), p['inline'])


class testUninstall(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.qitool    = getattr(self.portal, 'portal_quickinstaller')
        self.skinstool = getattr(self.portal, 'portal_skins')
        self.csstool   = getattr(self.portal, 'portal_css')
        self.jstool    = getattr(self.portal, 'portal_javascripts')
        self.qitool.uninstallProducts(products=[PROJECTNAME])

    def testProductUninstalled(self):
        self.failIf(self.qitool.isProductInstalled(PROJECTNAME))

    def testSkinSelectionDeleted(self):
        skin_selections = self.skinstool.getSkinSelections()
        for skin in SKINSELECTIONS:
            self.failIf(skin['name'] in skin_selections)

    def testDefaultSkinChanged(self):
        default_skin = self.skinstool.getDefaultSkin()
        if FULLRESET:
            self.assertEqual(default_skin, 'Plone Default')
        else:
            if DEFAULTSKIN:
                for skin in SKINSELECTIONS:
                    if skin['name'] == DEFAULTSKIN:
                        self.assertEqual(default_skin, skin['base'])
            else:
                self.assertEqual(default_skin, SKINSELECTIONS[0]['base'])

    def testResetSkinFlexibility(self):
        allow_any = self.skinstool.getAllowAny()
        if FULLRESET:
            self.failIf(allow_any)
        else:
            self.assertEqual(allow_any, ALLOWSELECTION)

    def testResetCookiePersistance(self):
        cookie_peristence = self.skinstool.getCookiePersistence()
        if FULLRESET:
            self.failIf(cookie_peristence)
        else:
            self.assertEqual(cookie_peristence, PERSISTENTCOOKIE)

    def testStylesheetsUninstalled(self):
        stylesheetids = self.csstool.getResourceIds()
        for css in STYLESHEETS:
            self.failIf(css['id'] in stylesheetids)

    def testJavascriptsUninstalled(self):
        javascriptids = self.jstool.getResourceIds()
        for js in JAVASCRIPTS:
            self.failIf(js['id'] in javascriptids)

if __name__ == '__main__':
    framework()
else:
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(testSkinsTool))
        suite.addTest(unittest.makeSuite(testResourceRegistrations))
        suite.addTest(unittest.makeSuite(testUninstall))
        return suite
