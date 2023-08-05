from distutils.core import setup, Extension

spam = Extension('spam',
                 sources = ['spam.c'])

setup (name = 'PackageCSystem',
       version = '1.0',
       description = 'This is a package to invoke some c code',
       ext_modules = [spam])

