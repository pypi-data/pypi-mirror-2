import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = '1.2'

long_description = (
    read('README.txt')
    + '\n' +
    read('docs', 'HISTORY.txt')
#   + '\n' +
#    read('Products', 'SimplePortlet', 'README.txt')
#    + '\n' +
#    read('CONTRIBUTORS.txt')
    )

setup(name='Products.SimplePortlet',
      version=version,
      description="Portlets as content-types",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Plone Foundation',
      author_email='Wouter.VandenHove@UGent.be',
      url='http://svn.plone.org/svn/collective/Products.SimplePortlet',
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

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
