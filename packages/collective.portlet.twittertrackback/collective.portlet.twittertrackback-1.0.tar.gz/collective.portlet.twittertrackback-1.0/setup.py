from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.portlet.twittertrackback',
      version=version,
      description="A portlet that displays mentions of the current page's url via Topsy",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone twitter topsy portlet',
      author='Matt Hamilton',
      author_email='matth@netsight.co.uk',
      url='http://plone.org/collective.portlet.twittertrackback',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
