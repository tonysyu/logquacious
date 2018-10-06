#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import re
from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


def find_version():
    with open('logquacious/__init__.py') as init_file:
        version_file = init_file.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


requirements = [
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'coverage',
    'flake8',
    'manuel',
    'mock',
    'pytest',
    'pytest-cov',
    'pytest-flake8',
    'pytest-sugar',
]

doc_requirements = [
    'sphinx',
    'sphinx-autobuild',
    'sphinx_rtd_theme',
    'sphinxcontrib-napoleon',
]

dev_requirements = [
    'bumpversion',
    'ipdb',
    'ipython',
    'twine',
    'wheel',
] + test_requirements + doc_requirements

setup(
    author="Tony S Yu",
    author_email='tsyu80@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Logging utilities to help you over-communicate",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='logquacious',
    name='logquacious',
    packages=find_packages(include=['logquacious']),
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require={
        'dev': dev_requirements,
        'docs': doc_requirements,
    },
    url='https://github.com/tonysyu/logquacious',
    version='0.3.0',
    zip_safe=False,
)
