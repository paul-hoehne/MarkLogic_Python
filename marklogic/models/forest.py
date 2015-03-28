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
# Paul Hoehne       03/01/2015     Initial development
#

import socket
import requests
import json
from .utilities.validators import validate_forest_availability

"""
MarkLogic Forest support classes.
"""

class Forest:
    """
    Encapsulates a MarkLogic forest.  Can be added to a database configuration to create forests
    with specific options.
    """
    def __init__(self, name):
        self.config = {
            u'forest-name': name,
            u'host': socket.gethostname().lower()
        }

    def set_host(self, host='localhost'):
        """
        Set the hostname to use for the forest.

        :param host: The server's host name
        :return: The Forest object
        """
        self.config[u'host'] = host
        return self

    def host(self):
        """
        Return the hostname for this forest

        :return: The hostname
        """
        return self.config['host']

    def set_database(self, db='Documents'):
        """
        The database to which this forest belongs.

        :param db: A database name
        :return: The Forest object
        """
        self.config['database'] = db
        return self

    def database(self):
        """
        Return the database for the forest

        :return: The asociated database
        """
        return self.config['database']

    def set_data_directory(self, datadir='/var/opt/MarkLogic/Data'):
        """
        The data directory where the forest's data will be stored.  It must be a valid path
        on the server running MarkLogic.

        :param datadir: The forest's data directory
        :return: The Forest object
        """
        self.config['data-directory'] = datadir
        return self

    def data_directory(self):
        """
        Returns the data directory for the forest.

        :return: The data directory path
        """
        return self.config['data-directory']

    def set_large_data_directory(self, datadir='/var/opt/MarkLogic/Big_Data'):
        """
        The forest's big data directory.  This must be a valid directory on the server where
        MarkLogic is running.

        :param datadir: The forest's large data directory
        :return: The Forest object
        """
        self.config['large-data-directory'] = datadir
        return self

    def large_data_directory(self):
        """
        Return the large data directory for the forest

        :return:The large data directory path
        """
        return self.config['large-data-directory']

    def set_fast_data_directory(self, datadir='/var/opt/MarkLogic/Fast_Data'):
        """
        The forest's fast data directory.  This must be a valid directory on the server where
        MarkLogic is running.

        :param datadir: The forest's fast data directory
        :return: The Forest object
        """
        self.config['fast-data-directory'] = datadir
        return self

    def fast_data_directory(self):
        """
        Return the fast data directory for the forest.

        :return:The fast data directory
        """
        return self.config['fast-data-directory']

    def set_availability(self, which='online'):
        """
        Indicate weather the forest is available.

        :param which: The availability of the forest
        :return: The Forest object
        """
        validate_forest_availability(which)
        self.config['availability'] = which
        return self

    def availability(self):
        """
        Returns the availability status for the forest.

        :return: Availability status
        """
        return self.config[u'availability']

    def name(self):
        """
        Returns the name of the forest.

        :return: The forest name
        """
        return self.config[u'forest-name']

    def create(self, connection):
        """
        Creates the forest on the MarkLogic server.

        :param connection: The connection to a MarkLogic server
        :return: The Forest object
        """
        uri = "http://{0}:{1}/manage/v2/forests".format(connection.host, connection.management_port)
        response = requests.post(uri, json=self.config, auth=connection.auth)
        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def save(self, connection):
        """
        Saves the updated forest configuration to the MarkLogic server.

        :param connection: The connection to a MarkLogic server
        :return: The Forest object
        """
        uri = "http://{0}:{1}/manage/v2/forests/{2}/properties".format(connection.host, connection.management_port,
                                                              self.config[u'forest-name'])
        response = requests.put(uri, json=self.config, auth=connection.auth)

        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def remove(self, connection):
        """
        Delete a forest from the MarkLogic server.

        :param connection: The connection to a MerkLogic server
        :return: The Forest object
        """
        uri = "http://{0}:{1}/manage/v2/forests/{2}?level=full".format(connection.host, connection.management_port,
                                                                       self.config[u'forest-name'])
        response = requests.delete(uri, auth=connection.auth)

        if response.status_code > 299 and not response.status_code == 404:
            raise Exception(response.text)

        return self

    @classmethod
    def lookup(cls, name, connection):
        """
        Look up a forest's configuration from the MarkLogic server.

        :param name: The name of the forest
        :param connection: The connection to a MarkLogic server
        :return: The Forest object
        """
        uri = "http://{0}:{1}/manage/v2/forests/{2}/properties".format(connection.host, connection.management_port, name)
        response = requests.get(uri, auth=connection.auth, headers={u'accept': u'application/json'})
        if response.status_code > 299:
            raise response
        result = Forest("temp")
        result.config = json.loads(response.text)

        return result