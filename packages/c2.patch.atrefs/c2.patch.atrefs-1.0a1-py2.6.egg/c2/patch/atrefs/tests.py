#!/usr/bin/env python
# encoding: utf-8

from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
import time
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

@onsetup
def setup_plone():
    fiveconfigure.debug_mode = True
    import c2.patch.atrefs
    fiveconfigure.debug_mode = False
    
setup_plone()

PRODUCTS = []
PloneTestCase.setupPloneSite(products=PRODUCTS)

class C2PatchAtRefsTestCase(PloneTestCase.PloneTestCase):
    """ """
    class Session(dict):
        def set(self, key, value):
            self[key] = value
    
    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()


now = DateTime()

class TestReference(C2PatchAtRefsTestCase):
    """  """
    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.workflow = self.portal.portal_workflow
        self.portal.invokeFactory('Document', 'doc1')
        self.doc1 = getattr(self.portal, 'doc1')
        
        self.portal.invokeFactory('Document', 'doc2')
        self.doc2 = getattr(self.portal, 'doc2')
        self.doc2.setRelatedItems([self.doc1.UID()])
        self.doc2.reindexObject()
    
    def test_refes(self):
        self.workflow.doActionFor(self.doc2, 'publish')
        self.doc2.reindexObject()
        self.logout()
        r1 = self.doc2.getRefs()
        self.assertEqual(len(r1), 1)
        r2 = self.doc2.getSecureRefs()
        self.assertEqual(len(r2), 0)
        self.login()
        self.workflow.doActionFor(self.doc1, 'publish')
        self.doc1.reindexObject()
        self.logout()
        r3 = self.doc2.getSecureRefs()
        self.assertEqual(len(r3), 1)
        self.login()

    def test_brefs(self):
        self.workflow.doActionFor(self.doc1, 'publish')
        self.doc1.reindexObject()
        self.logout()
        r1 = self.doc1.getBRefs()
        self.assertEqual(len(r1), 1)
        r2 = self.doc1.getSecureBRefs()
        self.assertEqual(len(r2), 0)
        self.login()
        self.workflow.doActionFor(self.doc2, 'publish')
        self.doc2.reindexObject()
        self.logout()
        r3 = self.doc1.getSecureBRefs()
        self.assertEqual(len(r3), 1)
        self.login()
    
    def test_refs_date(self):
        self.workflow.doActionFor(self.doc1, 'publish')
        self.workflow.doActionFor(self.doc2, 'publish')
        self.doc1.setEffectiveDate(now + 1)
        self.logout()
        r1 = self.doc2.getRefs()
        self.assertEqual(len(r1), 1)
        r2 = self.doc2.getSecureRefs()
        self.assertEqual(len(r2), 0)
        self.login()
        self.doc1.setEffectiveDate(now - 1)
        self.logout()
        r3 = self.doc2.getSecureRefs()
        self.assertEqual(len(r3), 1)
        self.login()
        self.doc1.setExpirationDate(now - 1)
        self.logout()
        r4 = self.doc2.getSecureRefs()
        self.assertEqual(len(r4), 0)
        self.login()

    def test_brefs_date(self):
        self.workflow.doActionFor(self.doc1, 'publish')
        self.workflow.doActionFor(self.doc2, 'publish')
        self.doc2.setEffectiveDate(now + 1)
        self.logout()
        r1 = self.doc1.getBRefs()
        self.assertEqual(len(r1), 1)
        r2 = self.doc1.getSecureBRefs()
        self.assertEqual(len(r2), 0)
        self.login()
        self.doc2.setEffectiveDate(now - 1)
        self.logout()
        r3 = self.doc1.getSecureBRefs()
        self.assertEqual(len(r3), 1)
        self.login()
        self.doc2.setExpirationDate(now - 1)
        self.logout()
        r4 = self.doc1.getSecureBRefs()
        self.assertEqual(len(r4), 0)
        self.login()

