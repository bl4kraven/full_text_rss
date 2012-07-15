#!/usr/bin/env python
# -*-coding:UTF-8-*-

# logging set
import logging
logging.basicConfig(filename="log.log",format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

import feedparser
from rsswriter import RssWriter,RssItem
from datetime import datetime
import sys

import Queue
from getfulltext import GetFullText


class Cache():

    def __init__(self, storage, time_zone, timeout, ttl_seconds=3600):
        """ storage: backend key-value storage.

            ttl_seconds: time to live time to content, default is 1 hours.

            user_agent: feedparser user agent
        """ 

        self.storage = storage
        self.ttl = ttl_seconds
        self.time_zone = time_zone
        self.timeout = timeout

    def fetch(self, url, new_feed):
        """Return the full text feed at url.

        url: The URL of the feed.

        new_feed=False: When True, create new feed, otherwise return local feed.
        """
        logger.info("fetch rss %s", url)
        key = url
        now = datetime.now()

        cached_time, cached_content = self.storage.get(key, (None, None))

        # not allow to create feed
        if not new_feed and not cached_content:
            logger.error("not allow to create feed")
            raise RuntimeError("not allow to create feed")

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

        if cached_content:
            # add conditional http GET
            rss_read = feedparser.parse(url,
                                        modified=cached_content.modified,
                                        etag=cached_content.etag)
        else:
            rss_read = feedparser.parse(url)


        status = rss_read.get("status", None)
        if status == 304:
            # no update, so update the cahce time
            self.storage[key] = (now, cached_content)
            return cached_content

        # 301/302 is http redirection
        elif status == 200 or status == 301 or status == 302:
            return self.fulltextrss(rss_read, key,  cached_content)

        else:
            logger.error("feedparser return http status code %d", status)
            raise RuntimeError("feedparser return unsuccess http status code")

    def fulltextrss(self, rss_read, key, cached_content):
        # full text rss output
        logger.debug("%s %s", rss_read.feed.title, rss_read.feed.description)

        full_text_rss = RssWriter()
        full_text_rss.set_title(rss_read.feed.title)
        full_text_rss.set_link(rss_read.feed.link)
        full_text_rss.set_description(rss_read.feed.description)
        full_text_rss.set_datetime(self.time_zone)

        # save modified and etag
        full_text_rss.modified = rss_read.get("modified", None)
        full_text_rss.etag = rss_read.get("etag", None)

        # thread pool queue
        queue = Queue.Queue()
        out_queue = Queue.Queue()

        # set item
        for item in rss_read.entries:
            logger.debug(item.title)

            # the guid is link.
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

            logger.debug("put in queue wait to thread to fetch")
            queue.put(item.link)

            full_text_rss.add_item(full_text_item)

        # spawn a poll of theads
        if not queue.empty():
            for i in range(4):
                t = GetFullText(queue, out_queue, self.timeout)
                t.setDaemon(True)
                t.start()

            # wait threads
            queue.join()

            while not out_queue.empty():
                url, content = out_queue.get()
                full_text_rss.find_item(url).set_content(content)

        # put in storage
        self.storage[key] = (full_text_rss.now, full_text_rss)
        return full_text_rss


def main():
    import shelve
    url = "http://www.ftchinese.com/rss/news"
    storage = shelve.open('.feedcache')
    cache = Cache(storage)
    cache.fetch(url)
    storage.close()

if __name__ == "__main__":
    main()
