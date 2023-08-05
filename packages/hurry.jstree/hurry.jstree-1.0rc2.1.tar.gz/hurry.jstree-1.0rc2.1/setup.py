from setuptools import setup, find_packages
import os

JSTREE_VERSION = '1.0rc2'
version = '1.0rc2.1'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

setup(name='hurry.jstree',
      version=version,
      description="hurry.resource resources for JsTree",
      long_description=long_description,
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Martijn Faassen /Izhar Firdaus',
      author_email='faassen@startifact.com',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['hurry'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'hurry.resource >= 0.10',
          'hurry.jquery',
      ],
      entry_points={
       'hurry.resource.libraries': [
        'jstree = hurry.jstree:jstree_lib',
       ],
      }
      )
