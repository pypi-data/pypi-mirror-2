from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='collective.addthis',
      version=version,
      description="AddThis addon for Plone CMS",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='AddThis',
      author='Jukka Ojaniemi',
      author_email='jukka.ojaniemi@jyu.fi',
      url='http://bitbucket.org/pingviini/collective.addthis/wiki/Home',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
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
