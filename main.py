#coding = utf-8
__author__ = "luztak"

"""Main."""

import pymongo
import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line

define("server_port", default=12307, help="Port of server service")

define("db_host", default="127.0.0.1", help="Host of MongoDB")
define("db_port", default=12306, help="Port of MongoDB")
define("db_name", default="blogcenter", help="Name of base of MongoDB")


db = pymongo.Connection(
    options["db_host"],
    options["db_port"]
    )[options["db_name"]

cookie_secret = "hello, world but not to you, hacker."


class BaseHanlder(tornado.web.RequestHandler):
    def get_current_user(self):
        u = self.get_secure_cookie("user")
        return db.members.find.find({'password':u})

    def get_entries(self, filter_type=None, filter_content=None):
        if filter_type:
            entries = db.entries.find({filter_type:filter_content})
        else:
            entries = db.entries.find()
        return entries


class HomeHandler(BaseHandler):
    def get(self, filter_type=None, filter_content=None):
        current_user = self.get_current_user()
        entries = self.get_entries(filter_type, filter_content)
        self.render("homepage.html", current_user=current_user, entries=entries)


class DashboardHandler(BaseHandler):
    def get(self):
        if not self.get_current_user():
            self.redirect("/")
            return
        self.render("dashboard.html")
    def post(self, action=None, action_data=None):
        if not self.get_current_user():
            self.redirect("/")
            return
        if not action or action_data:
            self.flush_message("Please choose an action!")
            self.redirect("/dashboard") #not good -- hard coded
            return
        if action == "changepassword":
            #see what PBB does here.
            self.flush_message("Password successfully changed.")
            self.redirect("/dashboard")
            return
        elif action == "changefeed":
            flag = self.change_feed(action_data)
            if flag:
                self.flush_message("Feed successfully changed.")
            else:
                self.flush_message("Feed isn't changed while an error occurs.")
            self.redirect("/dashboard")
            return


urls = [
    (r'/', HomeHandler),
    (r'/dashboard', DashboardHandler),
    ]
    
blogcenter = tornado.web.Application(urls)

if __name__ == "__main__":
    parse_command_line()
    blogcenter.listen(options['server_port'])
    tornado.ioloop.IOLoop.Instance.start()
