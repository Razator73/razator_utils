#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#") and not line.startswith("-r")]


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = parse_requirements('requirements/prod.txt')
test_requirements = parse_requirements('requirements/test.txt')

setup(
    author="Ryan Scott",
    author_email='ryan.t.scott73@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    description="A pypi package for personal use. Containing common functions I use.",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='razator_utils',
    name='razator_utils',
    packages=find_packages(include=['razator_utils', 'razator_utils.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/razator73/razator_utils',
    version='0.3.0',
    zip_safe=False,
)
