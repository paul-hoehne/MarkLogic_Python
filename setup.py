#
# Copyright 2015 MarkLogic Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0#
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Note that this code was taken from an example on using PyPi.
#

import os
from setuptools import setup, find_packages

__author__ = 'phoehne'


def _long_description():
    """A long reStructuredText description for PiPI
    """
    this_directory = os.path.dirname(os.path.abspath(__file__))
    parts = []
    for name in ('README.rst', 'CONTRIBUTING.rst', 'CHANGES.rst'):
        parts.append(open(os.path.join(this_directory, name), 'r').read().strip())
    return '\n\n'.join(parts)

setup(
    name="marklogic",
    version="0.0.1",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests>=2.5.0'
    ],
    include_package_data=True,
    zip_safe=False,
    platforms='any',

    # Metadata for upload to PyPI
    author="Paul Hoehne",
    author_email="paul.hoehne@marklogic.com",
    description="MarkLogic package for maintaining servers",
    long_description=_long_description(),
    license="Apache",
    keywords="MarkLogic rest management",
    classifiers=[
        # Valid classifiers:
        # https://pypi.python.org/pypi?%3Aaction=list_classifiershttps://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Database :: Front-Ends"
    ],
    url="https://github.com/paul-hoehne/MarkLogic_Python/",   # project home page, if any

    # Others
    test_suite='tests.all_tests'
)
