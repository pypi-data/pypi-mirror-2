from setuptools import setup, find_packages
import os

version = '1.2'

setup(name='collective.subscribemember',
      version=version,
      description="A tool to allow users to subscribe to a Plone site and pay their membership fees.",
      long_description=open(os.path.join("collective", "subscribemember", "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='plone remember membrane plonegetpaid subscription membership',
      author='Tim Knapp',
      author_email='tim@emergetec.com',
      url='http://www.emergetec.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.remember',
          'testfixtures',
          'functools',
          'archetypes.schemaextender'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
