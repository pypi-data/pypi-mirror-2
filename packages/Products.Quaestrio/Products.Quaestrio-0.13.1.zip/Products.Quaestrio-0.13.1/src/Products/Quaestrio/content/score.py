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

# Product imports
from Products.Quaestrio.interfaces.content import IQuaestrio_Score
from Products.Quaestrio.config import PROJECTNAME
from Products.Quaestrio.content.schema import schema_score

Quaestrio_ScoreSchema = atapi.BaseContent.schema.copy() + schema_score.copy()

class Quaestrio_Score(atapi.BaseContent):
    """Quaestrio_Score"""
    implements(IQuaestrio_Score)

    schema = Quaestrio_ScoreSchema

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

Quaestrio_Score.__doc__ = IQuaestrio_Score.__doc__
atapi.registerType(Quaestrio_Score, PROJECTNAME)
