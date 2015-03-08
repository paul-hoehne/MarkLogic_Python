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
# Paul Hoehne       03/01/2015     Initial development
#

from .utilities.validators import validate_index_type, validate_boolean, validate_index_invalid_value_actions, \
    validate_custom


class ElementRange:
    """
    Defines an element range index.
    """
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


class ElementAttributeRange:
    """
    Defines an element attribute range index
    """
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


class FieldRange:
    def __init__(self, name, type):
        self.config = {
            u'field-name': name,
            u'scalar-type': type,
            u'range-value-positions': False,
            u'invalid-values': "reject",
            u'collation': ''
        }

    def name(self):
        return self.config[u'field-name']

    def type(self):
        return self.config[u'scalar-type']


class FieldReference:
    """
    Encapsulates a field reference when working with fields.

    """
    def __init__(self, namespace_uri, local_name, attribute_name=None, attribute_namespace=None):
        self.config = {
            u'namespace-uri': namespace_uri,
            u'localname': local_name,
            u'weight': 1
        }
        if attribute_namespace and not attribute_name:
            raise validate_custom("Unable to create field reference with an attribute namespace but no attribute name")
        if attribute_name:
            self.config[u'attribute-name'] = attribute_name
        if attribute_namespace:
            self.config[u'attribute-namespace'] = attribute_namespace


    def namespace_uri(self):
        return self.config[u'namespace-uri']

    def localname(self):
        return self.config[u'localname']

    def attribute_name(self):
        if u'attribute-name' in self.config:
            return self.config[u'attribute-name']
        return None

    def attribute_namespace(self):
        if u'attribute-namespace' in self.config:
            return self.config[u'attribute-namespace']
        return None



class Field:
    """
    Defines a field usable in a field range index
    """
    def __init__(self, name, includes=None, excludes=None):
        self.config = {
            u'field-name': name,
            u'include-root': True,
            u'tokenizer-overrides': None
        }
        if includes is not None:
            self.config[u'included-element'] = []
            for include in includes:
                self.config[u'included-element'].append(include.config)

        if excludes is not None:
            self.config[u'excluded-element'] = []
            for exclude in excludes:
                self.config[u'excluded-element'].append(exclude.config)


    def add_path(self, path, weight):
        """
        Add a new path to the field description

        :param path: The document path
        :param weight: The weight assigned to that path
        :return: The field object
        """
        if u'paths' not in self.config:
            self.config[u'paths'] = []

        if u'include-root' in self.config:
            del self.config[u'include-root']


        self.config[u'paths'].append({u'path': path, u'weight': weight})
        return self

    def paths(self, path_idx=None):
        """
        Returns the list of paths defined for this field.

        :param path_idx: The index of the path
        :return:The list of paths
        """
        if u'paths' not in self.config:
            return None
        if path_idx and  path_idx >= len(self.config[u'paths']):
            return None
        if path_idx is None:
            return self.config[u'paths']
        return self.config[u'paths'][path_idx]

    def name(self):
        """
        Returns the field name.

        :return:The field name
        """
        return self.config[u'field-name']

    def includes(self, idx=None):
        """
        Returns the included elements in a field or a a specific element.

        :param idx: The optional index of the included element
        :return:Either all elements or, if an index is provided, a specific element
        """
        if idx is None:
            if u'included-element' in self.config:
                result = []
                for element in self.config[u'included-element']:
                    temp = FieldReference("", "")
                    temp.config = element
                    result.append(temp)
                return result
        elif idx < len(self.config[u'included-element']):
            result = FieldReference("", "")
            result.config = self.config[u'included-element'][idx]
            return result
        return None

    def excludes(self, idx=None):
        """
        Returns the excluded elements or a specific excluded element.

        :param idx: The optional index of the excluded element
        :return:Either all elements or, if an index is provided, the specific element.
        """
        if idx is None:
            if u'excluded-element' in self.config:
                result = []
                for element in self.config[u'excluded-element']:
                    temp = FieldReference("", "")
                    temp.config = element
                    result.append(temp)
                return result
        elif idx < len(self.config[u'excluded-element']):
            result = FieldReference("", "")
            result.config = self.config[u'excluded-element'][idx]
            return result
        return None