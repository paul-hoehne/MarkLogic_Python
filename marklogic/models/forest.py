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

class Forest:
    def __init__(self, name):
        self.config = {
            u'forest-name': name,
            u'host': socket.gethostname().lower()
        }

    def set_host(self, host='localhost'):
        self.config[u'host'] = host
        return self

    def set_database(self, db='Documents'):
        self.config[u'database'] = db
        return self

    def set_data_directory(self, datadir='/var/opt/MarkLogic/Data'):
        self.config[u'data-directory'] = datadir
        return self

    def set_large_data_directory(self, datadir='/var/opt/MarkLogic/Big_Data'):
        self.config[u'large-data-directory'] = datadir
        return self

    def set_fast_data_directory(self, datadir='/var/opt/MarkLogic/Fast_Data'):
        self.config[u'fast-data-directory'] = datadir
        return self

    def set_availability(self, which='online'):
        self.config[u'availability'] = which
        return self

    def name(self):
        return self.config[u'forest-name']

    def create(self, connection):
        uri = "http://{0}:{1}/manage/v2/forests".format(connection.host, connection.management_port)
        response = requests.post(uri, json=self.config, auth=connection.auth)
        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def save(self, connection):
        uri = "http://{0}:{1}/manage/v2/forests/{2}/properties".format(connection.host, connection.management_port,
                                                              self.config[u'forest-name'])
        response = requests.put(uri, json=self.config, auth=connection.auth)

        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def remove(self, connection):
        uri = "http://{0}:{1}/manage/v2/forests/{2}?level=full".format(connection.host, connection.management_port,
                                                              self.config[u'forest-name'])
        response = requests.delete(uri, auth=connection.auth)

        if response.status_code > 299 and not response.status_code == 404:
            raise Exception(response.text)

        return self

    @classmethod
    def lookup(cls, name, connection):
        uri = "http://{0}:{1}/manage/v2/forests/{2}/properties".format(connection.host, connection.management_port, name)
        response = requests.get(uri, auth=connection.auth, headers={u'accept': u'application/json'})
        if response.status_code > 299:
            raise response
        result = Forest("temp")
        result.config = json.loads(response.text)

        return result