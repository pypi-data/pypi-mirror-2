from base import ProductTestCase

testfolder="testfolder"

class TestProductInstall(ProductTestCase):
    def testAddQuizz(self):
        #self.loginAsPortalOwner()
        self.setRoles(('Manager',))
        types={}
        #container
        for portal_type in ['Quaestrio_Quizz']:
            types[portal_type] = self.folder.invokeFactory(portal_type, id='1')
            #acontained
        for i,portal_type in enumerate(['Quaestrio_Question','Quaestrio_Score']):
            types[portal_type] = self.folder[types['Quaestrio_Quizz']].invokeFactory(portal_type, id=i)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite

