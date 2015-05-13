#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
if '' not in sys.path:
    sys.path.insert(0, '')
import unittest
from tests import all_tests, privilege_tests, forest_tests, database_tests
from tests import server_tests, tools_tests

unittest.TextTestRunner(verbosity=2).run(all_tests())
