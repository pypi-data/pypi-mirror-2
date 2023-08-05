## Script (Python) "resetQuaestrioQuestionsForm"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Efface les questions répondues par l'utilisateur
##

from Products.CMFCore.utils import getToolByName
portal_url = getToolByName(context, 'portal_url')
t= getToolByName(context, 'anticancer_members_tool')
catalog= getToolByName(context, 'portal_catalog')
portal = portal_url.getPortalObject()

request = container.REQUEST
session = request.SESSION
SESSION_KEY ="quizz::%s"% context.UID()

quizz_name = request.get('quizz_name', None)
if quizz_name:
    session_items=session.get(SESSION_KEY,{})
    if session_items.has_key('answers'):
        del session_items['answers']
    session.set(SESSION_KEY, session_items)
    translate = getToolByName(context, 'translation_service').translate
    er = translate(msgid='erasedanswers', domain="quaestrio")
    pm = getToolByName(context, 'plone_utils')
    pm.addPortalMessage((er))
return state

# vim: set ft=python :
