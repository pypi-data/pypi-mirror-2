from setuptools import setup, find_packages
import sys, os

version = '0.6'

setup(name='delicious_links',
      version=version,
      description="Daily links publishing from Delicious to Wordpress",
      long_description=
        """Uses Delicious API to get a list of links for user with specified tag and 
          publishes these links grouped by category into Wordpress blog using XMLRPC. 
          Please check project page on Google Code for usage example""",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Topic :: Utilities"
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='delicious wordpress',
      author='Maksym Kozlenko',
      author_email='max@kozlenko.info',
      url='http://code.google.com/p/deliciouslinks/',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=["feedparser", "httplib2"],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
