from setuptools import setup, find_packages
import sys, os

try:
    description = file("README.txt").read()
except IOError:
    description = ''

version = '0.7'

setup(name='decoupage',
      version=version,
      description="Decoupage is the art of decorating an object by gluing colored paper cutouts onto it in combination with special paint effects ... The software decoupage lets you stitch together index pages from filesystem content",
      long_description=description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='http://k0s.org',
      license="GPL",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
         'WebOb',	
         'Paste',
         'PasteScript',
         'genshi',
         'martINI',
         'contenttransformer',
         ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      decoupage-templates = decoupage.templates:main
      decoupage-formatters = decoupage.formatters:main

      [paste.app_factory]
      main = decoupage.factory:factory

      [decoupage.formatters]
      all = decoupage.formatters:All
      css = decoupage.formatters:CSS
      describe = decoupage.formatters:FilenameDescription
      icon = decoupage.formatters:Favicon
      ignore = decoupage.formatters:Ignore
      include = decoupage.formatters:Include
      links = decoupage.formatters:Links
      scripts = decoupage.formatter:JavaScript
      sort = decoupage.formatters:Sort
      title = decoupage.formatters:TitleDescription
      up = decoupage.formatters:Up
      """,
      )
      
