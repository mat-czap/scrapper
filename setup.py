# -*- coding: utf8 -*-
#

#

import os

from setuptools import setup, find_packages

# Meta information
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)


setup(
    # Basic info
    name='scrapper',
    version=version,
    author='Mateusz Czaprański',
    author_email='czapranski.mateusz@gmail.com',
    url='https://github.com/fabiommendes/python-boilerplate',
    description='Creates the skeleton of your Python project.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    extras_require={
        'dev': [
            'manuel',
            'pytest',
            'pytest-cov',
            'coverage',
            'mock',
        ],
    },

    # Data files
    package_data={
        'python_boilerplate': [
            'templates/*.*',
            'templates/license/*.*',
            'templates/docs/*.*',
            'templates/package/*.*'
        ],
    },

    # Scripts
    entry_points={
        'console_scripts': [
            'python-boilerplate = ludos.__main__:main'],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)


