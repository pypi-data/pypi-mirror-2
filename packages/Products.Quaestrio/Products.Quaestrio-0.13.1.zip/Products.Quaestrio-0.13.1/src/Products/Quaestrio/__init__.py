# -*- coding: utf-8 -*-
#
__author__ = """Makina <contact@makina-corpus.com>"""
__docformat__ = 'plaintext'

# Python imports
import logging

# Zope imports
from AccessControl import allow_module

# plone
from Products.CMFCore.utils import ContentInit
from Products.CMFCore.DirectoryView import registerDirectory

# archetype
from Products.Archetypes.atapi import process_types, listTypes

# project
from permissions import DEFAULT_ADD_CONTENT_PERMISSION, ADD_CONTENT_PERMISSIONS
from config import PROJECTNAME, GLOBALS, SKINS_DIRS


# logger
logger = logging.getLogger(PROJECTNAME)
logger.info('Installing Product')

# Register skins directory
for skins_dir in SKINS_DIRS:
    registerDirectory(skins_dir, GLOBALS)

# Initialize product
def initialize(context):

    allow_module('Products.Quaestrio.utils')
    
    from Products.Quaestrio.content import Quaestrio_Quizz, Quaestrio_Question, Quaestrio_Score
    
    contentTypes, constructors, ftis = process_types(listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        '%s %s' % (PROJECTNAME,'Content'),
        content_types      = contentTypes,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
    ).initialize(context)

    for i in range(0, len(contentTypes)):
        klassname = contentTypes[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue
        context.registerClass(meta_type    = ftis[i]['meta_type'],
                              constructors = (constructors[i],),
                              permission   = ADD_CONTENT_PERMISSIONS[klassname])
