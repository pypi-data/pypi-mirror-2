from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='niteoweb.clickbank',
      version=version,
      description="Integrates ClickBank digital products retailer system with Plone for paid memberships.",
      long_description=open("README.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone clickbank',
      author='NiteoWeb Ltd.',
      author_email='info@niteoweb.com',
      url='http://svn.plone.org/svn/collective/niteoweb.clickbank',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['niteoweb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
