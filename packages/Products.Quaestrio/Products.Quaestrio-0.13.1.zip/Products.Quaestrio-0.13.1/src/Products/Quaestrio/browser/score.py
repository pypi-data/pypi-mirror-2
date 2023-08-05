from zope.interface import Interface, implements
from Products.Five import BrowserView

from Products.Quaestrio.interfaces.browser import IQuaestrio_ScoreView

class Quaestrio_ScoreView(BrowserView):
    implements(IQuaestrio_ScoreView)

    def computeScore(self,answers):
        ""
        import re
        # bugfix ^ -> ** for floats in python
        eval_formula = re.sub('(q[0-9]+)','float(%(\\1)s)', self.context.Formula.replace('^','**'))
        try:
            eval_str = eval_formula % answers
            return (True,'%g'%eval(eval_str))
        except (SyntaxError,KeyError):
            from Products.CMFCore.utils import getToolByName
            translate = getToolByName(self.context, 'translation_service').translate
            purl = getToolByName(self.context, 'portal_url')
            error1 = translate(msgid='missingquestion', domain="quaestrio")
            error2 =   translate(msgid='contact', domain="quaestrio")
            link_contact= '<br/><a href="%s/%s">%s</a>' % (purl.getPortalPath(),'contact-info',error2)
            return (False,'<p class="QuaestrioNoItem">%s</p>'%(error1+link_contact))

Quaestrio_ScoreView.__doc__ = IQuaestrio_ScoreView.__doc__
