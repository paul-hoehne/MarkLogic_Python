# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

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
# File History
# ------------
#
# Paul Hoehne       03/28/2015     Initial development
#

import unittest
from marklogic.models import Forest
from marklogic.models.utilities.validators import ValidationError

class TestForest(unittest.TestCase):
    def test_forest_defaults(self):
        pass

    def test_getters_and_setters(self):
        forest = Forest("Foo")

        self.assertEqual(forest.name(), "Foo")

        forest.set_availability("offline")
        self.assertEqual("offline", forest.availability())

        with self.assertRaises(ValidationError):
            forest.set_availability("foo")

        forest.set_host("bar")
        self.assertEqual("bar", forest.host())

        forest.set_data_directory("/foo/bar")
        self.assertEqual("/foo/bar", forest.data_directory())

        forest.set_database("foo")
        self.assertEqual("foo", forest.database())

        forest.set_fast_data_directory("/foo/bar")
        self.assertEqual("/foo/bar", forest.fast_data_directory())

        forest.set_large_data_directory("/foo/bar")
        self.assertEqual("/foo/bar", forest.large_data_directory())