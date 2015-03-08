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

from marklogic.models import Connection, Database, FieldRange, Field, FieldReference
from requests.auth import HTTPDigestAuth

auth = HTTPDigestAuth("admin", "admin")

conn = Connection("192.168.57.141", auth)

db = Database("range-field-test", "localhost.localdomain")
field = Field("test-field", includes=[FieldReference("http://foo.bar.com/invoice", "id")])
db.add_field(field)
db.add_index(FieldRange("test-field", "int"))

db.create(conn)