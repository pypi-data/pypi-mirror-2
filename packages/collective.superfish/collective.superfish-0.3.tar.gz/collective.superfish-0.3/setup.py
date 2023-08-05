# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from xml.dom.minidom import parse

def readversion():
    mdfile = os.path.join(os.path.dirname(__file__), 'collective', 'superfish', 
                          'profiles', 'default', 'metadata.xml')
    metadata = parse(mdfile)
    assert metadata.documentElement.tagName == "metadata"
    return metadata.getElementsByTagName("version")[0].childNodes[0].data

def read(*pathnames):
    return open(os.path.join(os.path.dirname(__file__), *pathnames)).read()

setup(name='collective.superfish',
      version=readversion().strip(),
      description="A suckerfish/superfish integration into plone",
      long_description='\n'.join([
        read('docs', 'README.txt'),
        read('docs', 'TODO.txt'),
        read('docs', 'HISTORY.txt'),
        read('docs', 'THANKS.txt'),
      ]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='navigation suckerfish superfish jquery dropdown',
      author='Daniel Widerin',
      author_email='daniel.widerin@kombinat.at',
      url='http://svn.plone.org/svn/collective/collective.superfish',
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
      # -*- Entry points: -*-
      """,
      )
