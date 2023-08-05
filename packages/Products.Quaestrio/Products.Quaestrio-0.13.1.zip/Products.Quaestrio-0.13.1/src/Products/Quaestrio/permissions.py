# -*- coding: utf-8 -*-
#
__author__ = """Makina <contact@makina-corpus.com>"""
__docformat__ = 'plaintext'



from AccessControl.Permissions import add_user_folders as AddUserFolders
from Products.CMFCore.permissions import setDefaultRoles

# Basic permissions
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.permissions import ListFolderContents
from Products.CMFCore.permissions import SetOwnPassword as SetPassword
from Products.CMFCore.permissions import ManageUsers


from config import PROJECTNAME

# Add permissions
AddQuizz    = "%s: %s" % (PROJECTNAME,"Add Quizz")
AddQuestion = "%s: %s" % (PROJECTNAME,"Add Question")
AddScore    = "%s: %s" % (PROJECTNAME,"Add Score")

for perm in [AddQuizz ,AddQuestion, AddScore]:
    setDefaultRoles(perm, ('Manager',))

DEFAULT_ADD_CONTENT_PERMISSION = AddPortalContent
ADD_CONTENT_PERMISSIONS = {
    'Quaestrio_Quizz'    : AddQuizz,
    'Quaestrio_Question' : AddQuestion,
    'Quaestrio_Score'    : AddScore,
}
