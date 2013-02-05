#coding = utf-8
__author__ = "luztak"

"""Utils."""

import feedparser
import datetime
import time

"""Our feed format:
feed[title,
    (id),
    #author #no way to get yet
    url,
    published,
    updated,
    summary,
    content
    ]
"""


def get_feeds(feedurl):
    """Return original data fetched by feedparser."""
    entries = feedparser.parse(feedurl).entries
    return [{
        'title': entry.title,
        #'id': entry.id,
        #'author': '',
        'url': entry.content.base,
        'published': convert_fptime(entry.published_parsed),
        'published_atom': entry.published,
        'updated': convert_fptime(entry.updated_parsed),
        'updated_atom': entry.updated,
        'summary': entry.summary or entry.content.value,
        'content': entry.content.value}
        for entry in entries]


def convert_fptime(fptime):
    return int(time.mktime(datetime.datetime(
        fptime[0],
        fptime[1],
        fptime[2],
        fptime[3],
        fptime[4],
        fptime[5]).timetuple()))
