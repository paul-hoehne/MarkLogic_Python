__author__ = 'phoehne'

import requests
import json

class HttpServer:
    def __init__(self, name, port, content_db_name=None):
        self.config = {
            u'server-name': name,
            u'server-type': u'http',
            u'group-name': u'Default',
            u'root': u'/',
            u'enabled': True,
            u'port': port,
            u'modules-database': name + "-modules",
            u'content-database': name
        }

        if content_db_name:
            self.config[u'content-database'] = content_db_name

    def set_url_rewriter(self, which="/rewriter.sjs"):
        self.config[u'url-rewriter'] = which
        return self

    def set_rewrite_resolves_globally(self, enabled=True):
        self.config[u'rewrite-resolves-globally'] = enabled
        return self

    def set_authentication(self, which=u'digest'):
        self.config[u'authentication'] = which
        return self

    def set_group_name(self, which=u'Default'):
        self.config[u'group-name'] = which
        return self

    def set_root(self, which=u'/'):
        self.config[u'root'] = which
        return self

    def set_enabled(self, enabled=True):
        self.config[u'enabled'] = enabled
        return self

    def set_port(self, limit=8080):
        self.config[u'port'] = limit
        return self

    def set_modules_database(self, which=u'modules'):
        self.config[u'modules-database'] = which
        return self

    def set_content_database(self, which=u'content'):
        self.config[u'content-database'] = which
        return self

    def create(self, connection):
        uri = "http://{0}:{1}/manage/v2/servers".format(connection.host, connection.management_port)
        response = requests.post(uri, json=self.config, auth=connection.auth)
        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def save(self, connection):
        uri = "http://{0}:{1}/manage/v2/servers/{2}/properties".format(connection.host, connection.management_port,
                                                                       self.config[u'server-name'])
        response = requests.put(uri, json=self.config, auth=connection.auth)

        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def remove(self, connection):
        uri = "http://{0}:{1}/manage/v2/servers/{2}?group-id={3}".format(connection.host, connection.management_port,
                                                                         self.config[u'server-name'],
                                                                         self.config[u'group-name'])
        response = requests.delete(uri, auth=connection.auth)

        if response.status_code > 299 and not response.status_code == 404:
            raise Exception(response.text)

        return self

    @classmethod
    def lookup(cls, name, connection, group=u'Default'):
        uri = "http://{0}:{1}/manage/v2/servers/{2}/properties?group-id={3}".format(connection.host, connection.management_port,
                                                                         name, group)
        response = requests.get(uri, auth=connection.auth, headers={u'accept': u'application/json'})
        if response.status_code > 299 and not response.status_code == 404:
            raise Exception(response.text)

        if not response.status_code == 404:
            result = HttpServer("temp", 8080)
            result.config = json.loads(response.text)
        else:
            result = None

        return result


class XdbcServer:
    def __init__(self, name, port):
        self.config = {
            u'server-name': name,
            u'server-type': u'xdbc',
            u'group-name': u'Default',
            u'root': u'/',
            u'enabled': True,
            u'port': port,
            u'modules-database': name + '-modules',
            u'content-database': name
        }

    def set_authentication(self, which=u'digest'):
        self.config[u'authentication'] = which
        return self

    def set_group_name(self, which=u'Default'):
        self.config[u'group-name'] = which
        return self

    def set_root(self, which=u'/'):
        self.config[u'root'] = which
        return self

    def set_enabled(self, enabled=True):
        self.config[u'enabled'] = enabled
        return self

    def set_port(self, limit=8080):
        self.config[u'port'] = limit
        return self

    def set_modules_database(self, which=u'modules'):
        self.config[u'modules-database'] = which
        return self

    def set_content_database(self, which=u'content'):
        self.config[u'content-database'] = which
        return self

    def create(self, connection):
        uri = "http://{0}:{1}/manage/v2/servers".format(connection.host, connection.management_port)
        response = requests.post(uri, json=self.config, auth=connection.auth)
        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def save(self, connection):
        uri = "http://{0}:{1}/manage/v2/servers/{2}/properties".format(connection.host, connection.management_port,
                                                              self.config[u'server-name'])
        response = requests.put(uri, json=self.config, auth=connection.auth)

        if response.status_code > 299:
            raise Exception(response.text)

        return self

    def remove(self, connection):
        uri = "http://{0}:{1}/manage/v2/servers/{2}".format(connection.host, connection.management_port,
                                                              self.config[u'server-name'])
        response = requests.delete(uri, auth=connection.auth)

        if response.status_code > 299 and not response.status_code == 404:
            raise Exception(response.text)

        return self

    @classmethod
    def lookup(cls, name, connection):
        uri = "http://{0}:{1}/manage/v2/servers/{2}/properties".format(connection.host, connection.management_port, name)
        response = requests.get(uri, auth=connection.auth, headers={u'accept': u'application/json'})
        if response.status_code > 299:
            raise response
        result = XdbcServer("temp", 8080)
        result.config = json.loads(response.text)

        return result