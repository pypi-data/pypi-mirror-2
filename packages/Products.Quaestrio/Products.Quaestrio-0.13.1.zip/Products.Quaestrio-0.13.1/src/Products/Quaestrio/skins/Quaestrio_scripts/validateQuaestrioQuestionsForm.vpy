## Script (Python) "validateQuaestrioQuestionsForm"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Valide les questions répondues par l'utilisateur
##

from Products.CMFCore.utils import getToolByName
portal_url = getToolByName(context, 'portal_url')
t= getToolByName(context, 'anticancer_members_tool')
catalog= getToolByName(context, 'portal_catalog')
portal = portal_url.getPortalObject()

request = container.REQUEST
session = request.SESSION
SESSION_KEY = 'quizz::%s' % context.UID()

quizz_name = request.get('quizz_name', None)
if quizz_name:
    session_items=session.get(SESSION_KEY,{})
    questions=request.get('questions',{})
    answers=session_items.get('answers',{})
    results = catalog.searchResults(
        portal_type='Quaestrio_Question',
        path=context.getPhysicalPath(),
        sort_index='getObjPositionInParent',
        review_state='published',)

    for question_id,question_brain in enumerate(results):
        qt = 'q%s' % question_id
        answer=questions.get(qt,None)
        if not answer:
            state.setError(qt, 'QuaestrioQuestionNotAnswered', new_status='failure')
        else:
            try:
                value = int(answer)
                answers[qt]=value
                # verify range
                question = question_brain.getObject()
                # range can be inversed
                valmin=question.Valmin
                valmax=question.Valmax
                if question.Valmax<question.Valmin:
                    valmin=question.Valmax
                    valmax=question.Valmin

                if not( valmax >= answers[qt]) and not( answers[qt] >= valmin):
                    del answers[qt]
                    state.setError(qt, 'QuaestrioQuestionNotValid %s %s %s'%(valmin,valmax,1), new_status='failure')
                # save into the inner session dictionnary
                session_items['answers']=answers

            except ValueError:
                state.setError(qt, 'QuaestrioQuestionNotValid', new_status='failure')

    #t.pdb([question_brain,answers,questions])
    #save into session
    session.set(SESSION_KEY, session_items)
return state
# vim: set ft=python :
