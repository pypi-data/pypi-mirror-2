#!/usr/bin/env python

import os
from setuptools import setup, find_packages

version = '0.0.1'


LONG_DESCRIPTION = '''

rcount
=======

Redis-powered counting, comparing, and ranking. It is Part One of a planned trilogy of thin Redis abstraction modules.

rcount is a small abstraction layer over Redis, focused on an abstract counter object. A counter does one thing: it keeps a count. You can increase or decrease the count, and return the value of the counter. Then, you can use your counter objects to do comparisons (which is bigger? by how much? are they equal?) and do rankings (order the counters by their associated integer size).


Full documentation is at http://github.com/tnm/rcount

'''


setup(
    name='rcount',
    version=version,
    description='Redis-powered counting, comparing, and ranking',
    long_description=LONG_DESCRIPTION,
    url='http://github.com/tnm/rcount',
    author='Ted Nyman',
    author_email='tnm800@gmail.com',
    keywords='Redis, counting, increment, ranking data structures',
    license='MIT',
    packages=find_packages(),
    py_modules=['rcount'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
	'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
   ],
)

