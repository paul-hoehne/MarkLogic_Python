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
