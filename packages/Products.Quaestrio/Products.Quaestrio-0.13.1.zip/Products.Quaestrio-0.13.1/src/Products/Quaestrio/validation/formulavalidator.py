from Products.validation.interfaces.IValidator import IValidator
from Products.validation.config import validation
from zope.interface import implements

class FormulaValidator:
    __implements__ = IValidator

    def __init__(self,
                 name,
                 title='Formula Validator',
                 description='Check a quizz formula'):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, vanilla_value, *args, **kwargs):
        import re
        error = None
        value=vanilla_value.replace(' ','')

        #regex_parts={'number':'((([0-9]+(\.[0-9]+)?)|(q[0-9]+))+)','operator':'(\/|\*|-|\+|\^)'}
        regex_parts={'number':'((([0-9]+(\.[0-9]+)?)|(q[0-9]+))+)','operator':'([\/*\-+^])'}
        checks={
            'invalidchars': [
                "^((%(number)s|%(operator)s|\.|\(|\))*)$" % regex_parts,
            ],
            'syntaxerror': [
                "^(\(*(%(number)s%(operator)s)*(\(*%(number)s*(%(operator)s%(number)s*)*\)*)*(%(operator)s%(number)s\)*)*\)*)$" % regex_parts,
                #^| ( |    qn         OP       | (    qn     (    OP         qn     )   )|*       OP       qn      )*|* )      $
            ]
        }
        inverseChecks={
            'syntaxerror': [
                #"%(operator)s(%(operator)s)+" % regex_parts, # double  operator
                "(%(operator)s){2}" % regex_parts, # double  operator
                "^(\(*%(operator)s)" % regex_parts, # check start is not operator
                "%(operator)s\)*$" % regex_parts, # check end is not operator
            ]
        }

        # search the value for containing at least one number
        if not re.search(regex_parts['number'],value) :
            #print "Error Pattern %s is not matched" % pattern
            error='syntaxerror'

        # check syntax
        for i18n_key,patterns in checks.iteritems():
            for pattern in patterns:
                #print "does match: %s" % pattern
                if not re.search(pattern,value) :
                    #print "Error Pattern %s is not matched" % pattern
                    error=i18n_key
                    break

        # negative checks as well
        for i18n_key,patterns in inverseChecks.iteritems():
            for pattern in patterns:
                #print "does not match: %s" % pattern
                if re.search(pattern,value) :
                    #print "Error Pattern %s is matched" % pattern
                    error=i18n_key
                    break

        # check parenthesis match
        if value.count('(') != value.count(')'):
            error = 'parenthesis-not-match'

        if error:
            from Products.CMFCore.utils import getToolByName
            translate = getToolByName(kwargs['instance'], 'translation_service').translate
            error = translate(msgid=error, domain="quaestrio")
        return(error)

validation.register(FormulaValidator('isValidQuizzFormula'))
