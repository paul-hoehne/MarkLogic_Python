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

__author__ = 'phoehne'

from setuptools import setup, find_packages
setup(
    name="marklogic",
    version="0.0.1",
    packages=["marklogic", "marklogic.models", "marklogic.recipes", "marklogic.tools", "marklogic.models.utilities"],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
        'requests>=2.5.0'
    ],

    include_package_data=True,
    zip_safe=False,
    platforms='any',

    # metadata for upload to PyPI
    author = "Paul Hoehne",
    author_email = "paul.hoehne@marklogic.com",
    description = "MarkLogic package for maintaining servers",
    license = "Apache",
    keywords = "MarkLogic rest management",
    url = "http://github.com/paul-hoehne/MarkLogic_Python/",   # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)