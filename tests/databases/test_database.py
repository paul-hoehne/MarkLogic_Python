# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

#
# Copyright 2015 MarkLogic Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
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
# Paul Hoehne       03/25/2015     Initial development
# Paul Hoehne       03/26/2015     Adding dynamic lookup of host name
#

import unittest
import os
from marklogic.models import Database, Connection, Host
from requests.auth import HTTPDigestAuth
from resources import TestConnection as tc

class TestDatabase(unittest.TestCase):
    """
    Basic creation test function.

    """

    def test_simple_create(self):
        """
        TODO: The hostname should come from the server's hostname

        Test the basic create function.  Creates a database and then check to see that it
        exists by getting the database configuration from the server.  It then destroys
        the database.

        :return: None
        """
        conn = Connection(tc.hostname, HTTPDigestAuth(tc.admin, tc.password))
        hosts = Host.list_hosts(conn)
        db = Database("test-db", hosts[0].host_name())

        db.create(conn)

        validate_db = Database.lookup("test-db", conn)
        try:
            self.assertIsNotNone(validate_db)
            self.assertEqual('test-db', validate_db.database_name())

        finally:
            validate_db.remove(conn)
            validate_db = Database.lookup("test-db", conn)
            self.assertIsNone(validate_db)

    def test_no_database_found(self):
        conn = Connection(tc.hostname, HTTPDigestAuth(tc.admin, tc.password))
        db = Database.lookup("No-Such-Database", conn)

        self.assertIsNone(db)
