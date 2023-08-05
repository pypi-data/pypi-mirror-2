from zope.interface import Interface, implements
from Products.Five import BrowserView

from Products.Quaestrio.interfaces.browser import IQuaestrio_QuizzView
from Products.CMFCore.utils import getToolByName


class Quaestrio_QuizzView(BrowserView):
    implements(IQuaestrio_QuizzView)

    def getQuestions(self):
        """"""
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog.searchResults(
            portal_type='Quaestrio_Question',
            path='/'.join(self.context.getPhysicalPath()),
            sort_on='getObjPositionInParent',
            review_state='published',)

        return results

    def getScores(self):
        """"""
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog.searchResults(
            portal_type='Quaestrio_Score',
            path='/'.join(self.context.getPhysicalPath()),
            sort_on='getObjPositionInParent',
            review_state='published',)

        return results


    def hasAnswer(self,questionid):
        """"""
        session_id = 'quizz::%s' % self.context.UID()
        session = self.request.SESSION.get(session_id,{})
        return session.get('answers',{}).has_key(questionid)

    def getAnswer(self,questionid):
        """"""
        session_id = 'quizz::%s' % self.context.UID()
        session = self.request.SESSION.get(session_id,{})
        return session.get('answers',{}).get(questionid,None)

    def getAnswers(self):
        """"""
        session_id = 'quizz::%s' % self.context.UID()
        session = self.request.SESSION.get(session_id,{})
        return session.get('answers',{})

Quaestrio_QuizzView.__doc__ = IQuaestrio_QuizzView.__doc__
