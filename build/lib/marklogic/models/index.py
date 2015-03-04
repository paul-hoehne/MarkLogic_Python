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

__author__ = 'phoehne'

from .utilities.validators import validate_index_type, validate_boolean, validate_index_invalid_value_actions


class ElementRange:
    def __init__(self, localname, scalar_type=u'string', namespace_uri=None, collation=None,
                 range_value_positions=False, invalid_values=u'reject'):
        validate_index_type(scalar_type)
        validate_boolean(range_value_positions)
        validate_index_invalid_value_actions(invalid_values)

        self.config = {
            u"scalar-type": scalar_type,
            u'namespace-uri': '',
            u"localname": localname,
            u'collation': u'',
            u"range-value-positions": range_value_positions,
            u"invalid-values": invalid_values
        }
        if namespace_uri:
            self.config[u'namespace-uri'] = namespace_uri
        if collation:
            self.config[u'collation'] = collation


class RangeElementAttribute:
    def __init__(self, element_name, attribute_name, scalar_type=u'string', element_namespace=None,
                 attribute_namespace=None, collation=None, range_value_positions=False, invalid_values=u'reject'):
        validate_index_type(scalar_type)
        validate_boolean(range_value_positions)
        validate_index_invalid_value_actions(invalid_values)

        self.config = {
            u"scalar-type": scalar_type,
            u'collation': u'',
            u'parent-namespace-uri': u'',
            u"parent-localname": element_name,
            u'namespace-uri': u'',
            u"localname": attribute_name,
            u"range-value-positions": range_value_positions,
            u"invalid-values": invalid_values
        }

        if collation:
            self.config[u'collation'] = collation
        if element_namespace:
            self.config[u'parent-namespace-uri'] = element_namespace
        if attribute_namespace:
            self.config[u'namespace-uri'] = attribute_namespace