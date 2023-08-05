from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.tabr',
      version=version,
      description="A simple package to add jQuery Tools Tabs UI support to Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Michael Dunlap',
      author_email='dunlapm@uw.edu',
      url='http://svn.plone.org/svn/collective/collective.tabr/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.jquerytools'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
