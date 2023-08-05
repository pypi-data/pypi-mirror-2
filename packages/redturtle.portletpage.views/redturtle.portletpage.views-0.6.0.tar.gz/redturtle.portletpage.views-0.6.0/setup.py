from setuptools import setup, find_packages
import os

version = '0.6.0'

setup(name='redturtle.portletpage.views',
      version=version,
      description="Additional views for Plone collective.portletpage product",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='portlet view portletpage',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.net',
      url='http://plone.org/products/redturtle.portletpage.views',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redturtle', 'redturtle.portletpage'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.portletpage',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
