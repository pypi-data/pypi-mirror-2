from setuptools import setup, find_packages
import os

version = '3.0'

setup(name='Products.qPloneDropDownMenu',
      version=version,
      description="The product allows Plone websites to update multilevel portal dropdown menu",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dropdown menu',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://quintagroup.com/services/plone-development/products/plone-drop-down-menu',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
