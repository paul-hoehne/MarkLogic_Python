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
# Paul Hoehne       03/03/2015     Initial development
#


from ..models.database import Database
from ..models.forest import Forest
from ..models.server import HttpServer


class Quickstart():
    def __init__(self):
        pass

    def create(self, conn):
        pass

    def destroy(self):
        pass


class SimpleDatabase(Quickstart):
    def __init__(self, app_name, port=8100, forests=3):
        """
        Factory class to acreate databases with an HTTP server and modules database.  The parts will be
        named <app_name>_db for the database, <app_name>_modules_db for the modules database,
        and the HTTP server port will be on the given port.

        :param app_name: The base name for the application
        :param port: The port number for the HTTP server
        :param forests: The number of forests
        :return: The initialized object
        """
        Quickstart.__init__(self)

        self._db_name = app_name + "_db"
        self._modules_db_name = app_name + "_modules_db"
        self._app_port = port
        self._http_server = app_name + "_http_" + str(port)
        self._forests = [self._db_name + "_forest_" + str(i + 1) for i in range(0, forests)]
        self._modules_forest = self._modules_db_name + "_forest"

    def create(self, conn, hostname='localhost.localdomain'):
        """
        Connects to the server and creates the relevant artifacts, including the database,
        the modules database, and the HTTP server.

        :param conn: The server connection
        :return:A map containing the content db, the modules db and the HTTP server.
        """
        data_database = Database(self._db_name, hostname)
        data_database.set_forests(self._forests)

        modules_database = Database(self._modules_db_name, hostname)

        server = HttpServer(self._http_server, self._app_port, self._db_name)
        server.set_modules_database(self._modules_db_name)

        data_database.create(conn)
        modules_database.create(conn)
        server.create(conn)

        return {
            u'content': data_database,
            u'modules': modules_database,
            u'server': server
        }
