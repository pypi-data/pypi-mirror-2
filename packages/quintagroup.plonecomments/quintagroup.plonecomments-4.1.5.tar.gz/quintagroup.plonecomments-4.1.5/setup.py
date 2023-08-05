from setuptools import setup, find_packages
import os

version = '4.1.5'

setup(name='quintagroup.plonecomments',
      version=version,
      description="Plone Comments",
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web zope plone theme',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://quintagroup.com/services/plone-development/products/plone-comments',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['quintagroup'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )
