from setuptools import setup, find_packages
import os

version = '0.13.1'

setup(name='Products.Quaestrio',
      version=version,
      description="A quizz product sponsorised by Makina Corpus",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone guerir.fr',
      author='Mathieu Pasquet',
      author_email='mpa@makina-corpus.com',
      url='https://svn.plone.org/svn/collective/Products.Quaestrio',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'':'src'},
      package_data={'src': ['Products'], 'docs':['*.txt','*.GPL']},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
