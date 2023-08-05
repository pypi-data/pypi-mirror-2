from setuptools import setup, find_packages
import os

version = '1.0.0'

setup(name='Products.PloneboardPasteObject',
      version=version,
      description="fix for Ploneboard that allow you paste into some Ploneboard's archetypes",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturlte.it',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.Ploneboard',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
