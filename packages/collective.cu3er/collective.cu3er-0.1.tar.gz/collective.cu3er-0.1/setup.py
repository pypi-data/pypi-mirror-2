from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.cu3er',
      version=version,
      description="CU3ER integration for Plone",
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings
      # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Zope Plone JavaScrip Slideshow CU3ER Viewlet',
      author='Thomas Massmann',
      author_email='thomas.massmann@inqbus.de',
      url='http://svn.plone.org/svn/collective/collective.cu3er',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'archetypes.schemaextender',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
