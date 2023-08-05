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
from Products.Archetypes import atapi
from Products.ATContentTypes import atct

# Product imports
from Products.Quaestrio.interfaces.content import IQuaestrio_Question
from Products.Quaestrio.content.schema import schema_question
from Products.Quaestrio.config import PROJECTNAME

Quaestrio_QuestionSchema = atapi.BaseContent.schema.copy() + schema_question.copy()

class Quaestrio_Question(atapi.BaseContent):
    """Quaestrio_Question"""
    schema = Quaestrio_QuestionSchema

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    implements(IQuaestrio_Question)

Quaestrio_Question.__doc__ = IQuaestrio_Question.__doc__
atapi.registerType(Quaestrio_Question, PROJECTNAME)
