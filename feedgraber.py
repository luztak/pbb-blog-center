#coding = utf-8
__author__ = "luztak"

""" Feed graber.
Run in crontab.
"""

import feedlist
import utils
from db import dbase


class feedgraber(object):
    def __init__(self, authors):
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
        db = dbase()
        for author in self.grabbed:
            for feed in author[1]:
                if db.entries.find({'url': feed.url}):
                    db.entries.update(
                        {'url': feed.url},
                        {'$set': {
                            'member': author[0],
                            'title': feed.title,
                            'url': feed.url,
                            'published': feed.published,
                            'updated': feed.updated,
                            'summary': feed.summary,
                            'content': feed.content.value}}
                    )

    def run(self):
        self.grab()
        self.intodb()
