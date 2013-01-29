#coding = utf-8
__author__ = "luztak"

"""Utils."""

import feedparser

def get_feed(feedurl):
  """Return original data fetched by feedparser."""
  return feedparser.parse(feedurl)

def feedize(feed):
  """Change feedparser data to our format.?""
  pass
