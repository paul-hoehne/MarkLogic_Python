#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
if '' not in sys.path:
    sys.path.insert(0, '')
import unittest
from tests import all_tests

result = unittest.TextTestRunner(verbosity=2).run(all_tests())

if result.wasSuccessful():
    sys.exit(0)
else:
    sys.exit(1)