class TestSortedReference(C2PatchAtRefsTestCase):
    """  """
    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.workflow = self.portal.portal_workflow
        self.portal.invokeFactory('Document', 'doc1')
        self.doc1 = getattr(self.portal, 'doc1')
        self.workflow.doActionFor(self.doc1, 'publish')
        self.doc1.reindexObject()

        time.sleep(2)
        self.portal.invokeFactory('Document', 'doc2')
        self.doc2 = getattr(self.portal, 'doc2')
        self.doc2.setRelatedItems([self.doc1.UID()])
        self.workflow.doActionFor(self.doc2, 'publish')
        self.doc2.reindexObject()

        time.sleep(2)
        self.portal.invokeFactory('Document', 'doc3')
        self.doc3 = getattr(self.portal, 'doc3')
        self.doc3.setRelatedItems([self.doc2.UID(), self.doc1.UID()])
        self.workflow.doActionFor(self.doc3, 'publish')
        self.doc3.reindexObject()

    def test_refes(self):
        self.logout()
        r2 = self.doc2.getSortedSecureRefs()
        self.assertEqual(len(r2), 1)

        r3 = self.doc3.getSortedSecureRefs()
        self.assertEqual(len(r3), 2)
        # print getattr(self.doc1, "Date", lambda:"No Date")()
        # print getattr(self.doc2, "Date", lambda:"No Date")()
        # print self.doc1.id, r3[0].id, r3[1].id
        self.assertEqual(self.doc1.UID(), r3[0].UID())
        
        r4 = self.doc3.getSortedSecureRefs(order='reverse')
        self.assertEqual(len(r4), 2)
        self.assertEqual(self.doc1.UID(), r4[1].UID())

        self.doc1.setTitle("abcd")
        self.doc1.reindexObject()
        r5 = self.doc3.getSortedSecureRefs(sort_key="modified")
        self.assertEqual(len(r5), 2)
        self.assertEqual(self.doc1.UID(), r5[1].UID())

        r6 = self.doc3.getSortedSecureRefs(sort_key="modified", order='reverse')
        self.assertEqual(len(r6), 2)
        self.assertEqual(self.doc1.UID(), r6[0].UID())

        r7 = self.doc3.getSortedSecureRefs(sort_key='getId', order='reverse')
        self.assertEqual(len(r7), 2)
        self.assertEqual(self.doc1.UID(), r7[1].UID())

        r8 = self.doc3.getSortedSecureRefs(sort_key='Non key')
        self.assertEqual(len(r8), 2)
        self.assertEqual(self.doc1.UID(), r8[1].UID())

        r9 = self.doc3.getSortedSecureRefs(sort_key='getObjPositionInParent')
        self.assertEqual(len(r9), 2)
        self.assertEqual(self.doc1.UID(), r9[0].UID())

class TestSortedBReference(C2PatchAtRefsTestCase):
    """  """
    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.workflow = self.portal.portal_workflow
        self.portal.invokeFactory('Document', 'doc1')
        self.doc1 = getattr(self.portal, 'doc1')
        self.workflow.doActionFor(self.doc1, 'publish')
        self.doc1.reindexObject()

        time.sleep(2)
        self.portal.invokeFactory('Document', 'doc2')
        self.doc2 = getattr(self.portal, 'doc2')
        self.doc2.setRelatedItems([self.doc1.UID()])
        self.workflow.doActionFor(self.doc2, 'publish')
        self.doc2.reindexObject()

        time.sleep(2)
        self.portal.invokeFactory('Document', 'doc3')
        self.doc3 = getattr(self.portal, 'doc3')
        self.doc3.setRelatedItems([self.doc2.UID(), self.doc1.UID()])
        self.workflow.doActionFor(self.doc3, 'publish')
        self.doc3.reindexObject()

    def test_brefs(self):
        self.logout()
        r1 = self.doc2.getSortedSecureBRefs()
        self.assertEqual(len(r1), 1)

        r2 = self.doc1.getSortedSecureBRefs()
        self.assertEqual(len(r2), 2)
        self.assertEqual(self.doc2.UID(), r2[0].UID())
        
        r3 = self.doc1.getSortedSecureBRefs(order='reverse')
        self.assertEqual(len(r3), 2)
        self.assertEqual(self.doc2.UID(), r3[1].UID())

        self.doc2.setTitle("abcd")
        self.doc2.reindexObject()
        r5 = self.doc1.getSortedSecureBRefs(sort_key="modified")
        self.assertEqual(len(r5), 2)
        self.assertEqual(self.doc2.UID(), r5[1].UID())

        r6 = self.doc1.getSortedSecureBRefs(sort_key="modified", order='reverse')
        self.assertEqual(len(r6), 2)
        self.assertEqual(self.doc2.UID(), r6[0].UID())

        r7 = self.doc1.getSortedSecureBRefs(sort_key='getId', order='reverse')
        self.assertEqual(len(r7), 2)
        self.assertEqual(self.doc2.UID(), r7[1].UID())

        r8 = self.doc1.getSortedSecureBRefs(sort_key='Non key')
        self.assertEqual(len(r8), 2)
        self.assertEqual(self.doc2.UID(), r8[0].UID())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestReference))
    suite.addTest(makeSuite(TestSortedReference))
    suite.addTest(makeSuite(TestSortedBReference))
    return suite