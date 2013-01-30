#coding = utf-8
__author__ = "luztak"

"""Utils."""

import feedparser

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
        'title':entry.title,
        #'id':entry.id,
        #'author':'',
        'url':entry.content.base,
        'published':convert_fptime(entry.published_parsed),
        'updated':convert_fptime(entry.updated_parsed),
        'summary':entry.summary or entry.content.value,
        'content':entry.content.value
        }
        for entry in entries]
