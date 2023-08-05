from setuptools import setup, find_packages
import os

version = '2.0'

setup(name='mfabrik.like',
      version=version,
      description=" Adds a Facebook Like-button viewlet to Plone content pages. Because everybody loves Facebook (and mFabrik).",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='facebook like plone viewlet',
      author='mFabrik Research Oy',
      author_email='research@mfabrik.com',
      url='http://mfabrik.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mfabrik'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.registry',
          'plone.directives.form'
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )
