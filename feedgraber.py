#coding = utf-8
__author__ = "luztak"

""" Feed graber.
Run in crontab.
"""

import feedlist
import utils
from handlers import BaseHandler
import datetime


class feedgraber(BaseHandler):
    def init(self, authors):
        grablist = []
        for author in authors:
            for feedy in feedlist.feedlist:
                if feedy[feedlist.AUTHOR_NAME] == author:
                    grablist.append((feedy[feedlist.AUTHOR_NAME],
                        feedy[feedlist.FEED_URL])
                    )
        self.grablist = grablist

    def grab(self):
        grabbed = []
        for grabby in self.grablist:
            grabbed.append(
                (grabby[0],
                utils.get_feeds(grabby[1]))
            )
        self.grabbed = grabbed

    def intodb(self):
        for author in self.grabbed:
            for feed in author[1]:
                if self.db.entries.find({'url': feed.url}):
                    self.db.entries.update({'url': feed.url},
                        {'$set': {
                            'member': author[0],
                            'title': feed.title,
                            'url': feed.url,
                            'published': feed.published,
                            'updated': feed.updated,
                            'summary': feed.summary,
                            'content': feed.content.value}}
                    )
                else:
                    self.db.entries.insert({
                        'member': author[0],
                        'title': feed.title,
                        'url': feed.url,
                        'published': feed.published,
                        'updated': feed.updated,
                        'summary': feed.summary,
                        'content': feed.content.value}
                    )
        # last grab and this time grab
        last = self.db.entries_time.find({'type': 'this'})['datetime']
        self.db.entries_time.update({'type': 'last'},
            {'$set': {'datetime': last}})
        self.db.entries_time.update({'type': 'this'},
            {'$set': {'datetime': datetime.datetime()}})

    def run(self):
        self.init()
        self.grab()
        self.intodb()
