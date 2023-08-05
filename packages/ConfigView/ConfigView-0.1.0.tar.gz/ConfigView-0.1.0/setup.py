#! /usr/bin/env python

from distutils.core import setup

# use README file as long_description
readme = open('README')
long_description = readme.read()
readme.close()


setup(name = 'ConfigView',
      description = 'visualize and manipulate (sets of hierarchal) config files',
      version = '0.1.0',
      license = 'MIT',
      author = 'Eduardo Naufel Schettino',
      author_email = 'schettino72@gmail.com',
      url = 'http://bitbucket.org/schettino72/configview/',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Environment :: Console',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Operating System :: POSIX',
                     'Programming Language :: Python :: 2.5',
                     'Programming Language :: Python :: 2.6',
                     'Topic :: Software Development',
                     ],

      packages = ['configview'],
      scripts = ['bin/confview'],
      long_description = long_description,

      install_requires = ['configdict', 'html'],
      )

