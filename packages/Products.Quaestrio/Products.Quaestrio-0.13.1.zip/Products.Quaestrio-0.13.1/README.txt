COMPATIBILITY
=============
- PLONE 3.x

ABSTRACT
=========
- Quaestrio is a product that enables you to create small quizzes inside plone.
- The use case:

    - You can enter a quizz
    - This quizz will contain questions & scores.

.. contents::

Makina Corpus sponsorised software
======================================
|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

INSTALL
=======
    - Drop it into your zope products directory
    - You can also see the profile files to adapt them to your needs.
    - Apply the queastrio profil extension

USAGE
======
Adding a quizz
---------------
    - Add a quizz
    - inside:

        - add questions with their answer from lower one to upper one
        - add score(s)
        - publsh them

            - Be ware that the questions begin their count at 'q0'

Filling a quizz
---------------
    - Open the quizz page
    - Fill all the questions
    - Your quizz ends up when all the questions are answered.
    - The scores with the computed formulas will appear.


AUTHORS
=======
    - Mathieu PASQUET <mpa@makina-corpus.com>

LICENSE
========
    - see docs/LICENSE.txt


