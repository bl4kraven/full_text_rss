#!/usr/bin/env python
# -*-coding:UTF-8-*-

# logging set
import logging
logging.basicConfig(filename="log.log",level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
#logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

import urllib2
from readability.readability import Document
import feedparser
from rsswriter import RssWriter,RssItem
from datetime import datetime
import sys

from config import *

class Cache():

    #def __init__(self, storage, ttl_seconds=7200):
    def __init__(self, storage, ttl_seconds=10):
        """ storage: backend key-value storage.

            ttl_seconds: time to live time to content, default is 2 hours.

            user_agent: feedparser user agent
        """ 

        self.storage = storage
        self.ttl = ttl_seconds

    def fetch(self, url, off_line=False):
        """Return the full text feed at url.

        url: The URL of the feed.

        off_line=False: When True, only return data from the local
        cache and never access the remote URL.
        """
        logger.info("fetch rss %s", url)
        key = url
        now = datetime.now()

        cached_time, cached_content = self.storage.get(key, (None, None))

        # return the cache content
        if off_line:
            logger.debug('offline mode')
            return cached_content

        if cached_time:
            delta = now - cached_time
            seconds = delta.seconds + delta.days*24*3600
            if seconds <= self.ttl:
                logger.debug("in ttl return cache content")
                return cached_content
            else:
                logger.debug("out of ttl ready to parser")


        # fetch full text rss
        logger.debug("feedparser fetch...")
        rss_read = feedparser.parse(url)
        if not rss_read.version:
            raise RuntimeError("feedparser.parse:Unknown feed type")

        logger.debug("%s %s\n", rss_read.feed.title, rss_read.feed.description)

        # full text rss output
        full_text_rss = RssWriter()
        full_text_rss.set_title(rss_read.feed.title)
        full_text_rss.set_link(rss_read.feed.link)
        full_text_rss.set_description(rss_read.feed.description)
        full_text_rss.set_datetime(TIME_ZONE)

        # set item
        for item in rss_read.entries:
            if item.has_key("content"):
                raise RuntimeError("rss.content: Already a full feed text")

            logger.debug(item.title)
            if item.has_key("guid"):
                guid = item.guid
            else:
                guid = item.link

            # find item from cache
            if cached_content:
                cached_item = cached_content.find_item(guid)
                if cached_item and cached_item.get_content():
                    logger.debug("return cached item")
                    full_text_rss.add_item(cached_item)
                    continue

            full_text_item = full_text_rss.new_item()
            full_text_item.set_title(item.title)
            full_text_item.set_link(item.link)
            full_text_item.set_guid(guid)

            if item.has_key("published"):
                full_text_item.set_datetime(item.published)
            else:
                full_text_item.set_datetime(full_text_rss.get_datetime())

            try:
                logger.debug("http read item link %s", item.link)
                # timeout 
                html = urllib2.urlopen(item.link, timeout=TIMEOUT).read()
                readable_article = Document(html).summary()
                full_text_item.set_content(readable_article)
            except IOError:
                logger.warning("url open fail, read nothing!")

            full_text_rss.add_item(full_text_item)

        # put in storage
        self.storage[key] = (full_text_rss.now, full_text_rss)
        return full_text_rss

def main():
    import shelve
    try:
        url = "http://www.ftchinese.com/rss/news"
        storage = shelve.open('.feedcache')
        cache = Cache(storage)
        cache.fetch(url)
    finally:
        storage.close()


if __name__ == "__main__":
    main()
