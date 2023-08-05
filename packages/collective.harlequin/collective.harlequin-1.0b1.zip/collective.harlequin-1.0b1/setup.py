from setuptools import setup, find_packages
import os

version = '1.0b1'

setup(name='collective.harlequin',
      version=version,
      description="System based on annotation to make a configurable browser view by Makina Corpus.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='zope plone',
      author='JeanMichel FRANCOIS aka toutpt',
      author_email='jeanmichel.francois@makina-corpus.com',
      url='http://svn.plone.org/svn/collective/collective.harlequin',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.z3cform',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
