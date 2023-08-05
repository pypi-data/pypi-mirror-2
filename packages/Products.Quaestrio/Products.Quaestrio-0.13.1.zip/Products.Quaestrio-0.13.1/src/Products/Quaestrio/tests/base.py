# Let Zope know about the two products we require above-and-beyond a basic
# Plone install (PloneTestCase takes care of these).
from Products.Quaestrio.config import PROJECTNAME
from Testing import ZopeTestCase
from Products.Five import zcml
from Products import Quaestrio 
ZopeTestCase.installProduct('Five') 
ZopeTestCase.installProduct(PROJECTNAME)
#zcml.xmlconfig('configure.zcml',Quaestrio) 
# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

# Set up a Plone site, and apply the extension profiles
# to make sure they are installed.
setupPloneSite(products=("Five",PROJECTNAME, ),extension_profiles=('Products.%s:default' % PROJECTNAME, ) )

class ProductTestCase(PloneTestCase):
    """Base class for integration tests for the 'Quaestrio' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """
