from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='experimental.daterangeindexoptimisations',
      version=version,
      description="A patch to Zope2's DateRangeIndexes to store data more efficiently",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone performance indexing daterangeindex catalog speedups',
      author='Matt Hamilton',
      author_email='matth@netsight.co.uk',
      url='https://svn.plone.org/svn/collective/experimental.daterangeindexoptimisations',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['experimental'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
