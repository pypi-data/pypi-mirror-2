from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='delicious_links',
      version=version,
      description="Daily links publishing from Delicious to Wordpress",
      long_description="""Daily links publishing from Delicious to Wordpress""",
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Topic :: Utilities"
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='delicious wordpress',
      author='Maksym Kozlenko',
      author_email='max@kozlenko.info',
      url='http://www.kozlenko.info',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
