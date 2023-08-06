#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="redsolutioncms",
    version=__import__('redsolutioncms').__version__,
    description=read('DESCRIPTION'),
    license="LGPL",
    keywords="django news",

    author="Alexander Ivanov, Ivan Gromov",
    author_email="src@redsolution.ru",

    maintainer='Ivan Gromov',
    maintainer_email='ivan.gromov@redsolution.ru',

    url="http://www.redsoluthioncms.org",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
    ],
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
    long_description=read('README'),
    entry_points={
        'console_scripts': ['redsolutioncms=redsolutioncms.loader:main'],
    }
)
