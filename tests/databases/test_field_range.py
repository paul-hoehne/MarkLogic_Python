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
# Paul Hoehne       03/05/2015     Initial development
#

import unittest

from marklogic.models import FieldRange, Field, Database, FieldReference

# "fields": {
#     "field": [
#         {
#             "field-name": "invoice-id",
#             "field-path": [
#                 {
#                     "path": "bill:invoice-id",
#                     "weight": 1
#                 },
#                 {
#                     "path": "inv:id",
#                     "weight": 1
#                 }
#             ],
#             "word-lexicons": null,
#             "included-elements": null,
#             "excluded-elements": null,
#             "tokenizer-overrides": null
#         }
#     ]
# },

class TestField(unittest.TestCase):

    def test_create_field(self):
        db = Database("testdb")

        self.assertNotIn(u'fields', db.config)

        field = Field("invoice-id")
        field.add_path("bill:invoice-id", 1)
        field.add_path("inv:id", 1)

        result = db.add_field(field)
        self.assertIn(u'fields', db.config)
        self.assertEqual(result, db)

        self.assertEqual(1, len(db.config[u'fields']))
        self.assertEqual("invoice-id", db.config[u'fields'][0].name())

        field = db.fields(0)
        self.assertEqual(2, len(field.paths()))
        self.assertEqual("bill:invoice-id", field.paths(0)[u'path'])
        self.assertEqual(1, field.paths()[0][u'weight'])

    def test_include_references(self):
        db = Database("testdb")

        field = Field("invoice-id", includes=[FieldReference("http://foo.bar.com/invoice", "id")])

        self.assertEqual(1, len(field.includes()))
        self.assertEqual("http://foo.bar.com/invoice", field.includes(0).namespace_uri())
        self.assertEqual("id", field.includes(0).localname())

    def test_exclude_references(self):
        db = Database("testdb")

        field = Field("invoice-id", excludes=[FieldReference("http://foo.bar.com/invoice", "id")])

        self.assertEqual(1, len(field.excludes()))
        self.assertEqual("http://foo.bar.com/invoice", field.excludes(0).namespace_uri())
        self.assertEqual("id", field.excludes(0).localname())


    def test_create_field_reference(self):
        element_reference = FieldReference("http://foo.bar.com/invoice", "id")

        self.assertEqual("http://foo.bar.com/invoice", element_reference.namespace_uri())
        self.assertEqual("id", element_reference.localname())

        element_reference = FieldReference("http://foo.bar.com/invoice", "id", attribute_name="foo")
        self.assertEqual("foo", element_reference.attribute_name())

        element_reference = FieldReference("http://foo.bar.com/invoice", "id",
                                           attribute_namespace="http://foo.bar.com/billing",
                                           attribute_name="bill")
        self.assertEqual("http://foo.bar.com/billing", element_reference.attribute_namespace())

    #
    # {
    #   "scalar-type": "int",
    #   "collation": "",
    #   "field-name": "test-one",
    #   "range-value-positions": false,
    #   "invalid-values": "reject"
    # }
    #
    def test_create_field_range(self):
        db = Database("foo")

        field = Field("invoice-id")
        db.add_field(field)

        field_range = FieldRange("invoice-id", "int")
        db.add_index(field_range)

        index = db.field_range_index(0)
        self.assertEqual("invoice-id", index.name())
        self.assertEqual("int", index.type())

        indexes = db.field_range_index()
        self.assertEqual(1, len(indexes))
