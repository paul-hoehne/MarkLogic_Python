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
# Paul Hoehne       04/03/2015     Initial development
#

import unittest
from marklogic.models import Connection, Role
from resources import TestConnection as tc
from requests.auth import HTTPDigestAuth

class TestRole(unittest.TestCase):

    def test_list(self):
        connection = Connection(tc.hostname, HTTPDigestAuth(tc.admin, tc.password))

        roles = Role.list_roles(connection)

        names = [role.name() for role in roles]
        self.assertGreater(len(names), 65)
        self.assertIn("admin", names)

    def test_lookup(self):
        connection = Connection(tc.hostname, HTTPDigestAuth(tc.admin, tc.password))

        role = Role.lookup("admin", connection)

        self.assertIsNotNone(role)
        self.assertEqual(role.name(), "admin")


if __name__ == "__main__":
    unittest.main()