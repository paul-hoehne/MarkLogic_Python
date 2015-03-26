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
# Paul Hoehne       03/26/2015     Initial development
#

import unittest
import os
from marklogic.models import Connection, Host
from requests.auth import HTTPDigestAuth


class TestHost(unittest.TestCase):
    def setUp(self):
        """
        TODO: Might need to move this a common parent class.

        Check to see that the following enviornment variables are set to run tests:
        o  MLHOST  - the name of the MarkLogic server
        o  MLADMIN - the admin user of the MarkLogic server
        o  MLPASS  - the admin user password.

        It defaults to 'localhost' for the host, and admin/admin for the
        username/passwrd.
        """
        if 'MLHOST' in os.environ:
            self._hostname = os.environ['MLHOST']
        else:
            self._hostname = 'localhost'
            print("No MLHOST environment variable - using 'localhost'")

        if 'MLADMIN' in os.environ:
            self._admin = os.environ['MLADMIN']
        else:
            self._admin = 'admin'
            print("No MLADMIN environment variable - using 'admin'")

        if 'MLPASS' in os.environ:
            self._password = os.environ['MLPASS']
        else:
            self._password = 'admin'
            print("No MLPASS environment variable - using 'admin'")

    def test_list_hosts(self):
        conn = Connection(self._hostname, HTTPDigestAuth(self._admin, self._password))

        hosts = Host.list_hosts(conn)
        assert len(hosts) > 0

        assert hosts[0] is not None