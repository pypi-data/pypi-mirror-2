import unittest
from Products.CMFCore.utils import getToolByName
from Products.PFGVerkkomaksut.tests.base import PFGVerkkomaksutTestCase

class TestSetup(PFGVerkkomaksutTestCase):

    def afterSetUp(self):
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.types = getToolByName(self.portal, 'portal_types')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.content_types = [
            'PFGVerkkomaksut',
        ]
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.skins      = getToolByName(self.portal, 'portal_skins')
        self.properties = getToolByName(self.portal, 'portal_properties')
        self.site_properties = getattr(self.properties, 'site_properties')
        self.navtree_properties = getattr(self.properties, 'navtree_properties')

    def test_is_pfg_installed(self):
        self.failUnless(self.installer.isProductInstalled('PloneFormGen'))

    def test_is_pfg_verkkomaksut_installed(self):
        self.failUnless(self.installer.isProductInstalled('PFGVerkkomaksut'))

    def testSkinLayersInstalled(self):
        self.failUnless('PFGVerkkomaksut' in self.skins.objectIds())

    ## Content Types
    def test_contents_installed(self):
        for type in self.content_types:
            self.failUnless(type in self.types.objectIds())

#    def test_add_PFGVerkkomaksut(self):
#        self.setRoles(('Manager',))
#        self.portal.invokeFactory('FormFolder', 'form')
#        form = self.portal.form
#        form.invokeFactory(
#            'FormFixedPointField',
#            'fixed_point_field',
#            title = 'Fixed Point Price',
#            required = True,
#        )
#        fpf = form.fixed_point_field
#        fpf_uid = fpf.UID()
#        form.invokeFactory(
#            'PFGVerkkomaksut',
#            'adapter',
##            title = 'Verkkomaksut Adapter',
##            price_field = fpf_uid,
##            thanks_text = '<p>Thanks!!</p>',
##            cancel_message = 'Order Canceled',
##            recipient_email = 'recipient@abita.fi',
#        )

    ## site_properties
    def test_not_searchable(self):
        self.failUnless('PFGVerkkomaksut' in self.site_properties.getProperty('types_not_searched'))

    def test_use_folder_tabs(self):
        self.failUnless('PFGVerkkomaksut' not in self.site_properties.getProperty('use_folder_tabs'))

    def test_typesLinkToFolderContentsInFC(self):
        self.failUnless('PFGVerkkomaksut' not in self.site_properties.getProperty('typesLinkToFolderContentsInFC'))

    ## navtree_properties
    def test_not_in_navtree(self):
        self.failUnless('PFGVerkkomaksut' in self.navtree_properties.getProperty('metaTypesNotToList'))

    # Workflow
    def test_workflow(self):
        self.assertEquals((), self.wftool.getChainForPortalType('PFGVerkkomaksut'))

    def test_workflow_mapped(self):
        for portal_type, chain in self.wftool.listChainOverrides():
            if portal_type in ('PFGVerkkomaksut'):
                self.assertEquals((), chain)
            if portal_type in ('File', 'Image'):
                self.assertEquals((), chain)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
