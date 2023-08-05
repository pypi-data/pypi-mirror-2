from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(name='collective.googlesharing',
      version=version,
      description="GS manages the sharing of documents stored in the Google servers and their synchronization from the Plone application to Google Docs service",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone google googledocs',
      author="D'Elia Federica",
      author_email='federica.delia@redturtle.it',
      url='http://svn.plone.org/svn/collective/collective.googlesharing/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.googleauthentication',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
