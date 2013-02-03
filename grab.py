#coding = utf-8
__author__ = "luztak"

"""Grabber shell.
To be run by crontab.
"""

import feedgrabber
import feedlist

grabber = feedgrabber(
    [author[feedlist.AUTHOR_NAME] for author in list.feedlist])

grabber.run()
