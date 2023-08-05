from zope.interface import Interface, implements
from Products.Five import BrowserView

from Products.Quaestrio.interfaces.browser import IQuaestrio_QuestionView

class Quaestrio_QuestionView(BrowserView):
    implements(IQuaestrio_QuestionView)

Quaestrio_QuestionView.__doc__ = IQuaestrio_QuestionView.__doc__

