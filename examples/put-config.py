#!/usr/bin/python

__author__ = 'ndw'

import argparse
import logging
import json
import os
import base64
from requests.auth import HTTPDigestAuth
from marklogic.models.connection import Connection
from marklogic.models.database import Database
from marklogic.models.permission import Permission
from marklogic.models.privilege import Privilege
from marklogic.models.role import Role
from marklogic.models.server import Server
from marklogic.models.user import User

#logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--host", action='store', default="localhost",
                    help="Management API host")
parser.add_argument("--username", action='store', default="admin",
                    help="User name")
parser.add_argument("--password", action='store', default="admin",
                    help="Password")
parser.add_argument("--json", action="store",
                    help="Name of the file containing JSON config")
args = parser.parse_args()

with open(args.json) as data_file:
    data = json.load(data_file)

conn = Connection(args.host, HTTPDigestAuth(args.username, args.password))

# Create roles
for config in data['roles']:
    name = config['role-name']
    role = Role.lookup(conn, name)
    if role is None:
        print("Need to create role: {0}".format(name))
        role = Role(name)
        role.create(conn)

# Update privileges
for config in data['roles']:
    name = config['role-name']
    role = Role.unmarshal(config)
    print("Updating role: {0}".format(name))
    role.update(conn)

# Update privileges
for config in data['privileges']:
    name = config['privilege-name']
    kind = config['kind']
    priv = Privilege.lookup(conn, name, kind)
    verb = "Creating" if priv is None else "Updating"
    priv = Privilege.unmarshal(config)
    print("{0} {1} privilege: {2}".format(verb, kind, name))
    priv.update(conn)

# Update users
for config in data['users']:
    name = config['user-name']
    user = User.lookup(conn, name)
    if user is None:
        verb = "Creating"
        user = User.unmarshal(config)
        # Must assign some sort of password
        user.set_password(base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8'))
        print("{0} user: {1}".format(verb, name))
        user.create(conn)
    else:
        verb = "Updating"
        user = User.unmarshal(config)
        print("{0} user: {1}".format(verb, name))
        user.update(conn)

# Create databases
for config in data['databases']:
    name = config['database-name']
    db = Database.lookup(conn, name)
    if db is None:
        print("Need to create database: {0}".format(name))
        db = Database(name)
        db.create(conn)

# Update databases
for config in data['databases']:
    name = config['database-name']
    db = Database.unmarshal(config)
    print("Updating database: {0}".format(name))
    db.update(conn)

# Update servers
for config in data['servers']:
    name = config['server-name']
    group = config['group-name']
    server = Server.lookup(conn, name, group)
    verb = "Creating" if server is None else "Updating"
    server = Server.unmarshal(config)
    print("{0} server: {1}[{2}]".format(verb, name, group))
    server.update(conn)
