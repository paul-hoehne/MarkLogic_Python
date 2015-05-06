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
# Norman Walsh      04/29/2015     Hacked role.py into user.py
#

import requests
from marklogic.models.utilities import exceptions
import json

class User(object):
    def __init__(self, name):
        self.config = {}
        self.config['user-name'] = name

    def name(self):
        """
        Return the name of the user.

        :return:The user name
        """
        return self.config['user-name']

    def set_name(self, name):
        """
        Set the name of the user.

        :return:The user object
        """
        self.config['user-name'] = name
        return self

    def set_password(self, psw):
        """
        Set the password of the user.

        :return:The user object
        """
        self.config['password'] = psw
        return self

    def description(self):
        """
        Returns the description for the user.

        :return:The user description
        """
        if 'description' not in self.config:
            return None
        return self.config['description']

    def set_description(self, description):
        """
        Set the description for the user

        :param description: A description for the user
        :return:The user object
        """
        self.config['description'] = description
        return self

    def role_names(self):
        """
        Returns the roles for this user

        :return:The list of roles
        """
        if u'role' not in self.config:
            return None
        return self.config[u'role']

    def set_role_names(self, roles):
        """
        Sets the roles for this user

        :return:The user object
        """
        if not(isinstance(roles, list)):
            raise exceptions.InvalidValue("Roles must be a list")

        self.config[u'role'] = roles
        return self

    def add_role_name(self, add_role):
        """
        Adds the specified role to roles for this user

        :return:The user object
        """
        roles = set()
        roles.add(add_role)
        if u'role' in self.config:
            for role in self.config[u'role']:
                roles.add(role)
        self.config[u'role'] = []
        for role in roles:
            self.config[u'role'].append(role)
        return self

    def remove_role_name(self, remove_role):
        """
        Removes the specified role to roles for this user

        :return:The user object
        """
        roles = set()
        if u'role' in self.config:
            for role in self.config[u'role']:
                if role != remove_role:
                    roles.add(role)
        self.config[u'role'] = []
        for role in roles:
            self.config[u'role'].append(role)
        return self

    def create(self, connection):
        """
        Creates the User on the MarkLogic server.

        :param connection: The connection to a MarkLogic server
        :return: The User object
        """
        uri = "http://{0}:{1}/manage/v2/users".format(connection.host, connection.management_port)

        response = requests.post(uri, json=self.config, auth=connection.auth)
        if response.status_code not in [200, 201, 204]:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)

        return self

    def save(self, connection):
        uri = "http://{0}:{1}/manage/v2/users/{2}/properties".format(connection.host, connection.management_port,
                                                                     self.config[u'user-name'])
        response = requests.put(uri, json=self.config, auth=connection.auth)

        if response.status_code not in [200, 204]:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)

        return self

    def remove(self, connection):
        uri = "http://{0}:{1}/manage/v2/users/{2}".format(connection.host, connection.management_port,
                                                          self.config[u'user-name'])
        response = requests.delete(uri, auth=connection.auth)

        if response.status_code not in [200, 204] and not response.status_code == 404:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)

        return self

    @classmethod
    def list_users(cls, connection):
        """
        List all the users in the security database.

        :param connection:The connection to a MarkLogic server
        :return:A list of Users
        """

        uri = "http://{0}:{1}/manage/v2/users".format(connection.host, connection.port)
        response = requests.get(uri, auth=connection.auth, headers={'accept': 'application/json'})

        if response.status_code != 200:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)

        results = []
        json_doc = json.loads(response.text)

        for item in json_doc['user-default-list']['list-items']['list-item']:
            temp = User("temp")
            user_uri = "http://{0}:{1}{2}/properties".format(connection.host, connection.port, item['uriref'])

            response = requests.get(user_uri, auth=connection.auth, headers={'accept': 'application/json'})
            if response.status_code != 200:
                raise exceptions.UnexpectedManagementAPIResponse(response.text)

            temp.config = json.loads(response.text)
            results.append(temp)

        return results


    @classmethod
    def lookup(cls, name, connection):
        """
        Look up an individual user from the security database.

        :param name: The name of the user
        :param connection: The connection to the MarkLogic database
        :return: The user
        """
        uri = "http://{0}:{1}/manage/v2/users/{2}/properties".format(connection.host, connection.port,
                                                                     name)
        response = requests.get(uri, auth=connection.auth, headers={'accept': 'application/json'})

        if response.status_code == 200:
            result = User("temp")
            result.config = json.loads(response.text)
            return result
        elif response.status_code == 404:
            return None
        else:
            raise exceptions.UnexpectedManagementAPIResponse(response.text)
