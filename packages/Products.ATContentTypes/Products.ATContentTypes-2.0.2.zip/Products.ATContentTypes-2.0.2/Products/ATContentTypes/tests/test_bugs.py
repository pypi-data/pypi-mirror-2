from Testing import ZopeTestCase # side effect import. leave it here.
from Products.ATContentTypes.tests import atcttestcase
from Products.validation.interfaces.IValidator import IValidationChain
from Products.ATContentTypes.content.schemata import ATContentTypeSchema

from Products.Archetypes.atapi import *

tests = []

class TestBugs(atcttestcase.ATCTSiteTestCase):

    def afterSetUp(self):
        atcttestcase.ATCTSiteTestCase.afterSetUp(self)
        self.wf = self.portal.portal_workflow

    def test_wfmapping(self):
        default = ('simple_publication_workflow',)

        mapping = {
            'Document' : default,
            'Event' : default,
            'File' : (),
            'Folder' : default,
            'Image' : (),
            'Link' : default,
            'News Item' : default,
            'Topic' : default,
            }

        for pt, wf in mapping.items():
            pwf = self.wf.getChainFor(pt)
            self.failUnlessEqual(pwf, wf, (pt, pwf, wf))

    def test_striphtmlbug(self):
        # Test for Plone tracker #4944
        self.folder.invokeFactory('Document', 'document')
        d = getattr(self.folder, 'document')
        d.setTitle("HTML end tags start with </ and end with >")
        self.assertEqual(d.Title(), "HTML end tags start with </ and end with >")
    
    def test_dt2DT2dtTZbug(self):
        # Tests problems with conversion between datetime and DateTime becoming naive of timezones
        import DateTime
        from Products.ATContentTypes.utils import DT2dt,dt2DT
        PartyBST = DateTime.DateTime("2007-07-19 20:00 GMT+0100")
        PartyUTC = DateTime.DateTime("2007-07-19 19:00 GMT+0000")
        PartyEDT = DateTime.DateTime("2007-07-19 15:00 GMT-0400")
        self.assertEqual(PartyUTC, PartyBST)
        self.assertEqual(PartyUTC, PartyEDT)
        partyUTC = DT2dt(PartyUTC)
        self.assertEqual(str(dt2DT(partyUTC)), str(PartyUTC))
        partyEDT = DT2dt(PartyEDT)
        self.assertEqual(str(dt2DT(partyEDT)), str(PartyEDT))
        partyBST = DT2dt(PartyBST)
        self.assertEqual(str(dt2DT(partyBST)), str(PartyBST))
        self.assertNotEqual(str(dt2DT(partyEDT)), str(PartyBST))
        self.assertNotEqual(str(dt2DT(partyUTC)), str(PartyBST))
        self.assertNotEqual(str(dt2DT(partyEDT)), str(PartyUTC))

    def test_validation_layer_from_id_field_from_base_schema_was_initialized(self):
        field = ATContentTypeSchema['id']
        self.failUnless(IValidationChain.providedBy(field.validators))


tests.append(TestBugs)

import unittest
def test_suite():
    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(unittest.makeSuite(test))
    return suite
