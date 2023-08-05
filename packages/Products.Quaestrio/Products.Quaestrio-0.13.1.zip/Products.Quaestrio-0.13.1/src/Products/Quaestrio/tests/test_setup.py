from base import ProductTestCase

class TestProductInstall(ProductTestCase):
    """"""
    def testTypesInstalled(self):
        types = ('Quaestrio_Quizz','Quaestrio_Score','Quaestrio_Question',)
        for t in types:
            self.failUnless(t in self.portal.portal_types.objectIds(), '%s content type not installed' % t)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite


#value="profile-Products.AntiCancerDocuments:default"
