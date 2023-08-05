from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.cssgridsystem',
      version=version,
      description="960CSS And Blue print packaged as zope browser resource",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='css zope plone',
      author='JeanMichel FRANCOIS aka toutpt',
      author_email='toupt@gmail.com',
      url='http://svn.plone.org/svn/collective/collective.cssgridsystem',
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

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
