#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='johbo-pytest-sqlalchemy',
    version='0.1.0',
    description="SQLAlchemy integration fow py.test with automatic test database creation.",
    long_description=readme + '\n\n' + history,
    author="Johannes Bornhold",
    author_email='johannes@bornhold.name',
    url='https://github.com/johbo/johbo-pytest-sqlalchemy',
    packages=[
        'johbo_pytest_sqlalchemy',
    ],
    package_dir={'johbo_pytest_sqlalchemy':
                 'johbo_pytest_sqlalchemy'},
    include_package_data=True,
    install_requires=requirements,
    license="TODO",
    zip_safe=False,
    keywords='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points = {
        'pytest11': [
            'johbo_pytest_sqlalchemy = johbo_pytest_sqlalchemy.pytest_plugin',
        ]
    },
)
