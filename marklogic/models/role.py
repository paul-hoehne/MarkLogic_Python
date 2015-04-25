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
# Paul Hoehne       04/02/2015     Initial development
#

import requests
from marklogic.models.utilities import exceptions
import json


class Role(object):
    def __init__(self, name):
        self.config = {}
        self.config['role-name'] = name

    def name(self):
        """
        Return the name of the role.

        :return:The role name
        """
        return self.config['role-name']

    def create(self, connection):
        """
        Creates the Role on the MarkLogic server.

        :param connection: The connection to a MarkLogic server
        :return: The Role object
        """
        uri = "http://{0}:{1}/manage/v2/roles".format(connection.host, connection.management_port)

        response = requests.post(uri, json=self.config, auth=connection.auth)
        if response.status_code not in [200, 201, 204]:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)

        return self

    def save(self, connection):
        uri = "http://{0}:{1}/manage/v2/roles/{2}/properties".format(connection.host, connection.management_port,
                                                                     self.config[u'role-name'])
        response = requests.put(uri, json=self.config, auth=connection.auth)

        if response.status_code not in [200, 204]:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)

        return self

    def remove(self, connection):
        uri = "http://{0}:{1}/manage/v2/roles/{2}".format(connection.host, connection.management_port,
                                                          self.config[u'role-name'])
        response = requests.delete(uri, auth=connection.auth)

        if response.status_code not in [200, 204] and not response.status_code == 404:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)

        return self

    def add_parent_role(self, role_name):
        """
        Add a parent role to given role

        :param role_name: The name of the parent role
        :return: The role object
        """
        if "role" not in self.config:
            self.config['role'] = [role_name]
        else:
            self.config['role'].append(role_name)
        return self

    def parent_roles(self):
        """
        Returns the parent roles

        :return:The list of roles
        """
        if "role" not in self.config:
            return None
        return self.config['role']

    def set_description(self, description):
        """
        Set the description for the role

        :param description: A description for the role
        :return:The role object
        """
        self.config['description'] = description
        return self

    def description(self):
        """
        Returns the description for the role.

        :return:The role description
        """
        if 'description' not in self.config:
            return None
        return self.config['description']

    def add_privilege(self, name, action, kind):
        """
        Add a new privilege to the list of role privileges.

        :param name: The name of the privilege
        :param action: The action
        :param kind: The kind of permission
        :return:The role object
        """
        if 'privilege' not in self.config:
            self.config['privilege'] = [
                {'privilege-name': name, 'action': action, 'kind': kind}
            ]
        else:
            self.config['privilege'].append({
                'privilege-name': name, 'action': action, 'kind': kind
            })
        return self

    def privileges(self):
        """
        Returns the privileges for a given role

        :return:The list of privileges
        """
        if 'privilege' not in self.config:
            return None
        return self.config['privilege']


    @classmethod
    def list_roles(cls, connection):
        """
        List all the roles in the security database.

        :param connection:The connection to a MarkLogic server
        :return:A list of Roles
        """

        uri = "http://{0}:{1}/manage/v2/roles".format(connection.host, connection.port)
        response = requests.get(uri, auth=connection.auth, headers={'accept': 'application/json'})

        if response.status_code != 200:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)

        results = []
        json_doc = json.loads(response.text)

        for item in json_doc['role-default-list']['list-items']['list-item']:
            temp = Role("temp")
            role_uri = "http://{0}:{1}{2}/properties".format(connection.host, connection.port, item['uriref'])

            response = requests.get(role_uri, auth=connection.auth, headers={'accept': 'application/json'})
            if response.status_code != 200:
                raise exceptions.UnexpectedManagementAPIResponse(response.text)

            temp.config = json.loads(response.text)
            results.append(temp)

        return results


    @classmethod
    def lookup(cls, name, connection):
        """
        Look up an individual role from the security database.

        :param name: The name of the role
        :param connection: The connection to the MarkLogic database
        :return: The role
        """
        uri = "http://{0}:{1}/manage/v2/roles/{2}/properties".format(connection.host, connection.port,
                                                                     name)
        response = requests.get(uri, auth=connection.auth, headers={'accept': 'application/json'})

        if response.status_code == 200:
            result = Role("temp")
            result.config = json.loads(response.text)
            return result
        elif response.status_code == 404:
            return None
        else:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)
