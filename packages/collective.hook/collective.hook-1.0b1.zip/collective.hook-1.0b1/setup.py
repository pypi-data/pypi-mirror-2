from setuptools import setup, find_packages
import os

version = '1.0b1'

setup(name='collective.hook',
      version=version,
      description="A very simple hook system for zope application by Makina-Corpus.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='JeanMichel FRANCOIS aka toutpt',
      author_email='toutpt@makina-corpus.org',
      url='http://svn.plone.org/svn/collective/collective.hook',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.schema',
          'zope.event',
          'zope.interface',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
