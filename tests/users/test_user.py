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
# Norman Walsh      05/01/2015     Initial development
#

import unittest
from marklogic.models import Connection, Role
from resources import TestConnection as tc

class TestUser(unittest.TestCase):

    def test_list(self):
        connection = Connection.make_connection(tc.hostname, tc.admin, tc.password)

        users = User.list_users(connection)

        names = [user.name() for user in users]
        self.assertGreater(len(names), 2)
        self.assertIn("nobody", names)

    def test_lookup(self):
        connection = Connection.make_connection(tc.hostname, tc.admin, tc.password)

        user = User.lookup("nobody", connection)

        self.assertIsNotNone(user)
        self.assertEqual(user.name(), "nobody")

    def test_create_user(self):
        new_user = User("foo-user")

        self.assertEqual(new_user.name(), "foo-user")

        new_user.create(connection)

        users = User.list_users(connection)

        names = [user.name() for user in users]
        self.assertIn("foo-user", names)

    def test_description(self):
        user = User("foo-user")
        user.set_description("This is the foo user")

        self.assertEqual(user.description(), "This is the foo user")

    def test_add_role(self):
        user = User("foo-user")

        user.add_role(u'manage-user')

        role = user.roles_names()[0]
        self.assertEqual(u'manage-user', role)

    def test_create_remove_user(self):
        connection = Connection.make_connection(tc.hostname, tc.admin, tc.password)
        user = User("foo-user")

        user.create(connection)

        the_user = User.lookup("foo-user", connection)
        self.assertIsNotNone(the_user)

        the_user.remove(connection)
        the_user = User.lookup("foo-user", connection)
        self.assertIsNone(the_user)

    def test_save_user(self):
        connection = Connection.make_connection(tc.hostname, tc.admin, tc.password)
        user = User("foo-user")

        self.assertIsNone(user.create(connection).description())
        user.set_description("This is the foo user")

        user.save(connection)

        user = User.lookup("foo-user", connection)
        self.assertEqual("This is the foo user", user.description())

        user.remove(connection)

if __name__ == "__main__":
    unittest.main()
