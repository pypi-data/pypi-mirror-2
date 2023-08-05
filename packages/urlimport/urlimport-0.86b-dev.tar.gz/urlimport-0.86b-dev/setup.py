#coding: utf-8

from setuptools import setup, find_packages
import sys, os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def readlines(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).readlines()

pyversion = sys.version_info[0] * 10 + sys.version_info[1]

setup(name='urlimport',
      version=[l for l in readlines('changelog') if l.strip() and not l.lstrip().startswith('#')][0].split()[0][1:],
      description="Allow importing files through the web, by adding urls to pythopath",
      long_description=read('README'),
      platforms='ALL',
      keywords='python import remote modules http https ftp perforce',
      author='Jure Vrscaj, 송영진(MyEvan), Alex Bodnaru',
      author_email='jure@codeshift.net, myevan_net@naver.com, alexbodn@012.net.il',
      maintainer='alex bodnaru',
      maintainer_email='alexbodn@012.net.il',
      url='http://packages.python.org/urlimport',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'server_side', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          "pysqlite"
      ] if pyversion < 25 else [],
      entry_points="""
      # -*- Entry points: -*-
      """,
      # not yet there ;)
      #test_suite = 'nose.collector',
      classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2", # as of now
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Communications",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
      ],
)

