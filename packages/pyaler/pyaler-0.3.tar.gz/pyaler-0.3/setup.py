from setuptools import setup, find_packages
import sys, os

def read(*names):
    values = dict()
    for name in names:
        filename = name+'.txt'
        if os.path.isfile(filename):
            value = open(name+'.txt').read()
        else:
            value = ''
        values[name] = value
    return values

long_description="""
%(README)s

See http://packages.python.org/pyaler/ for the full documentation

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

version = '0.3'

setup(name='pyaler',
      version=version,
      description="A restfull application to control your arduino devices",
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='arduino http restful api',
      author='Guyzmo, Bearstech',
      author_email='bpratz@bearstech.com',
      url='http://packages.python.org/pyaler/',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'pyserial',
          'pyyaml',
          'bottle',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      pyaler = pyaler.pyaler:main
      [paste.app_factory]
      main = pyaler.pyaler:make_app
      """,
      )
