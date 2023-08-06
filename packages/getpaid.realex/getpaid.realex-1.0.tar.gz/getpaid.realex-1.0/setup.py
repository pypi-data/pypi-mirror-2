from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='getpaid.realex',
      version=version,
      description="Realex plugin for Plone GetPaid (www.realexpayments.com)",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='getpaid, ecommerce, payment',
      author='Kevin Gill',
      author_email='kevin@movieextras.ie',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['getpaid'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',

          # -*- Extra requirements: -*-
          'five.grok',
          'Products.PloneGetPaid',
          'getpaid.core',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=[],
      paster_plugins = [],

      )
