from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='Products.googlecoop',
      version=version,
      description="Google Coop for Plone makes it easy for you to integrate a Google Co-op Custom Search engine in your plone site.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Christian Ledermann',
      author_email='christian.ledermann@gmail.com',
      maintainer='Vitaliy Podoba',
      maintainer_email='vitaliypodoba@gmail.com',
      url='http://plone.org/products/google-co-op',
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
      """,
      )
