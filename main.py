#coding = utf-8
__author__ = "luztak"

"""Main."""

import pymongo

db_settings = [
    '127.0.0.1',
    12306,
    'blogcenter'
    ]

db = pymongo.Connection(
    db_settings[0],
    db_settings[1]
    )[db_settings[2]]

cookie_secret = "hello, world but not to you, hacker."


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        current_user = None
        u = self.get_secure_cookie("user")
        member = db.members.find({"password":u})
        if member:
            current_user = member
        entries = db.entries.find()
        self.render("homepage.html,current_user=current_user,entries=entries)


class AccountManagementHandler(tornado.web.RequestHandler):
    def get(self):
        current_user = self.get_secure_cookie("user")
        
