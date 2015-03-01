__author__ = 'phoehne'

from models.database import Database
from models.forest import Forest
from models.server import HttpServer


class Quickstart():
    def __init__(self):
        pass

    def create(self, conn):
        pass

    def destroy(self):
        pass


class SimpleDatabase(Quickstart):
    def __init__(self, app_name, port=8100, forests=3):
        Quickstart.__init__(self)

        self._db_name = app_name + "_db"
        self._modules_db_name = app_name + "_modules_db"
        self._app_port = port
        self._http_server = app_name + "_http_" + str(port)
        self._forests = [self._db_name + "_forest_" + str(i + 1) for i in range(0, forests)]
        self._modules_forest = [self._modules_db_name] + "_forest"

    def create(self, conn):
        data_database = Database(self._db_name)
        data_database.add_forest([Forest(forest_name) for forest_name in self._forests])

        modules_database = Database(self._modules_db_name)
        modules_database.add_forest(Forest(self._modules_forest))

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
