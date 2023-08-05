from base import ProductTestCase

class TestProductInstall(ProductTestCase):
    def testFormulaValidator(self):
        from Products.Quaestrio.validation import FormulaValidator as validator
        val = validator("myValidator")
        valid_formula=[
            "q4+(q1*q2)+q3",
            "(q1*q2)+q3",
            "q4+(q1*q2)",
            "(q4+(q1*q2))",
            "q0/((q1/100)*(q1/100))",
            "q0/((q1/100)*(q1))",
            "q0/((q1)*(q1/100))",
            "q0/((q1/100)*q1)",
            "q0/(q1*(q1/100))", 
            "q0/(q1/100*q1)",
            "q0/(q1*q1/100)",  
            "(q1*q2)",
            "q1",
            "q12",
            "q1+q2",
            "1-q2",
            "1/q2",
            "1*q2",
            "1+q2",
            "1.2",
            "11.2",
            "11.22",
            "1 1.22",
            "  11.22",
            "1.1+q1",
            "((q0+q1+q2)-200)/10",
        ]
        invalid_formula=[
            "q1++q2",
            "q1.2",
            "1q",
            "q1q",
            "q0/((q1/100)**(q1))",
            "q1+++q2",
            "+q1",
            "q2+",
            "(q2+)",
            "(+q2)",
            "(+q2+)",
            "    ",
           # "((q0+q1+q2)+99999999999999999999999999999999999999999999", #fails atm
        ]
        invalid_chars=["aezr" ,"1+aezr","q1+q2@"]
        for i in valid_formula:
            print "\nWill match: %s" % i
            self.assertEqual(val(i,instance = self.portal) ,None)

        for i in invalid_formula:
            print "\nWont match: %s" % i
            self.failUnless(val(i,instance = self.portal) in (u'syntaxerror' , u'invalidchars'))

        for i in invalid_chars:
            print "\nWont contain: %s" % i
            self.assertEqual(val(i,instance = self.portal) ,u'invalidchars')
            self.assertEqual(val("a(ezr",instance = self.portal) ,u'parenthesis-not-match')

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite

