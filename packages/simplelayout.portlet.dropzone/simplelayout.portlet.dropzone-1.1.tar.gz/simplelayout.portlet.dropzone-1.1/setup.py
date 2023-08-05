from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='simplelayout.portlet.dropzone',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Mathias LEIMGRUBER (4teamwork)',
      author_email='m.leimgruber@4teamwork.ch',
      url='http://plone.org/products/simplelayout.portlet.dropzone',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['simplelayout', 'simplelayout.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.portlets',
          'simplelayout.base'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
