#!/usr/bin/env python
from distutils.core import setup

readme = open('README.txt').read()
conf = dict(
    name='qvikconfig',
    version='0.1.1',
    author='Niels Serup',
    author_email='ns@metanohi.org',
    package_dir={'': '.'},
    py_modules = ['qvikconfig'],
    url='http://metanohi.org/projects/qvikconfig/',
    license='LICENSE.txt',
    description='Read and write simple config files.',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: End Users/Desktop',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Utilities',
                 'License :: DFSG approved',
                 "License :: OSI Approved :: GNU General Public License (GPL)",
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 3.1'
                 ]
)

try:
    # setup.py register wants unicode data..
    conf['long_description'] = readme.decode('utf-8')
    setup(**conf)
except Exception:
    # ..but setup.py sdist upload wants byte data
    conf['long_description'] = readme
    setup(**conf)
