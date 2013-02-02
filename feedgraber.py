#coding = utf-8
__author__ = "luztak"

""" Feed graber.
Run in crontab.
"""

from list import *
from utils import *
import db

class feedgraber(object): 
    def __init__(self, authors): 
        grablist = []
        for author in authors: 
            for feedy in feedlist: 
                if feedy[AUTHOR_NAME] is author: 
                    grablist.append(
                        (feedy[AUTHOR_NAME],
                        feedy[FEED_URL]
                        ))
        self.grablist = grablist
    
    def grab(self):
        grabbed = []
        for grabby in self.grablist: 
            grabbed.append(
                (grabby[0],
                get_feeds(grabby[1])
                ))
        self.grabbed = grabbed
    
    def intodb(self): 
        db = db.db()
        for author in self.grabbed: 
            for feed in author[1]: 
                db.update(
                    {'member':author[0],
                    'title':feed.title,
                    'url':feed.url,
                    'published':feed.published,
                    'updated':feed.updated,
                    'summary':feed.summary,
                    'content':feed.content
                    })
    
    def run():
        self.grab()
        self.intodb()
            
