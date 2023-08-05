from setuptools import setup, find_packages
import os

version = '1.0b1'

setup(name='z3c.appconfig',
      version=version,
      description="Simple application configuration system",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='http://svn.plone.org/svn/collective/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['z3c'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
          "zope.interface",
          "zope.component [zcml]",
      ],
      )
