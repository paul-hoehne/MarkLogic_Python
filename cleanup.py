__author__ = 'phoehne'

import time
from requests.auth import HTTPDigestAuth
from models.database import Database
from models.connection import Connection
from models.server import HttpServer


conn = Connection("localhost", HTTPDigestAuth("admin", "admin"))

srvr = HttpServer.lookup("test-one-http", conn)
if srvr:
    srvr.remove(conn)

# TODO determine if the server is restarted
time.sleep(30)


db = Database.lookup("test-one", conn)
db.remove(conn)

mod = Database.lookup("test-one-modules", conn)
mod.remove(conn)