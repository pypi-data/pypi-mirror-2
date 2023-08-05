from setuptools import setup, find_packages
import os

version = '0.4'

setup(name='uwosh.northstar',
      version=version,
      description="Provide a better mechanism to create and manage workflows for Plone TTW.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='workflow uwosh plone manager ajax',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='https://141.233.238.172/svn/plone/Projects/uwosh.northstar',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['uwosh'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.jquerytools'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
