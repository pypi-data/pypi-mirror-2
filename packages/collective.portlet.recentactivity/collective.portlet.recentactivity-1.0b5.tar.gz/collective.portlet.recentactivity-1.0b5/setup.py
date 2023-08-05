from setuptools import setup, find_packages
import os

version = '1.0b5'

setup(name='collective.portlet.recentactivity',
      version=version,
      description="Recent activity portlet for Plone.",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Timo Stollenwerk',
      author_email='timo@zmag.de',
      url='http://svn.plone.org/svn/collective/collective.portlet.recentactivity',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
