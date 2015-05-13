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

def privilege_tests():
    """Just the privilege tests.
    """
    return unittest.defaultTestLoader.discover(tests_directory + "/privileges")

def forest_tests():
    """Just the forest tests.
    """
    return unittest.defaultTestLoader.discover(tests_directory + "/forests")

def database_tests():
    """Just the database tests.
    """
    return unittest.defaultTestLoader.discover(tests_directory + "/databases")

def server_tests():
    """Just the server tests.
    """
    return unittest.defaultTestLoader.discover(tests_directory + "/servers")

def tools_tests():
    """Just the tools tests.
    """
    return unittest.defaultTestLoader.discover(tests_directory + "/tools")
