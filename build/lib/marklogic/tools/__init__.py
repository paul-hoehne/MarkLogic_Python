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

__author__ = 'phoehne'


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
