from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.portlet.fblikebox',
      version=version,
      description="Facebook Like-Box Portlet",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Facebook Plone Portlet',
      author='Steve McMahon',
      author_email='steve@dcn.org',
      url='http://svn.plone.org/svn/collective/collective.portlet.fblikebox',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
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
