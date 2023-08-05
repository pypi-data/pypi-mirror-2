# -*- coding: utf-8 -*-

__author__ = """Makina <contact@makina-corpus.com>"""
__docformat__ = 'plaintext'

# CMF imports
from Products.Archetypes import atapi
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Quaestrio import validation

schema_quizz = atapi.Schema(
    (
        atapi.TextField(
            name='Quizz',
            allowable_content_types=( 'text/html', ),
            default_content_type = 'text/html',
            default_output_type  = 'text/html',
            required=1,
            widget=atapi.RichWidget(
                rows=10,
                label_msgid='label_QuizzText',
                i18n_domain='quaestrio',
            )
        ),
        atapi.TextField(
            name='questions_widget',
            allowable_content_types=( 'text/html', ),
            default_content_type = 'text/html',
            default_output_type  = 'text/html',
            vocabulary = ('radioButtons','selectList'),
            widget=atapi.SelectionWidget(
                format='select',
                size='20',
                label_msgid='label_questions_widget',
                i18n_domain='quaestrio',
            )
        ),
    ),
)

schema_question = atapi.Schema (
    (
        atapi.TextField(
            name='Question',
            allowable_content_types=( 'text/html', ),
            default_content_type = 'text/html',
            default_output_type  = 'text/html',
            required=1,
            widget=atapi.RichWidget(
                rows=10,
                label_msgid='label_QuestionText',
                i18n_domain='quaestrio',
            )
        ),
        atapi.IntegerField(
            name='Valmin',
            required=1,
            widget=atapi.StringWidget(
                size = '4',
                maxlength = '4',
                label_msgid='label_valmin',
                i18n_domain='quaestrio',
            ),
        ),
        atapi.StringField(
            name='DescValmin',
            widget=atapi.StringWidget(
                size = '80',
                maxlength = '80',
                label_msgid='label_DescValmin',
                i18n_domain='quaestrio',
            ),
        ),
        atapi.IntegerField(
            name='Valmax',
            required=1,
            widget=atapi.IntegerWidget(
                size = '4',
                maxlength = '4',
                label_msgid='label_valmax',
                i18n_domain='quaestrio',
            ),
        ),
        atapi.StringField(
            name='DescValmax',
            widget=atapi.StringWidget(
                size = '80',
                maxlength = '80',
                label_msgid='label_DescValmax',
                i18n_domain='quaestrio',
            ),
        ),
),
)

schema_score = atapi.Schema(
    (
        atapi.TextField(
            name='Score',
            allowable_content_types=( 'text/html', ),
            default_content_type = 'text/html',
            default_output_type  = 'text/html',
            required=1,
            widget=atapi.RichWidget(
                rows=10,
                label_msgid='label_ScoreText',
                i18n_domain='quaestrio',
            )
        ),
        atapi.StringField(
            name='Formula',
            required=1,
            validators = ('isValidQuizzFormula',),
            widget=atapi.StringWidget(
                size = '80',
                maxlength = '80',
                label_msgid='label_Formula',
                description_msgid='help_Formula',
                i18n_domain='quaestrio',
            ),
        ),
    ),
)


