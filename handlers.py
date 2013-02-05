#coding = utf-8
__author__ = "luztak"

"""Handlers."""

import tornado.web
import tornado.escape


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        u = self.get_secure_cookie("user")
        return self.db.members.find({'password': u})

    def get_entries(self, filter_type=None, filter_content=None):
        if filter_type:
            entries = self.db.entries.find({filter_type: filter_content})
        else:
            entries = self.db.entries.find()
        return entries

    @property
    def messages(self):
        if not hasattr(self, '_messages'):
            messages = self.get_secure_cookie('bc_flash_messages')
            self._messages = []
            if messages:
                self._messages = tornado.escape.json_decode(messages)
            return self._messages

    def flash(self, message, msgtype='error'):
        self.messages.append((msgtype, message))
        self.set_secure_cookie('bc_flash_messages',
            tornado.escape.json_encode(self.messages))

    def get_flashed_messages(self):
        messages = self.messages
        self._messages = []
        self.clear_cookie('bc_flash_messages')
        return messages


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
            self.flash_message("Please choose an action!")
            self.redirect("/dashboard")
        elif action == "changefeed":
            flag = self.change_feed(action_data)
            if flag:
                self.flash_message("Feed changed successfully.",
                    mstgype="success")
            else:
                self.flash_message("Feed isn't changed while an error occurs.")
            self.redirect("/dashboard")
            return

    def change_feed(self, feedurl):
        def get_old(author):
            import feedlist
            return feedlist.feedlist[author][feedlist.FEED_URL]

        old_url = get_old(self.current_user['username'])
        f = open("list.py").read()
        f = f.replace(old_url, feedurl)
        open("list.py", "w").write(f)
        return feedurl in open("list.py").read()


class FeedHandler(BaseHandler):
    def get(self):
        topics = self.db.entries.find(sort=[('updated', -1)])
        self.render('feed.xml', topics=topics)
