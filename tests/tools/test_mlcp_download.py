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
# Paul Hoehne       03/09/2015     Initial development
#

import unittest
import os
import time
from marklogic.tools import MLCPLoader
from marklogic.models import Connection
from marklogic.recipes import SimpleDatabase
from requests.auth import HTTPDigestAuth

class TestMLCPDownload(unittest.TestCase):

    def setUp(self):
        if os.path.isdir(".mlcp"):
            os.popen("rm -rf .mlcp")

    def test_download(self):
        loader = MLCPLoader()
        loader.clear_directory()

        loader.download_mlcp()
        dir_stat = os.stat(".mlcp")

        self.assertIsNotNone(dir_stat, "There shoudld be an mlcp subdirectory created")

    def test_clear_directory(self):
        os.mkdir(".mlcp")
        loader = MLCPLoader()
        loader.clear_directory()

        self.assertFalse(os.path.isdir(".mlcp"))

    def test_load_data(self):
        simpledb = SimpleDatabase("exmaple_app", port=8400)

        auth = HTTPDigestAuth("admin", "admin")
        conn = Connection("192.168.57.141", auth)

        exampledb = simpledb.create(conn)

        loader = MLCPLoader()
        loader.download_mlcp()

        try:
            loader.load_directory(conn, exampledb[u'content'], "../../examples/data",
                                  collections=["example1"], prefix="/test/data1")
            self.assertIsNotNone(exampledb[u'content'].get_document(conn, "/test/data1/purchases/december/purchase-001.json"))
            self.assertIsNotNone(exampledb[u'content'].get_document(conn, "/test/data1/customer-001.json"))

        finally:
            exampledb[u'server'].remove(conn)
            print("Pausing 15 seconds for server restart")
            time.sleep(15)

            exampledb[u'modules'].remove(conn)
            exampledb[u'content'].remove(conn)
