#coding = utf-8
__author__ = "luztak"

"""DB shell of Blog Center.
"""

import pymongo
from tornado.options import define, options

define("db_host", default="127.0.0.1", help="Host of MongoDB")
define("db_port", default=12306, help="Port of MongoDB")
define("db_name", default="blogcenter", help="Name of base of MongoDB")


class dbase(object):
    def __init__(self):
        self.db = pymongo.Connection(
            options["db_host"],
            options["db_port"])[options["db_name"]]

    def __getitem__(self, name):
        return getattr(self.db, name)
