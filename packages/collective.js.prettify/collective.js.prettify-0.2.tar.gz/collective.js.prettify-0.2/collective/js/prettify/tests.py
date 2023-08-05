import unittest

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

ptc.setupPloneSite(products=['collective.js.prettify'])

from Products.CMFCore.utils import getToolByName

import collective.js.prettify


class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.js.prettify)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass
    
    def afterSetUp(self):
        self.js_res_basepath = "++resource++collective.js.prettify.javascripts/"
        self.css_res_basepath = "++resource++collective.js.prettify.stylesheets/"

    def test_portal_js(self):
        pj = getToolByName(self.portal,'portal_javascripts')
        self.failUnless(self.js_res_basepath + 'prettify.js' in pj.getResourceIds(),
                        "prettify.js not found in portal_javascripts")
        self.failUnless(self.js_res_basepath + 'prettyprint.js' in pj.getResourceIds(),
                        "prettyprint.js not found in portal_javascripts")
        
    def test_portal_css(self):
        p_css = getToolByName(self.portal,'portal_css')
        self.failUnless(self.css_res_basepath + 'prettify.css' in p_css.getResourceIds(),
                        "prettify.css not found in portal_css")
        
    def test_js_resources(self):
        for js_name in ['prettify.js','prettyprint.js']:
            try:
                self.portal.restrictedTraverse(self.js_res_basepath + js_name)
            except AttributeError:
                self.fail('%s resource not found' % js_name)
    
    def test_TinyMCE_styles(self):
        self.failUnless("Syntax highlight|pre|prettyprint" in self.portal.portal_tinymce.styles)
        self.failUnless("Syntax high. and linenums|pre|prettyprint linenums:1" in self.portal.portal_tinymce.styles)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
