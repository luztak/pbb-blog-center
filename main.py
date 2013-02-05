#coding = utf-8
__author__ = "luztak"

"""Main."""

import pymongo
import tornado.web
import tornado.ioloop
import tornado.escape
from tornado.options import define, options, parse_command_line
from handlers import HomeHandler, DashboardHandler, FeedHandler

define("port", default=12307, help="Port of server service")

cookie_secret = "hello, world but not you, hacker."
define("cookie_secret", default=cookie_secret, help="Cookie Secret")


class Application(tornado.web.Application):
    def __init__(self):
        self.db = pymongo.Connection(
            options["db_host"],
            options["db_port"])[options["db_name"]]
        super(Application, self).__init__([
            HomeHandler,
            DashboardHandler,
            FeedHandler]
        )

urls = [
    (r'/', HomeHandler),
    (r'/dashboard', DashboardHandler),
    (r'/feed', FeedHandler),
]

blogcenter = Application(urls)

if __name__ == "__main__":
    parse_command_line()
    blogcenter.listen(options['server_port'])
    tornado.ioloop.IOLoop.Instance.start()
