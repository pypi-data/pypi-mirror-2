from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='twisted.scheduling',
      version=version,
      description="A scheduling plugin for twisted",
      long_description=open(os.path.join("docs", "README")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Twisted",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
      keywords='twisted python scheduling cron',
      author='Texas A&M University Library',
      author_email='webmaster@library.tamu.edu',
      maintainer='Benjamin Liles',
      maintainer_email='bliles@library.tamu.edu',
      url='http://code.google.com/p/meercat',
      packages=find_packages(),
      namespace_packages=['twisted'],
      test_suite = 'twisted.scheduling.tests.test_suite',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Twisted>=8',
          'zope.interface',
      ])
