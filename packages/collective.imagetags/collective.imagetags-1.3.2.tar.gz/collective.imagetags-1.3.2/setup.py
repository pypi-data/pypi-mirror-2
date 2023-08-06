from setuptools import setup, find_packages
import os

version = '1.3.2'

setup(name='collective.imagetags',
      version=version,
      description="Adds Facebook-like tags (or Flickr-like notes) to images",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read()  + "\n" +
                       open(os.path.join("docs", "AUTHORS.txt")).read()  + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Marcos F. Romero',
      author_email='marcos.romero {at} inter-cultura {dot} com',
      url='http://svn.plone.org/svn/collective/collective.imagetags',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.js.jqueryui',
          'plone.app.registry',
          'simplejson',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
