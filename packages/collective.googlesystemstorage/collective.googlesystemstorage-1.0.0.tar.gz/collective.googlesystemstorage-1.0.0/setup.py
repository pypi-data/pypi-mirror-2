from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(name='collective.googlesystemstorage',
      version=version,
      description="GSS saves the document types supported by the Google Docs service on the Google servers",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone google googledocs iw.fss',
      author="D'Elia Federica",
      author_email='federica.delia@redturtle.it',
      url='http://svn.plone.org/svn/collective/collective.googlesystemstorage/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.googleauthentication',
          'iw.fss',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
