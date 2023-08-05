from setuptools import setup, find_packages
import os

version = '0.0.7'

setup(name='prdg.util',
      version=version,
      description='General utilities.',
      long_description='\n'.join([
        open('README.txt').read(),
        open('TODO.txt').read(),
        open('HISTORY.txt').read()
      ]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='util utils',
      author='Rafael Oliveira',
      author_email='rafaelbco@gmail.com',
      url='http://code.google.com/p/prdg-python/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['prdg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'rbco.commandwrap<=0.0.99',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
