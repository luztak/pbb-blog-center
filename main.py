#coding = utf-8
__author__ = "luztak"

"""Main."""

import pymongo
import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line

define("port", default=12307, help="Port of server service")

define("db_host", default="127.0.0.1", help="Host of MongoDB")
define("db_port", default=12306, help="Port of MongoDB")
define("db_name", default="blogcenter", help="Name of base of MongoDB")

cookie_secret = "hello, world but not you, hacker."
define("cookie_secret", default=cookie_secret, help="Cookie Secret")

db = pymongo.Connection(
    options["db_host"],
    options["db_port"])[options["db_name"]]


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        u = self.get_secure_cookie("user")
        return db.members.find.find({'password': u})

    def get_entries(self, filter_type=None, filter_content=None):
        if filter_type:
            entries = db.entries.find({filter_type: filter_content})
        else:
            entries = db.entries.find()
        return entries


class HomeHandler(BaseHandler):
    def get(self, filter_type=None, filter_content=None):
        entries = self.get_entries(filter_type, filter_content)
        self.render("homepage.html", entries=entries)


class DashboardHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/")
            return
        self.render("dashboard.html")

    def post(self, action=None, action_data=None):
        if not self.current_user:
            self.redirect("/")
            return
        if not action or action_data:
            self.flush_message("Please choose an action!")
            self.redirect("/dashboard")
        elif action == "changefeed":
            flag = self.change_feed(action_data)
            if flag:
                self.flush_message("Feed changed successfully.")
            else:
                self.flush_message("Feed isn't changed while an error occurs.")
            self.redirect("/dashboard")
            return

    def change_feed(self, feedurl):
        def get_old(author):
            import feedlist
            return feedlist.feedlist[author][feedlist.FEED_URL]

        old_url = get_old(self.current_useru['username'])
        f = open("list.py").read()
        f = f.replace(old_url, feedurl)
        open("list.py", "w").write(f)
        return feedurl in open("list.py").read()


urls = [
    (r'/', HomeHandler),
    (r'/dashboard', DashboardHandler), ]

blogcenter = tornado.web.Application(urls)

if __name__ == "__main__":
    parse_command_line()
    blogcenter.listen(options['server_port'])
    tornado.ioloop.IOLoop.Instance.start()
