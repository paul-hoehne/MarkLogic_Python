__author__ = 'phoehne'

from requests.auth import HTTPDigestAuth
from marklogic.models import Database, Connection, HttpServer
from marklogic.models.database.index import ElementRangeIndex
from marklogic.models.database.index import AttributeRangeIndex
from marklogic.models.host import Host

conn = Connection('localhost', HTTPDigestAuth('admin', 'admin'))

server_hostname = hosts = Host.list(conn)[0]

db = Database('test-one', server_hostname)
db.create(conn).load_file(conn, 'example_doc.json', '/test/document.json',
                          ['example', 'collection'])

modules = Database('test-one-modules', server_hostname)
modules.create(conn)

db = Database.lookup('test-one', conn)
db.add_index(ElementRangeIndex('int', '', 'order-id'))
db.add_index(AttributeRangeIndex('int', '', 'customer', '', 'id'))
db.update(conn)

srvr = HttpServer('test-one-http', port=10101)
srvr.set_content_database_name(db.database_name()) \
  .set_modules_database_name(modules.database_name())
srvr.create(conn)

db.load_file(conn, 'example_doc.json', '/example/file.json', ['test'])
db.load_directory_files(conn, 'data', '/test/data/', ['test2'])
db.load_directory(conn, 'data', collections=['this', 'that'])
