# -*- coding: utf-8 -*-
#
__author__ = """Makina <contact@makina-corpus.com>"""
__docformat__ = 'plaintext'

# Python imports
import exceptions

# Zope imports
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from zope.app.annotation.interfaces import IAnnotations

# CMF imports
from Products.CMFCore.utils import getToolByName
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.Archetypes import atapi
from Products.ATContentTypes import atct

# Product imports
from Products.Quaestrio.interfaces.content import IQuaestrio_Quizz
from Products.Quaestrio.config import PROJECTNAME

from Products.Quaestrio.content.schema import schema_quizz

Quaestrio_QuizzSchema = atct.ATFolder.schema.copy() + schema_quizz.copy()
#Quaestrio_QuizzSchema['description'].isMetadata = False
#Quaestrio_QuizzSchema['description'].schemata = 'properties'

 #del Quaestrio_QuizzSchema['description']

class Quaestrio_Quizz(atct.ATFolder):
    """Quaestrio_Quizz"""
    implements(IQuaestrio_Quizz)

    schema = Quaestrio_QuizzSchema

    security = ClassSecurityInfo()

    _at_rename_after_creation = True

Quaestrio_Quizz.__doc__= IQuaestrio_Quizz.__doc__
atapi.registerType(Quaestrio_Quizz, PROJECTNAME)


