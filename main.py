#coding = utf-8
__author__ = "luztak"

"""Main."""

import pymongo
import tornado.web

settings = {
    'port':12307,
    }
    

db_settings = [
    '127.0.0.1',
    12306,
    ''
    ]

db = pymongo.Connection(
    db_settings[0],
    db_settings[1]
    )[db_settings[2]]

cookie_secret = "hello, world but not to you, hacker."


class BaseHanldwr(tornado.web.Application):
    def get_current_user(self):
        current_user = None
        u = self.get_secure_cookie("user")
        member = db.members.find.find({'password':u})
        if member:
            current_user = member
        return current_user
    
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
            self.redirect("/") #how to name this......?
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
    blogcenter.listen(settings['port'])
    tornado.ioloop.IOLoop.Instance.start()
