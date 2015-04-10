# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import os
import unittest

tests_directory = os.path.dirname(os.path.abspath(__file__))

def all_tests():
    """Making the standard tests suite using auto discovery suitable to
    "run_tests.py" and "python setup.py test".
    """
    return unittest.defaultTestLoader.discover(tests_directory)
