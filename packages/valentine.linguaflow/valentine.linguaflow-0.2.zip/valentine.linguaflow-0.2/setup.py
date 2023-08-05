from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='valentine.linguaflow',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Sasha Vincic',
      author_email='sasha dot vincic at valentinewebsystems dot com',
      url='http://svn.plone.org/svn/collective/valentine.linguaflow/trunk/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['valentine'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.monkey',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
