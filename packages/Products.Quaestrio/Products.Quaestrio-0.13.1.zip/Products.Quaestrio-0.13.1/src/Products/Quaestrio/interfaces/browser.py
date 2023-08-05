# -*- coding: utf-8 -*-

from zope import interface

class IQuaestrio_QuestionView(interface.Interface):
    """browser view for question content-type """


class IQuaestrio_QuizzView(interface.Interface):
    """browser view for quizz content-type """

    def getQuestions():
        """ get questions in the current quizz folder"""

    def getScores():
        """ get scores in the current quizz folder"""

    def hasAnswer(self,questionid):
        """if a question has entry in the session, return true"""

    def getAnswer(self,questionid):
        """if a question has entry in the session, return its value"""

    def getAnswers(self):
        """if there are questions in the session, return questions dict"""

class IQuaestrio_ScoreView(interface.Interface):
    """browser view for score content-type """

    def computeScore(self,answers): 
        """ Compute the score by applying answers inside the score formula
        - answers: answers dict. eg {'q1':1,'q3':3}
        Returns a tuple : (First,Second)
            * First : False: error True: score is valid
            * Second : Error / Score
        """

