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
    origins = feedparser.parse(feedurl).entries
    return [{
        title:entry.title,
        #id:entry.id,
        url:entry.content.base,
        published:convert_time(entry.published_parsed),
        updated:convert_time(entry.updated_parsed),
        summary:entry.summary or entry.content.value,
        content:entry.content
        }
        for entry in origins]
