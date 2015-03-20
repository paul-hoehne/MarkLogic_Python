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

import os
import urllib2
import re


"""
These are assorted tools to help the end user.  The goal is to provide
a simple set of scripting interfaces.
"""

class MLCPLoader():
    """
    This class will execute the content pump to load data.
    """
    def __init__(self):
        pass

    def load(self, conn):
        pass

    def clear_directory(self):
        if os.path.isdir(".mlcp"):
            os.popen("rm -rf .mlcp")

    def download_mlcp(self):
        os.mkdir(".mlcp")
        request = urllib2.urlopen("http://developer.marklogic.com/download/binaries/mlcp/mlcp-Hadoop2-1.3-1-bin.zip")
        with open(".mlcp/mlcp.zip", "wb") as bin_file:
            data = request.read()
            bin_file.write(data)

        os.popen("cd .mlcp; unzip mlcp.zip")
        files = os.listdir(".mlcp")
        for file in files:
            if re.match(r"[\w\-]+(\d\.\d).*", file):
                os.popen("cd .mlcp; mv {0} mlcp; rm mlcp.zip".format(file))

    def load_directory(self, conn, database, data_directory, collections=None, prefix=''):
        command_path = ".mlcp/mlcp/bin/mlcp.sh"

        if collections:
            collections_command = "-output_collections \"{0}\"".format(",".join(collections))
        else:
            collections_command = ''

        command_line = "{0} import -username {1} -password {2} -host {3} -port {4} -database {5} {6} " \
                       "-input_file_path {7} -output_uri_replace \"{8},'{9}'\""

        run_line = command_line.format(command_path, conn.auth.username, conn.auth.password, conn.host,
                                       conn.port, database.database_name(), collections_command, data_directory,
                                       os.path.abspath(data_directory), prefix)
        with os.popen(run_line) as in_file:
            for line in in_file:
                print(line.rstrip())




class Watcher():
    """
    Watcher will observe a directory and all the files in the director
    or its descendants.  If any change, it should upload the file to
    the appropriate database.
    """
    def __init__(self):
        pass

    def watch(self, conn, directory):
        pass
