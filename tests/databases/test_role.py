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

class TestRole(unittest.TestCase):

    def test_list(self):
        connection = Connection.make_connection(tc.hostname, tc.admin, tc.password)

        roles = Role.list_roles(connection)

        names = [role.name() for role in roles]
        self.assertGreater(len(names), 65)
        self.assertIn("admin", names)

    def test_lookup(self):
        connection = Connection.make_connection(tc.hostname, tc.admin, tc.password)

        role = Role.lookup("admin", connection)

        self.assertIsNotNone(role)
        self.assertEqual(role.name(), "admin")

    def test_create_role(self):
        new_role = Role("foo-role")

        self.assertEqual(new_role.name(), "foo-role")

        new_role.add_parent_role("admin")
        self.assertIn("admin", new_role.parent_roles())

    def test_description(self):
        role = Role("foo-role")
        role.set_description("This is the foo role")

        self.assertEqual(role.description(), "This is the foo role")

    def test_add_privilege(self):
        role = Role("foo-role")

        name = "foodle"
        action = "http://marklogic.com/xdmp/privileges/foodle"
        kind = "execute"

        role.add_privilege(name, action, kind)

        priv = role.privileges()[0]
        self.assertEqual(priv['privilege-name'], name)
        self.assertEqual(priv['action'], action)
        self.assertEqual(priv['kind'], kind)

    def test_create_remove_role(self):
        connection = Connection.make_connection(tc.hostname, tc.admin, tc.password)
        role = Role("foo-role")

        role.create(connection)

        the_role = Role.lookup("foo-role", connection)
        self.assertIsNotNone(the_role)

        the_role.remove(connection)
        the_role = Role.lookup("foo-role", connection)
        self.assertIsNone(the_role)

    def test_save_role(self):
        connection = Connection.make_connection(tc.hostname, tc.admin, tc.password)
        role = Role("foo-role")

        self.assertIsNone(role.create(connection).description())
        role.set_description("This is the foo role")

        role.save(connection)

        role = Role.lookup("foo-role", connection)
        self.assertEqual("This is the foo role", role.description())

        role.remove(connection)




if __name__ == "__main__":
    unittest.main()